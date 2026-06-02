import argparse
import json
import csv
from collections import Counter
from datetime import datetime


# -----------------------------
# Parse a single log line
# -----------------------------
def parse_log_line(line):
    line = line.strip()

    # Try JSON format first
    try:
        data = json.loads(line)

        return {
            "timestamp": data.get("timestamp"),
            "level": data.get("level"),
            "message": data.get("message")
        }

    except json.JSONDecodeError:
        pass

    # Plain text format
    try:
        parts = line.split(" ", 3)

        timestamp = parts[0] + " " + parts[1]
        level = parts[2]
        message = parts[3]

        return {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }

    except Exception:
        return None


# -----------------------------
# Check if log matches filters
# -----------------------------
def matches_filters(log, level_filter, from_time, to_time):

    # Level filter
    if level_filter:
        if log["level"] != level_filter:
            return False

    # Time filter
    if from_time or to_time:

        try:
            log_time = datetime.strptime(
                log["timestamp"],
                "%Y-%m-%d %H:%M:%S"
            )

            if from_time and log_time < from_time:
                return False

            if to_time and log_time > to_time:
                return False

        except:
            return False

    return True


# -----------------------------
# Export results to CSV
# -----------------------------
def export_to_csv(filename, summary):

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["metric", "value"])

        for key, value in summary.items():
            writer.writerow([key, value])

    print(f"\nSummary exported to {filename}")


# -----------------------------
# Main Program
# -----------------------------
def main():

    parser = argparse.ArgumentParser(
        description="Simple Log Analyzer CLI"
    )

    parser.add_argument(
        "-file",
        required=True,
        help="Path to log file"
    )

    parser.add_argument(
        "--level",
        help="Filter by log level"
    )

    parser.add_argument(
        "--from_time",
        help="Start timestamp (YYYY-MM-DD HH:MM)"
    )

    parser.add_argument(
        "--to_time",
        help="End timestamp (YYYY-MM-DD HH:MM)"
    )

    parser.add_argument(
        "-export",
        help="Export summary to CSV"
    )

    args = parser.parse_args()

    # Convert filter dates
    from_time = None
    to_time = None

    if args.from_time:
        from_time = datetime.strptime(
            args.from_time,
            "%Y-%m-%d %H:%M"
        )

    if args.to_time:
        to_time = datetime.strptime(
            args.to_time,
            "%Y-%m-%d %H:%M"
        )

    # Counters
    errors = 0
    warnings = 0
    info = 0
    total_logs = 0

    error_messages = Counter()
    failure_times = []

    # Read file line by line
    with open(args.file, "r") as file:

        for line_number, line in enumerate(file, start=1):

            print(f"Line {line_number}: {line.strip()}")

            log = parse_log_line(line)

            if not log:
                continue

            if not matches_filters(
                log,
                args.level,
                from_time,
                to_time
            ):
                continue

            total_logs += 1

            level = log["level"]

            if level == "ERROR":
                errors += 1

                error_messages[log["message"]] += 1

                failure_times.append(log["timestamp"])

            elif level == "WARNING":
                warnings += 1

            elif level == "INFO":
                info += 1

    # Most common error
    most_common_error = "None"

    if error_messages:
        most_common_error = error_messages.most_common(1)[0][0]

    # Display results
    print("\n" + "=" * 50)

    print(f"Total logs:          {total_logs}")
    print(f"Errors:              {errors}")
    print(f"Warnings:            {warnings}")
    print(f"Info:                {info}")
    print(f"Most frequent error: {most_common_error}")

    if failure_times:
        print(
            f"Failure timestamps:  {', '.join(failure_times[:10])}"
        )

    # Summary dictionary
    summary = {
        "total_logs": total_logs,
        "errors": errors,
        "warnings": warnings,
        "info": info,
        "most_common_error": most_common_error
    }

    # Export CSV
    if args.export:
        export_to_csv(args.export, summary)


if __name__ == "__main__":
    main()