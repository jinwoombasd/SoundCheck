import argparse
import json
import sys
from typing import Sequence

from .file_analyzer import analyze_file


def main(argv: Sequence[str] = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze a speech-focused audio file.")
    parser.add_argument("path", help="Path to a WAV or MP3 file.")
    parser.add_argument("--json", action="store_true", help="Print the full report as JSON.")
    parser.add_argument(
        "--week-1-json",
        action="store_true",
        help="Print report fields mapped to the Week 1 report template as JSON.",
    )
    args = parser.parse_args(argv)

    try:
        report = analyze_file(args.path)
    except (FileNotFoundError, ImportError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
        return 0

    if args.week_1_json:
        print(json.dumps(report.to_week_1_report_fields(), indent=2, sort_keys=True))
        return 0

    metrics = report.metrics
    print(f"File: {report.path}")
    print(f"Duration: {metrics.duration_seconds:.2f}s")
    print(f"Format: {metrics.sample_rate} Hz, {metrics.channels} channel(s)")
    print(f"Level: RMS {metrics.rms_dbfs:.1f} dBFS, peak {metrics.peak_dbfs:.1f} dBFS")
    print(f"Clipping: {metrics.clipping_count} samples ({metrics.clipping_ratio:.4%})")
    print("Findings:")
    for judgment in report.judgments:
        print(f"- {judgment.severity}: {judgment.message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
