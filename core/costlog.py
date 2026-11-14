#!/usr/bin/env python3
"""Record what one cycle cost (operator, 2026-11-14).

PROTECTED CORE - the trading agent must not edit files under core/.

loop.sh runs each cycle with `claude -p --output-format json` and hands the
JSON result here. This appends one row to journal/cycle-costs.jsonl and prints
the session's final text, so the cycle log reads as it did before. The row
holds tokens and list-price dollars per model (Task subagents such as the
haiku screeners included), turns, wall time and web requests. It is the
baseline for "what does a cycle spend", e.g. before and after a playbook trim.

Never blocks a cycle: a missing or unreadable result still exits 0 and writes
a row that says so.

Usage: python3 core/costlog.py --result <file> --model <model> [--why <text>]
"""
import argparse
import datetime as dt
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
COSTS = ROOT / "journal" / "cycle-costs.jsonl"


def summarize(result, model, why, now):
    row = {"ts": now, "model": model, "model_why": why}
    if not isinstance(result, dict):
        row["error"] = "no JSON result (cycle crashed or was killed)"
        return row
    row["cost_usd"] = round(float(result.get("total_cost_usd") or 0.0), 4)
    row["num_turns"] = result.get("num_turns")
    row["duration_min"] = round((result.get("duration_ms") or 0) / 60000, 1)
    row["is_error"] = bool(result.get("is_error"))
    per_model = {}
    for name, u in (result.get("modelUsage") or {}).items():
        if not isinstance(u, dict):
            continue
        per_model[name] = {
            "input": u.get("inputTokens", 0),
            "output": u.get("outputTokens", 0),
            "cache_read": u.get("cacheReadInputTokens", 0),
            "cache_write": u.get("cacheCreationInputTokens", 0),
            "web_search": u.get("webSearchRequests", 0),
            "cost_usd": round(float(u.get("costUSD") or 0.0), 4),
        }
    row["by_model"] = per_model
    row["total_tokens"] = sum(m["input"] + m["output"] + m["cache_read"]
                              + m["cache_write"] for m in per_model.values())
    server = (result.get("usage") or {}).get("server_tool_use") or {}
    row["web_fetch"] = server.get("web_fetch_requests")
    stats = result.get("subagent_stats") or {}
    row["subagents"] = stats.get("spawned")
    return row


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--result", required=True)
    ap.add_argument("--model", default="")
    ap.add_argument("--why", default="")
    ap.add_argument("--out", default=str(COSTS))
    args = ap.parse_args(argv)
    result = None
    try:
        text = pathlib.Path(args.result).read_text()
        result = json.loads(text.strip().splitlines()[-1]) if text.strip() else None
    except (OSError, ValueError, IndexError) as e:
        print(f"costlog: could not read the cycle result: {e}", file=sys.stderr)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = summarize(result, args.model, args.why, now)
    try:
        with open(args.out, "a") as f:
            f.write(json.dumps(row) + "\n")
    except OSError as e:
        print(f"costlog: could not append {args.out}: {e}", file=sys.stderr)
    if isinstance(result, dict) and result.get("result"):
        print(result["result"])
    print(f"costlog: {json.dumps(row)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
