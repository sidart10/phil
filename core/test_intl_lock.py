#!/usr/bin/env python3
"""Offline tests for the international Polymarket venue lock (core/pmapi.py).

PROTECTED CORE - the trading agent must not edit files under core/.

Operator, 2026-11-14: with config/protected.json venues.polymarket.enabled
false, no request may reach gamma, the CLOB or the data API, except one market
or token read for a row already recorded and still open (so it can settle).
Kalshi and Polymarket US requests, soccer and foreign leagues included, are
never refused. Nothing touches the network: urlopen is patched to fail loudly.

Usage: python3 core/test_intl_lock.py
"""
import io
import json
import os
import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import archive  # noqa: E402
import pmapi  # noqa: E402
import watch  # noqa: E402

OPEN_MARKET = "999001"
OPEN_TOKEN = "1234567890"


class FakeResp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def fake_urlopen(req, timeout=None):
    return FakeResp(json.dumps({"ok": True}).encode())


class IntlLock(unittest.TestCase):
    def setUp(self):
        env = mock.patch.dict(os.environ, {"PHIL_TEST_INTL": "",
                                           "PHIL_ALLOW_INTL_READS": ""})
        env.start()
        self.addCleanup(env.stop)
        for target, value in (("intl_enabled", lambda: False),
                              ("recorded_open_intl_ids",
                               lambda: {OPEN_MARKET, OPEN_TOKEN})):
            p = mock.patch.object(pmapi, target, value)
            p.start()
            self.addCleanup(p.stop)
        p = mock.patch("urllib.request.urlopen", fake_urlopen)
        p.start()
        self.addCleanup(p.stop)

    def refused(self, url, body=None):
        return pmapi.intl_request_refusal(url, body)

    def test_listing_and_discovery_are_refused(self):
        for url in (f"{pmapi.GAMMA}/markets?closed=false&limit=100",
                    f"{pmapi.GAMMA}/events/123",
                    f"{pmapi.GAMMA}/tags",
                    f"{pmapi.GAMMA}/markets/keyset?limit=10",
                    f"{pmapi.GAMMA}/markets?id={OPEN_MARKET}",
                    "https://data-api.polymarket.com/trades"):
            self.assertIsNotNone(self.refused(url), url)
        with self.assertRaises(RuntimeError):
            pmapi.gamma_markets(closed="false")
        with self.assertRaises(RuntimeError):
            pmapi.get_json(f"{pmapi.CLOB}/books", body=[{"token_id": OPEN_TOKEN}])

    def test_unrecorded_market_and_token_are_refused(self):
        self.assertIsNotNone(self.refused(f"{pmapi.GAMMA}/markets/555"))
        self.assertIsNotNone(self.refused(f"{pmapi.CLOB}/book?token_id=42"))
        with self.assertRaises(RuntimeError):
            pmapi.gamma_market("555")

    def test_open_recorded_row_can_still_settle(self):
        self.assertIsNone(self.refused(f"{pmapi.GAMMA}/markets/{OPEN_MARKET}"))
        self.assertIsNone(self.refused(f"{pmapi.CLOB}/book?token_id={OPEN_TOKEN}"))
        self.assertEqual(pmapi.gamma_market(OPEN_MARKET), {"ok": True})

    def test_us_venues_never_refused(self):
        for url in ("https://api.elections.kalshi.com/trade-api/v2/markets/KXUCLGAME-26NOV25RMABAY",
                    "https://gateway.polymarket.us/v1/market/slug/epl-ars-che-2026-11-22",
                    "https://xtracker.polymarket.com/user/elonmusk"):
            self.assertIsNone(self.refused(url), url)

    def test_switch_on_or_operator_override_allows(self):
        with mock.patch.object(pmapi, "intl_enabled", lambda: True):
            self.assertIsNone(self.refused(f"{pmapi.GAMMA}/markets?closed=false"))
        with mock.patch.dict(os.environ, {"PHIL_ALLOW_INTL_READS": "1"}):
            self.assertIsNone(self.refused(f"{pmapi.GAMMA}/markets?closed=false"))

    def test_watch_fetch_is_locked(self):
        with self.assertRaises(RuntimeError):
            watch.fetch_json(f"{pmapi.CLOB}/prices-history", {"market": "42"})

    def test_archive_skips_without_requests(self):
        with mock.patch.object(archive, "run",
                               side_effect=AssertionError("archive ran")), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as out:
            self.assertEqual(archive.main([]), 0)
        self.assertIn("skipped", json.loads(out.getvalue()))


class RecordedIds(unittest.TestCase):
    def test_reads_only_open_unprefixed_rows(self):
        ids = pmapi.recorded_open_intl_ids()
        self.assertFalse(any(pmapi.is_other_venue(i) for i in ids))
        root = pathlib.Path(__file__).resolve().parent.parent / "journal"
        rows = [json.loads(line) for line in
                (root / "forecasts.jsonl").read_text().splitlines() if line.strip()]
        settled = {str(r["market_id"]) for r in rows
                   if r.get("status") in ("won", "lost") and ":" not in str(r["market_id"])}
        still_open = {str(r["market_id"]) for r in rows
                      if r.get("status") == "open" and ":" not in str(r["market_id"])}
        self.assertTrue((settled - still_open).isdisjoint(ids))


if __name__ == "__main__":
    unittest.main()
