"""Kalshi venue adapter (read-only, public data). Stdlib only.

PROTECTED CORE - the trading agent must not edit files under core/.

Kalshi's public market data needs no key (api.elections.kalshi.com/trade-api/v2
answered unsigned requests on 2026-11-11). This module turns Kalshi markets,
order books and settlements into the gamma-shaped records and CLOB-shaped
books the engine already understands, through the dispatch in pmapi.py, the
same way core/venue_pmus.py does for Polymarket US.

Identifiers inside Phil:
  market id  "kalshi:<TICKER>"
  token ids  "kalshi:<TICKER>:yes" and "kalshi:<TICKER>:no"
Outcomes are always ["Yes", "No"]; the market's yes_sub_title is folded into
the question so the agent knows what Yes means.

Order book. GET /markets/<ticker>/orderbook returns resting BIDS only, for each
side (orderbook_fp.yes_dollars, orderbook_fp.no_dollars, price ascending). A
Yes ask at p is a No bid at 1 - p, so the Yes asks are the No bids mirrored and
the No asks are the Yes bids mirrored.

Settlement. A market counts as closed here only when its status is "settled"
or "finalized" AND it carries settlement_value_dollars (Yes payout per
contract); then outcomePrices are [v, 1 - v]. Anything else stays open, so
resolve.py never voids a bet because Kalshi is slow to settle.

When the result is known: expected_expiration_time (the scheduled event), else
close_time. Kalshi's close_time is often days after a game.

Fees (Kalshi fee schedule): taker fee = 0.07 x fee_multiplier x C x p x (1 - p),
rounded up to the cent per order. The series' fee_multiplier is read when the
series is reachable; otherwise 1.
"""
import datetime as dt
import functools
import json
import urllib.parse

import pmapi

API = "https://api.elections.kalshi.com/trade-api/v2"
PREFIX = "kalshi:"
VERSION = "kalshi"
TAKER_THETA = 0.07
SETTLED = {"settled", "finalized"}


def is_market_id(market_id):
    return str(market_id).startswith(PREFIX)


def ticker_of(market_id):
    return str(market_id)[len(PREFIX):]


def _token(ticker, side):
    return f"{PREFIX}{ticker}:{side}"


def _split_token(token_id):
    ticker, _, side = str(token_id)[len(PREFIX):].rpartition(":")
    if side not in ("yes", "no") or not ticker:
        raise ValueError(f"not a Kalshi token id: {token_id!r}")
    return ticker, side


def _f(value):
    try:
        return float(value)
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


def series_of(ticker_or_event):
    return str(ticker_or_event).split("-", 1)[0]


@functools.lru_cache(maxsize=512)
def fee_multiplier(series_ticker):
    try:
        s = pmapi.get_json(f"{API}/series/{urllib.parse.quote(series_ticker)}",
                           retries=1).get("series") or {}
    except RuntimeError:
        return 1.0
    m = _f(s.get("fee_multiplier"))
    return m if m is not None and m > 0 else 1.0


def effective_end(rec):
    return _parse_ts(rec.get("expected_expiration_time")) or _parse_ts(rec.get("close_time"))


def _question(rec):
    title = (rec.get("title") or "").strip()
    yes = (rec.get("yes_sub_title") or "").strip()
    if yes and yes.lower() not in title.lower():
        return f"{title} [Yes = {yes}]"
    return title


def normalize(rec, fee_mult=None):
    """A Kalshi market record as a gamma-shaped dict, or None if unusable."""
    ticker = rec.get("ticker")
    if not ticker or rec.get("market_type", "binary") != "binary":
        return None
    end = effective_end(rec)
    settled_v = _f(rec.get("settlement_value_dollars"))
    closed = rec.get("status") in SETTLED and settled_v is not None
    bid, ask = _f(rec.get("yes_bid_dollars")), _f(rec.get("yes_ask_dollars"))
    if closed:
        prices = [settled_v, round(1.0 - settled_v, 6)]
    elif bid and ask and 0 < bid < ask:
        prices = [ask, round(1.0 - bid, 6)]   # what Yes and No cost to buy now
    else:
        prices = []
    if fee_mult is None:
        fee_mult = fee_multiplier(series_of(rec.get("event_ticker") or ticker))
    return {
        "id": PREFIX + ticker,
        "venue": VERSION,
        "version": VERSION,
        "question": _question(rec),
        "slug": ticker,
        "event_ticker": rec.get("event_ticker"),
        "category": None,
        "description": "\n".join(x for x in (rec.get("rules_primary"),
                                             rec.get("rules_secondary")) if x),
        "endDate": _iso(end) if end else rec.get("close_time"),
        "venueCloseTime": rec.get("close_time"),
        "closed": closed,
        "closedTime": rec.get("settlement_ts") if closed else None,
        "status": rec.get("status"),
        "outcomes": json.dumps(["Yes", "No"]),
        "outcomePrices": json.dumps(prices),
        "clobTokenIds": [_token(ticker, "yes"), _token(ticker, "no")],
        "feesEnabled": True,
        "feeSchedule": {"rate": TAKER_THETA * fee_mult, "exponent": 1},
        "bestBid": bid,
        "bestAsk": ask,
        "volume24hr": _f(rec.get("volume_24h_fp")) or 0.0,
        "liquidityNum": _f(rec.get("open_interest_fp")) or 0.0,
    }


def market(market_id):
    ticker = ticker_of(market_id)
    r = pmapi.get_json(f"{API}/markets/{urllib.parse.quote(ticker)}")
    rec = (r or {}).get("market")
    if not rec:
        raise RuntimeError(f"Kalshi market {ticker!r} not found")
    m = normalize(rec)
    if m is None:
        raise RuntimeError(f"Kalshi market {ticker!r} is not a binary market")
    return m


def _levels(rows):
    out = []
    for row in rows or []:
        try:
            p, q = float(row[0]), float(row[1])
        except (TypeError, ValueError, IndexError):
            continue
        if q > 0:
            out.append((p, q))
    return out


def book(token_id):
    """CLOB-shaped book for one side: its bids are that side's resting bids,
    its asks are the other side's bids mirrored (1 - p), best first."""
    ticker, side = _split_token(token_id)
    r = pmapi.get_json(f"{API}/markets/{urllib.parse.quote(ticker)}/orderbook")
    ob = (r or {}).get("orderbook_fp") or {}
    yes, no = _levels(ob.get("yes_dollars")), _levels(ob.get("no_dollars"))
    own, other = (yes, no) if side == "yes" else (no, yes)
    bids = sorted(own, reverse=True)
    asks = sorted((round(1.0 - p, 6), q) for p, q in other)
    return {
        "asset_id": token_id,
        "bids": [{"price": str(p), "size": str(q)} for p, q in bids],
        "asks": [{"price": str(p), "size": str(q)} for p, q in asks],
        "last_trade_price": None,
    }


def last_trade_price(token_id):
    ticker, side = _split_token(token_id)
    r = pmapi.get_json(f"{API}/markets/{urllib.parse.quote(ticker)}")
    last = _f(((r or {}).get("market") or {}).get("last_price_dollars"))
    if not last:
        return None
    return last if side == "yes" else round(1.0 - last, 6)


def list_markets(start, end, page_size=1000, max_pages=80):
    """Open binary Kalshi markets whose close_time falls between the
    datetimes start and end, combos (multivariate) excluded. A 3-day window
    held 27,000 markets on 2026-11-11 (mostly player props), so up to
    max_pages x page_size are read; the caller filters and caps."""
    out, cursor = [], None
    for _ in range(max_pages):
        params = {"limit": page_size, "status": "open", "mve_filter": "exclude",
                  "min_close_ts": int(start.timestamp()), "max_close_ts": int(end.timestamp())}
        if cursor:
            params["cursor"] = cursor
        r = pmapi.get_json(f"{API}/markets", params)
        out.extend(m for m in (r or {}).get("markets") or []
                   if m.get("market_type", "binary") == "binary")
        cursor = (r or {}).get("cursor")
        if not cursor:
            break
    return out
