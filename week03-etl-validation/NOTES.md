# NOTES.md — Week 3: ETL and Data Validation

**Student ID used with `generate_for_student.py`:**
142301038


## Quarantine count vs. the 7 known injected problems

A total of 6 unique rows ended up being quarantined.

The validation report contains 8 total expectation violations:

expect_column_not_null: 3 violations
expect_column_positive: 3 violations
expect_column_in_set: 1 violation
expect_column_unique: 1 violation

There were 7 known injected problems, but the number of expectation violations is 8 because some rows violate more than one expectation. In particular, rows 535 and 551 violate both expect_column_not_null and expect_column_positive.

Therefore, there are 8 validation violations across 6 unique quarantined rows, rather than exactly 7.
