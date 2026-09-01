# NOTES.md — Week 5: Model Registry Governance

**Student ID used with `generate_for_student.py`:**
142301038


## Which candidate reached Production, and why?

Candidate B (v2) reached Production because it satisfied all the Production governance requirements: it had a valid model card and its F1 score was above the required threshold of 0.7


## Gating stale feature data

We would add the feature data's age or last-updated timestamp to the model manifest and check it during Production promotion. 

If the feature data is more than 30 days old, promote_model would raise a GovernanceError and not allow the promotion.


## Scaling the gate to 40 candidates

The design would not need major changes. register_model already assigns each candidate its own version and stores its metrics and metadata, while promote_model applies the same governance checks independently to all versions. 

Thus, 40 candidates can be registered and evaluated using the same functions; only the process that selects the candidates would need to iterate over all 40 models.
