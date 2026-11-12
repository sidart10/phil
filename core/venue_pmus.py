"""Polymarket US venue adapter (read-only, public data). Stdlib only.

PROTECTED CORE - the trading agent must not edit files under core/.

Polymarket US (polymarket.us, a CFTC-regulated exchange) is a different venue
from the international Polymarket CLOB that the rest of core/ was written for.
Its public market data needs no key: gateway.polymarket.us/v1 serves market
records, order books and settlements. This module turns them into the gamma-
shaped records and CLOB-shaped books the engine already understands, so
ledger.py, forecast.py, resolve.py and score.py work on them unchanged through
the dispatch in pmapi.py.

Identifiers. A Polymarket US market is named by its slug. Inside Phil every id
carries a venue prefix so it can never collide with an international id:
  market id  "pmus:<slug>"
  token ids  "pmus:<slug>:long" and "pmus:<slug>:short"
Each market has ONE order book, for the long side. Buying the short side at p
is selling long at 1 - p, so the short side's asks are the long bids mirrored
(price 1 - p, same quantity) and its bids are the long offers mirrored.

Outcomes come from marketSides (long first): the record's own `outcomes` /
`outcomePrices` pair is not reliably ordered (2026-11-11: a market listed
outcomes ["No","Yes"] with prices [Yes price, No price]). Prices come from the
best bid and ask, never from marketSides[].price (see normalize).

Settlement. GET /v1/markets/<slug>/settlement returns {"settlement": x}, the
long side's payout per contract (1 = long won, 0 = short won, 0.5 = split), and
an error until the market settles. A market counts as closed here ONLY once a
settlement exists, so resolve.py never voids a bet because the venue is slow:
the record's `closed` flag stays false even on resolved markets.

Fees (docs.polymarket.us/fees, read 2026-11-11): fee = theta x C x p x (1 - p),
taker theta 0.0695 (table tennis 0.10), rounded to the cent per order. Market
records also carry a `feeCoefficient` (0.095 on every market checked). Until an
order preview confirms which one is charged, the larger of the two is used, so
paper fills never look cheaper than real ones.
"""
import datetime as dt
import json
import urllib.parse

import pmapi

GATEWAY = "https://gateway.polymarket.us/v1"
PREFIX = "pmus:"
VERSION = "pmus"
DOC_TAKER_THETA = 0.0695
# A game market's endDate is usually days after the game (a resolution
# window). The engine's horizon and min-minutes-to-resolution checks need when
# the result is known, so a game ends GAME_HOURS after it starts.
GAME_HOURS = 4
GAME_TYPES = {"moneyline", "drawable_outcome", "props", "spreads", "spread", "totals",
              "total"}


def is_market_id(market_id):
    return str(market_id).startswith(PREFIX)


def is_token(token_id):
    return str(token_id).startswith(PREFIX)


def slug_of(market_id):
    return str(market_id)[len(PREFIX):]


def _token(slug, side):
    return f"{PREFIX}{slug}:{side}"


def _split_token(token_id):
    slug, _, side = str(token_id)[len(PREFIX):].rpartition(":")
    if side not in ("long", "short") or not slug:
        raise ValueError(f"not a Polymarket US token id: {token_id!r}")
    return slug, side


def _px(amount):
    try:
        return float((amount or {}).get("value"))
    except (TypeError, ValueError):
        return None


def _parse_ts(value):
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def _iso(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def effective_end(rec):
    """When the result should be known: game start + GAME_HOURS for a game
    market whose start is before its endDate, else the endDate."""
    end = _parse_ts(rec.get("endDate"))
    start = _parse_ts(rec.get("gameStartTime"))
    if (start and end and start < end
            and (rec.get("marketType") or "").lower() in GAME_TYPES):
        return start + dt.timedelta(hours=GAME_HOURS)
    return end


def sides(rec):
    """(long_side, short_side) dicts from marketSides, or None when unusable."""
    ss = rec.get("marketSides") or []
    long_ = next((s for s in ss if s.get("long") is True), None)
    short = next((s for s in ss if s.get("long") is False), None)
    if not long_ or not short:
        return None
    return long_, short


def _question(rec):
    q = (rec.get("question") or "").strip()
    title = (rec.get("title") or "").strip()
    if title and title.lower() not in q.lower():
        q = f"{q}: {title}" if q else title
    return q


def fee_theta(rec):
    try:
        coeff = float(rec.get("feeCoefficient"))
    except (TypeError, ValueError):
        coeff = 0.0
    return max(coeff, DOC_TAKER_THETA)


def settlement(slug):
    """Long side's payout per contract once settled, else None."""
    try:
        r = pmapi.get_json(f"{GATEWAY}/markets/{urllib.parse.quote(slug)}/settlement",
                           retries=1)
    except RuntimeError:
        return None
    try:
        return float(r["settlement"])
    except (KeyError, TypeError, ValueError):
        return None


def normalize(rec, settled=None):
    """A Polymarket US market record as a gamma-shaped dict, or None when its
    sides are unusable. `settled` is settlement() for this market, if known."""
    s = sides(rec)
    if s is None or not rec.get("slug"):
        return None
    long_, short = s
    slug = rec["slug"]
    end = effective_end(rec)
    closed = settled is not None
    bid = _px(rec.get("bestBidQuote"))
    ask = _px(rec.get("bestAskQuote"))
    if closed:
        prices = [settled, round(1.0 - settled, 6)]
    elif bid is not None and ask is not None:
        # What each side costs to buy now: the long ask, and the short ask,
        # which is 1 - the long bid. marketSides[].price is not used: inside
        # /events records it disagrees with the book (2026-11-11: a 0.435 /
        # 0.565 market showed side prices 0.435 and 0.4375).
        prices = [ask, round(1.0 - bid, 6)]
    else:
        prices = [None, None]
    return {
        "id": PREFIX + slug,
        "venue": VERSION,
        "version": VERSION,
        "question": _question(rec),
        "slug": slug,
        "category": rec.get("category"),
        "marketType": rec.get("marketType"),
        "description": rec.get("description") or "",
        "endDate": _iso(end) if end else rec.get("endDate"),
        "venueEndDate": rec.get("endDate"),
        "gameStartTime": rec.get("gameStartTime"),
        "closed": closed,
        "status": rec.get("status"),
        "outcomes": json.dumps([long_.get("description") or "Long",
                                short.get("description") or "Short"]),
        "outcomePrices": json.dumps([p for p in prices if p is not None]
                                    if None not in prices else []),
        "clobTokenIds": [_token(slug, "long"), _token(slug, "short")],
        "feesEnabled": True,
        "feeSchedule": {"rate": fee_theta(rec), "exponent": 1},
        "bestBid": bid,
        "bestAsk": ask,
        "minimumTradeQty": rec.get("minimumTradeQty"),
        # The gateway publishes no 24h volume or liquidity; the scan judges a
        # Polymarket US market by its quoted spread instead.
        "volume24hr": None,
        "liquidityNum": None,
    }


def market(market_id):
    """gamma-shaped record for "pmus:<slug>", with its settlement if any."""
    slug = slug_of(market_id)
    r = pmapi.get_json(f"{GATEWAY}/market/slug/{urllib.parse.quote(slug)}")
    rec = r.get("market") if isinstance(r, dict) else None
    if not rec:
        raise RuntimeError(f"Polymarket US market {slug!r} not found")
    settled = settlement(slug) if rec.get("status") != "MARKET_STATUS_OPEN" else None
    m = normalize(rec, settled)
    if m is None:
        raise RuntimeError(f"Polymarket US market {slug!r} has no usable long/short sides")
    return m


def _levels(rows):
    out = []
    for lvl in rows or []:
        p = _px(lvl.get("px"))
        try:
            q = float(lvl.get("qty"))
        except (TypeError, ValueError):
            continue
        if p is not None and q > 0:
            out.append((p, q))
    return out


def book(token_id):
    """CLOB-shaped book {"bids": [...], "asks": [...]} for one side, with
    string prices and sizes like the international CLOB's, plus
    last_trade_price for that side (or None)."""
    slug, side = _split_token(token_id)
    r = pmapi.get_json(f"{GATEWAY}/markets/{urllib.parse.quote(slug)}/book")
    data = (r or {}).get("marketData") or {}
    bids, offers = _levels(data.get("bids")), _levels(data.get("offers"))
    last = _px(((data.get("stats") or {}).get("lastTradePx")))
    if side == "long":
        b, a = bids, offers
    else:
        b = [(round(1.0 - p, 6), q) for p, q in offers]
        a = [(round(1.0 - p, 6), q) for p, q in bids]
        last = round(1.0 - last, 6) if last is not None else None
    return {
        "asset_id": token_id,
        "bids": [{"price": str(p), "size": str(q)} for p, q in b],
        "asks": [{"price": str(p), "size": str(q)} for p, q in a],
        "state": data.get("state"),
        "last_trade_price": last,
    }


def list_markets(start, end, page_size=500, max_pages=20):
    """Open Polymarket US market records (raw) for events that start, or end,
    between the datetimes start and end. The /markets listing ignores date
    filters and holds 60,000+ markets, so this pages /events, whose
    startTimeMin/Max and endDateMin/Max filters work (checked 2026-11-11), and
    takes the markets embedded in each event, de-duplicated by slug."""
    out, seen = [], set()
    windows = ({"startTimeMin": _iso(start), "startTimeMax": _iso(end)},
               {"endDateMin": _iso(start), "endDateMax": _iso(end)})
    for window in windows:
        for page in range(max_pages):
            r = pmapi.get_json(f"{GATEWAY}/events",
                               dict(window, limit=page_size, offset=page * page_size,
                                    active="true", closed="false"))
            events = (r or {}).get("events") or []
            for ev in events:
                for m in ev.get("markets") or []:
                    if m.get("status") == "MARKET_STATUS_OPEN" and m.get("slug") not in seen:
                        seen.add(m.get("slug"))
                        out.append(m)
            if len(events) < page_size:
                break
    return out
