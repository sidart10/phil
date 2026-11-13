#!/usr/bin/env python3
"""Offline tests for the Polymarket US venue (core/venue_pmus.py) and its
dispatch through core/pmapi.py, core/resolve.py and core/score.py.

The fixtures are trimmed copies of real gateway.polymarket.us/v1 responses
read on 2026-11-11. Run: python3 core/test_venue_pmus.py
"""
import datetime as dt
import json
import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pmapi  # noqa: E402
import resolve  # noqa: E402
import score  # noqa: E402
import venue_pmus  # noqa: E402

SLUG = "aec-nfl-was-nyg-2026-11-12"
GAME = {
    "id": "170001", "slug": SLUG, "status": "MARKET_STATUS_OPEN", "closed": False,
    "question": "Who will win in the upcoming football event Washington Commanders "
                "vs New York Giants scheduled for November 13, 2026 at 1:15 AM UTC?",
    "marketType": "moneyline", "category": "sports",
    "endDate": "2026-11-20T01:15:00Z", "gameStartTime": "2026-11-13T01:15:00Z",
    # Deliberately inconsistent, as /events records are: the short side's
    # price is not 1 - the long bid. normalize() must ignore these.
    "marketSides": [{"description": "Commanders", "long": True, "price": "0.435"},
                    {"description": "Giants", "long": False, "price": "0.4375"}],
    "outcomes": "[\"Giants\",\"Commanders\"]", "outcomePrices": "[\"0.1\",\"0.9\"]",
    "bestBidQuote": {"value": "0.4350", "currency": "USD"},
    "bestAskQuote": {"value": "0.4375", "currency": "USD"},
    "feeCoefficient": 0.095, "minimumTradeQty": 0.01,
}
FUTURE = dict(GAME, slug="tpoyc-2026-zohmam", marketType="futures",
              question="TIME Person of the Year 2026", title="Zohran Mamdani",
              endDate="2027-01-15T04:00:00Z", gameStartTime="2027-01-01T04:59:00Z",
              feeCoefficient=None,
              marketSides=[{"description": "Yes", "long": True, "price": "0.27"},
                           {"description": "No", "long": False, "price": "0.74"}])
BOOK = {"marketData": {
    "marketSlug": SLUG, "state": "MARKET_STATE_OPEN",
    "bids": [{"px": {"value": "0.4350"}, "qty": "100"}, {"px": {"value": "0.4300"}, "qty": "50"}],
    "offers": [{"px": {"value": "0.4375"}, "qty": "80"}, {"px": {"value": "0.4400"}, "qty": "20"}],
    "stats": {"lastTradePx": {"value": "0.4360"}},
}}
RESOLVED = dict(GAME, slug="tsc-cs2-org-fruju-2026-09-24-m2tr-20pt5",
                status="MARKET_STATUS_RESOLVED", marketType="totals",
                marketSides=[{"description": "Over", "long": True, "price": "0"},
                             {"description": "Under", "long": False, "price": "1"}])


def gateway(markets, settlements, books=None):
    """A fake pmapi.get_json serving the gateway routes venue_pmus uses."""
    by_slug = {m["slug"]: m for m in markets}

    def get_json(url, params=None, retries=3, body=None):
        path = url.split("/v1", 1)[1]
        if path.startswith("/market/slug/"):
            return {"market": by_slug[path.rsplit("/", 1)[1]]}
        if path.endswith("/settlement"):
            slug = path.split("/")[2]
            if slug in settlements:
                return {"slug": slug, "settlement": settlements[slug]}
            raise RuntimeError("Settlement not found")
        if path.endswith("/book"):
            return (books or {}).get(path.split("/")[2], BOOK)
        if path == "/events":
            return {"events": [{"markets": markets}]} if params.get("offset") == 0 else {"events": []}
        raise AssertionError(f"unexpected url {url}")
    return get_json


class Normalize(unittest.TestCase):
    def test_game_market(self):
        m = venue_pmus.normalize(GAME)
        self.assertEqual(m["id"], "pmus:" + SLUG)
        self.assertEqual(json.loads(m["outcomes"]), ["Commanders", "Giants"])
        # Long ask, and 1 - long bid for the short side; never the side prices.
        self.assertEqual(json.loads(m["outcomePrices"]), [0.4375, 0.565])
        # Result known 4h after the game starts, not at the venue's endDate.
        self.assertEqual(m["endDate"], "2026-11-13T05:15:00Z")
        self.assertFalse(m["closed"])
        self.assertEqual(m["feeSchedule"], {"rate": 0.095, "exponent": 1})
        self.assertEqual(pmapi.token_ids(m), ["pmus:%s:long" % SLUG, "pmus:%s:short" % SLUG])
        self.assertTrue(pmapi.tradable(m))

    def test_future_uses_end_date_title_and_doc_fee(self):
        m = venue_pmus.normalize(FUTURE)
        self.assertEqual(m["endDate"], "2027-01-15T04:00:00Z")
        self.assertEqual(m["question"], "TIME Person of the Year 2026: Zohran Mamdani")
        self.assertEqual(m["feeSchedule"]["rate"], venue_pmus.DOC_TAKER_THETA)

    def test_unusable_sides(self):
        self.assertIsNone(venue_pmus.normalize(dict(GAME, marketSides=[])))

    def test_settled(self):
        m = venue_pmus.normalize(RESOLVED, settled=0.0)
        self.assertTrue(m["closed"])
        self.assertEqual(json.loads(m["outcomePrices"]), [0.0, 1.0])


class Books(unittest.TestCase):
    def setUp(self):
        p = mock.patch.object(pmapi, "get_json", gateway([GAME], {}))
        p.start()
        self.addCleanup(p.stop)

    def test_long_side_is_the_book(self):
        q = pmapi.book_quote(f"pmus:{SLUG}:long")
        self.assertEqual((q["bid"], q["ask"]), (0.435, 0.4375))
        self.assertEqual(q["asks"], [(0.4375, 80.0), (0.44, 20.0)])

    def test_short_side_mirrors_the_book(self):
        q = pmapi.book_quote(f"pmus:{SLUG}:short")
        self.assertEqual((q["bid"], q["ask"]), (0.5625, 0.565))
        self.assertEqual(q["asks"], [(0.565, 100.0), (0.57, 50.0)])
        self.assertAlmostEqual(pmapi.last_trade_price(f"pmus:{SLUG}:short"), 0.564)

    def test_fee_follows_the_published_formula(self):
        m = venue_pmus.normalize(GAME)
        # theta x p x (1 - p) per contract (docs.polymarket.us/fees).
        self.assertAlmostEqual(pmapi.taker_fee_per_share(m, 0.5), 0.095 * 0.25)

    def test_gamma_market_dispatch(self):
        m = pmapi.gamma_market("pmus:" + SLUG)
        self.assertEqual(m["venue"], "pmus")
        self.assertFalse(m["closed"])

    def test_bad_token(self):
        with self.assertRaises(ValueError):
            pmapi.clob_book("pmus:no-side")


class Settle(unittest.TestCase):
    NOW = dt.datetime(2026, 11, 11, 23, 0, tzinfo=dt.timezone.utc)

    def row(self, outcome, slug=RESOLVED["slug"]):
        return {"market_id": "pmus:" + slug, "outcome": outcome, "status": "open",
                "end_date": "2026-09-25T00:00:00Z", "stake_usd": 5.0, "shares": 10.0}

    def settle(self, row, settlements):
        with mock.patch.object(pmapi, "get_json", gateway([RESOLVED, GAME], settlements)):
            m = pmapi.gamma_market(row["market_id"])
        return resolve.settle_against_market(row, m, self.NOW), row

    def test_short_side_wins_on_zero(self):
        ok, r = self.settle(self.row("Under"), {RESOLVED["slug"]: 0})
        self.assertTrue(ok)
        self.assertEqual((r["status"], r["pnl_usd"], r["outcome_won"]), ("won", 5.0, "Under"))
        ok, r = self.settle(self.row("Over"), {RESOLVED["slug"]: 0})
        self.assertEqual((r["status"], r["pnl_usd"]), ("lost", -5.0))

    def test_split_settlement_pays_half_as_void(self):
        ok, r = self.settle(self.row("Under"), {RESOLVED["slug"]: 0.5})
        self.assertTrue(ok)
        self.assertEqual((r["status"], r["pnl_usd"]), ("void", 0.0))   # 10 x 0.5 - 5

    def test_no_settlement_stays_open_even_long_past_end(self):
        ok, r = self.settle(self.row("Under"), {})
        self.assertFalse(ok)
        self.assertEqual(r["status"], "open")

    def test_open_market_is_never_settled(self):
        ok, r = self.settle(self.row("Giants", slug=SLUG), {SLUG: 1})
        self.assertFalse(ok)


class Listing(unittest.TestCase):
    def test_events_windows_dedupe_and_skip_closed(self):
        closed = dict(GAME, slug="x-closed", status="MARKET_STATUS_RESOLVED")
        start = dt.datetime(2026, 11, 11, tzinfo=dt.timezone.utc)
        with mock.patch.object(pmapi, "get_json", gateway([GAME, FUTURE, closed], {})):
            got = venue_pmus.list_markets(start, start + dt.timedelta(days=3))
        self.assertEqual([m["slug"] for m in got], [SLUG, FUTURE["slug"]])


class Venue(unittest.TestCase):
    def test_venue_of(self):
        self.assertEqual(score.venue_of({"market_id": "pmus:x"}), "pmus")
        self.assertEqual(score.venue_of({"market_id": "123"}), "polymarket")
        self.assertEqual(score.venue_of({"market_id": "123", "venue": "kalshi"}), "kalshi")


class InternationalSwitch(unittest.TestCase):
    """venues.polymarket.enabled = false refuses new international rows only."""

    def test_switched_off_refuses_plain_ids_only(self):
        from unittest import mock
        import os
        with mock.patch.dict(os.environ, {"PHIL_TEST_INTL": ""}), \
                mock.patch.object(pmapi.json, "loads",
                                  return_value={"venues": {"polymarket": {"enabled": False}}}):
            self.assertFalse(pmapi.intl_enabled())
            self.assertIn("switched off", pmapi.refuse_if_switched_off("6990335"))
            self.assertIsNone(pmapi.refuse_if_switched_off("pmus:aec-nba-tor-cha-2026-11-12"))
            self.assertIsNone(pmapi.refuse_if_switched_off("kalshi:KXNBAGAME-26NOV12DALDET-DET"))

    def test_missing_switch_means_on(self):
        from unittest import mock
        import os
        with mock.patch.dict(os.environ, {"PHIL_TEST_INTL": ""}), \
                mock.patch.object(pmapi.json, "loads", return_value={"venues": {}}):
            self.assertTrue(pmapi.intl_enabled())
            self.assertIsNone(pmapi.refuse_if_switched_off("6990335"))


if __name__ == "__main__":
    unittest.main()
