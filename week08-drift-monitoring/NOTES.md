# NOTES.md — Week 8: Drift and Observability Monitoring

**Student ID used with `generate_for_student.py`:**
142301038


## Drift level vs. expectation

<!-- What drift level did the report show, and does that match what you'd
     expect given the two cameras were built with deliberately different
     visual statistics? -->
The report indicates a "moderate" drift level with a PSI of 0.2489, which sits right on the verge of the "significant" threshold 0.25. 

This aligns well with expectations: changing visual conditions from daylight to low light introduces a clear domain shift that impacts model confidence. Interestingly, while standard summary statistics like the mean (0.9726 vs. 0.9742) make the distributions look nearly identical, PSI captures the underlying bin-level redistribution caused by the darker environment.


## What confidence-score-only monitoring misses

<!-- What would you monitor IN ADDITION to confidence score if you had
     access to ground-truth labels a day later? (Tie this to the kinds of
     drift from the lecture — which one does confidence-score-only
     monitoring miss?) -->

Once we have grouond truth labels, we are enabled to get mAP, Precision, Recall, FPR, etc.

Confidence scores only track Feature Drift or Prediction Drift.

Confidence scores only tell you how sure the model feels, not if the model is actually right.

Confidence-score monitoring misses Concept Drift because a model can be 100% confident while being 100% wrong. Getting ground-truth labels later is the only way to catch this loss of accuracy.
