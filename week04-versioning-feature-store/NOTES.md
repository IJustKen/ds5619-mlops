# NOTES.md — Week 4: Versioning, Feature Store & Lineage

**Student ID used with `generate_for_student.py`:**
142301038


## v1 vs. v2 manifest comparison

<!-- What's different between the v1 and v2 feature group's manifest.json?
     (Look at both.) -->
The v2 feature group's manifest differs from v1 in its feature_group_version_id and source_raw_version_id; the v2 feature group is registered as new version because it was made from the v2 raw data format. This keeps the history of v1 feature group instead of overwriting it.


## Why treat amount_minor_units differently from amount?

<!-- Why does build_features need to treat amount_minor_units differently
     from amount for the aggregates to be comparable across versions? -->
amount in v1 is already stored in the required currency unit, while amount_minor_units in v2 is in cents. Therefore, amount_minor_units must be divided by 100 since a dollar is 100 cents (before calculating aggregates). 
This converts both versions to the same scale/unit, making sure that features such as average and maximum amount are comparable between v1 & v2.
