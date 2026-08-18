"""
Extract -> Validate -> Transform -> Load pipeline for the fraud transaction
data. Run with:

    python src/etl.py --config config.yaml

(a default config.yaml pointing at data/raw_transactions.csv is provided)
"""
import argparse
import csv
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expectations as exp

KNOWN_CATEGORIES = {
    "grocery", "electronics", "fuel", "travel", "restaurant",
    "online_retail", "utilities", "pharmacy", "entertainment", "atm_withdrawal",
}


def build_expectation_suite():
    """The data contract for this dataset. Each entry says which expectation
    function to run, and with what arguments. This is provided — read it to
    know exactly what your expectation functions in expectations.py need to
    handle correctly.
    """
    return [
        (exp.expect_column_not_null, {"column": "amount"}),
        (exp.expect_column_not_null, {"column": "card_id"}),
        (exp.expect_column_positive, {"column": "amount"}),
        (exp.expect_column_in_set, {"column": "merchant_category", "allowed_values": KNOWN_CATEGORIES}),
        (exp.expect_column_unique, {"column": "transaction_id"}),
    ]


def extract(input_path):
    with open(input_path, newline="") as f:
        return list(csv.DictReader(f))


def run_etl(config):
    """Implement the four ETL steps described in ASSIGNMENT.md:
    extract, validate (run every expectation in build_expectation_suite()
    and collect ALL violations, not just the first), transform (split into
    clean vs quarantined rows — a row with ANY violation is quarantined),
    load (write clean_output_path, quarantine_output_path, and
    report_output_path as described in the assignment).

    Return the validation_report dict as well as writing it to disk.
    """
    rows = extract(config["input_path"])

    all_violations = []

    for exp_fn, args in build_expectation_suite():
        violations = exp_fn(rows, **args)
        all_violations.extend(violations)

    quarantined_indices = {v.row_index for v in all_violations}

    clean_rows = []
    quarantined_rows = []

    for i in range(len(rows)):
        if i in quarantined_indices:
            quarantined_rows.append(rows[i])

        else:
            clean_rows.append(rows[i])

    with open(config["clean_output_path"], "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(clean_rows)

    with open(config["quarantine_output_path"], "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(quarantined_rows)

    report = {}

    for violation in all_violations:
        if violation.expectation not in report:
            # first case found
            report[violation.expectation] = {
                "violation_count": 0,
                "row_indices": []
            }
        # else just increment
        report[violation.expectation]["violation_count"] += 1
        report[violation.expectation]["row_indices"].append(violation.row_index)

    with open(config["report_output_path"], "w") as f:
        json.dump(report, f, indent=2)

    print("Wrote to .JSON file")
    
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    report = run_etl(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
