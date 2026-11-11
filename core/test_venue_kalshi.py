#!/usr/bin/env python3
"""Offline tests for the Kalshi venue (core/venue_kalshi.py) and its dispatch
through core/pmapi.py and core/resolve.py.

Fixtures are trimmed copies of real api.elections.kalshi.com/trade-api/v2
responses read on 2026-11-11. Run: python3 core/test_venue_kalshi.py
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
import venue_kalshi  # noqa: E402

TICKER = "KXITFWMATCH-26NOV11LIUSCH-SCH"
OPEN = {
    "ticker": TICKER, "event_ticker": "KXITFWMATCH-26NOV11LIUSCH",
    "market_type": "binary", "status": "active", "title": "Karlin Schock wins",
    "yes_sub_title": "Karlin Schock", "rules_primary": "If Karlin Schock wins the match, Yes.",
    "close_time": "2026-11-14T03:00:00Z", "expected_expiration_time": "2026-11-12T03:00:00Z",
    "yes_bid_dollars": "0.4100", "yes_ask_dollars": "0.4300",
    "last_price_dollars": "0.4200", "volume_24h_fp": "1500.00", "open_interest_fp": "900.00",
}
TIE = dict(OPEN, ticker="KXURYPDGAME-26NOV12CLAPRO-TIE", event_ticker="KXURYPDGAME-26NOV12CLAPRO",
           title="Tie is the result", yes_sub_title="Tie")
BOOK = {"orderbook_fp": {
    # Resting bids only, price ascending, as Kalshi serves them.
    "yes_dollars": [["0.3900", "27.42"], ["0.4000", "14.13"], ["0.4100", "2.03"]],
    "no_dollars": [["0.5500", "73.44"], ["0.5600", "91.50"], ["0.5700", "28.82"]],
}}
SETTLED_NO = dict(OPEN, status="finalized", result="no", settlement_value_dollars="0.0000",
                  settlement_ts="2026-11-11T23:23:11.252095Z")
SCALAR = dict(OPEN, status="finalized", result="scalar", settlement_value_dollars="0.3300",
              settlement_ts="2026-11-11T21:00:00Z")


def api(market, book=BOOK, fee_multiplier=1):
    def get_json(url, params=None, retries=3, body=None):
        path = url.split("/trade-api/v2", 1)[1]
        if path.startswith("/series/"):
            return {"series": {"fee_multiplier": fee_multiplier, "fee_type": "quadratic"}}
        if path.endswith("/orderbook"):
            return book
        if path.startswith("/markets/"):
            return {"market": market}
        if path == "/markets":
            return {"markets": [market, dict(market, ticker="X-MULTI", market_type="scalar")],
                    "cursor": ""}
        raise AssertionError(f"unexpected url {url}")
    return get_json


class Normalize(unittest.TestCase):
    def setUp(self):
        venue_kalshi.fee_multiplier.cache_clear()

    def test_open_market(self):
        m = venue_kalshi.normalize(OPEN, fee_mult=1.0)
        self.assertEqual(m["id"], "kalshi:" + TICKER)
        self.assertEqual(json.loads(m["outcomes"]), ["Yes", "No"])
        self.assertEqual(json.loads(m["outcomePrices"]), [0.43, 0.59])
        self.assertEqual(m["endDate"], "2026-11-12T03:00:00Z")
        self.assertFalse(m["closed"])
        self.assertTrue(pmapi.tradable(m))
        self.assertEqual(pmapi.token_ids(m), [f"kalshi:{TICKER}:yes", f"kalshi:{TICKER}:no"])

    def test_question_names_the_yes_side(self):
        self.assertEqual(venue_kalshi.normalize(TIE, 1.0)["question"], "Tie is the result")
        m = venue_kalshi.normalize(dict(OPEN, title="Who wins?"), 1.0)
        self.assertEqual(m["question"], "Who wins? [Yes = Karlin Schock]")

    def test_fee_multiplier_from_series(self):
        with mock.patch.object(pmapi, "get_json", api(OPEN, fee_multiplier=2)):
            m = venue_kalshi.normalize(OPEN)
        self.assertAlmostEqual(m["feeSchedule"]["rate"], 0.14)

    def test_non_binary_is_skipped(self):
        self.assertIsNone(venue_kalshi.normalize(dict(OPEN, market_type="scalar"), 1.0))


class Books(unittest.TestCase):
    def setUp(self):
        p = mock.patch.object(pmapi, "get_json", api(OPEN))
        p.start()
        self.addCleanup(p.stop)

    def test_yes_asks_are_no_bids_mirrored(self):
        q = pmapi.book_quote(f"kalshi:{TICKER}:yes")
        self.assertEqual((q["bid"], q["ask"]), (0.41, 0.43))
        self.assertEqual(q["asks"], [(0.43, 28.82), (0.44, 91.5), (0.45, 73.44)])

    def test_no_asks_are_yes_bids_mirrored(self):
        q = pmapi.book_quote(f"kalshi:{TICKER}:no")
        self.assertEqual((q["bid"], q["ask"]), (0.57, 0.59))
        self.assertEqual(q["asks"], [(0.59, 2.03), (0.6, 14.13), (0.61, 27.42)])

    def test_last_trade(self):
        self.assertAlmostEqual(pmapi.last_trade_price(f"kalshi:{TICKER}:yes"), 0.42)
        self.assertAlmostEqual(pmapi.last_trade_price(f"kalshi:{TICKER}:no"), 0.58)

    def test_listing_keeps_binary_only(self):
        start = dt.datetime(2026, 11, 11, tzinfo=dt.timezone.utc)
        got = venue_kalshi.list_markets(start, start + dt.timedelta(days=3))
        self.assertEqual([m["ticker"] for m in got], [TICKER])


class Settle(unittest.TestCase):
    NOW = dt.datetime(2026, 11, 12, 6, 0, tzinfo=dt.timezone.utc)

    def settle(self, market, outcome):
        venue_kalshi.fee_multiplier.cache_clear()
        with mock.patch.object(pmapi, "get_json", api(market)):
            m = pmapi.gamma_market("kalshi:" + market["ticker"])
        row = {"market_id": m["id"], "outcome": outcome, "status": "open",
               "end_date": "2026-11-12T03:00:00Z", "stake_usd": 4.0, "shares": 10.0}
        return resolve.settle_against_market(row, m, self.NOW), row

    def test_no_result(self):
        ok, r = self.settle(SETTLED_NO, "No")
        self.assertTrue(ok)
        self.assertEqual((r["status"], r["pnl_usd"], r["outcome_won"]), ("won", 6.0, "No"))
        self.assertEqual(r["settled_ts"], "2026-11-11T23:23:11Z")
        ok, r = self.settle(SETTLED_NO, "Yes")
        self.assertEqual((r["status"], r["pnl_usd"]), ("lost", -4.0))

    def test_scalar_pays_settled_price_as_void(self):
        ok, r = self.settle(SCALAR, "Yes")
        self.assertTrue(ok)
        self.assertEqual((r["status"], r["pnl_usd"]), ("void", -0.7))   # 10 x 0.33 - 4
        ok, r = self.settle(SCALAR, "No")
        self.assertEqual((r["status"], r["pnl_usd"]), ("void", 2.7))    # 10 x 0.67 - 4

    def test_open_market_stays_open(self):
        ok, r = self.settle(OPEN, "Yes")
        self.assertFalse(ok)
        self.assertEqual(r["status"], "open")

    def test_settled_without_value_stays_open(self):
        ok, r = self.settle(dict(SETTLED_NO, settlement_value_dollars=None), "No")
        self.assertFalse(ok)


class Venue(unittest.TestCase):
    def test_venue_of_and_real_guard(self):
        self.assertEqual(score.venue_of({"market_id": "kalshi:X"}), "kalshi")
        self.assertTrue(pmapi.is_other_venue("kalshi:X"))
        self.assertTrue(pmapi.is_other_venue("pmus:x"))
        self.assertFalse(pmapi.is_other_venue("12345"))


if __name__ == "__main__":
    unittest.main()
