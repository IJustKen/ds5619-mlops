# NOTES.md — Week 10: Fairness and Robustness Audit

**Student ID used with `generate_for_student.py`:**
142301038


## Which classes got flagged?

<!-- Which classes got flagged, and does that match what you'd expect given
     how generate_for_student.py built the fixtures? -->
In the clean audit, Two-wheeler (81.82% recall) and Bicycle (89.47% recall) were the only classes flagged below the 90% threshold. This matches what I expected because generate_for_student.py specifically generates smaller bounding boxes for these two classes. Since small objects are structurally harder for detectors to pick up, their lower recall makes sense. Other vehicle classes had enough box area to comfortably pass the threshold.

## If the grouping variable were a protected attribute

<!-- Tying back to the framing note: what would change about this audit's
     stakes and your obligations as an engineer if the grouping variable
     were a protected demographic attribute instead of a vehicle class? -->
If the grouping variable were a protected demographic group like race or gender instead of vehicle classes, the ethical stakes and legal responsibilities would be completely different. Underperforming on a protected group can lead to real-world discrimination, civil rights violations, social harm. As an engineer, I would be legally and morally required to stop deployment, perform root-cause bias mitigation, and ensure continuous fairness monitoring, rather than treating low recall as just a technical performance gap.

## Which attack could corrupt this audit?

<!-- Name one lifecycle stage and attack from the lecture (data poisoning,
     model theft, or adversarial examples) that could silently corrupt THIS
     audit's result, and one control from the lecture that would reduce the
     risk. -->
A data poisoning attack during the data collection or annotation phase could silently corrupt this audit. An attacker could tamper with the validation image fixtures by slightly altering pixel colors or mislabeling bounding boxes, causing the audit to show artificially inflated or deflated recall stats. To prevent this, an MLOps pipeline control like cryptographic dataset hashing (SHA-256) and automated data integrity validation should be used to verify data provenance before running the audit.

## Would SHAP or LIME explain a missed detection?

<!-- Pick one missed ground-truth box in a flagged class. An auditor asks
     you to explain WHY the detector missed it, not just that it did. Would
     SHAP or LIME actually help you answer that for a bounding-box detector
     — and if not, what's different about this detector's inputs/outputs
     that breaks the assumption both tools make? -->
SHAP and LIME would not really help explain why the detector missed a ground-truth box. Both tools are built on the assumption of fixed-dimension classification models that output a set probability score for fixed inputs. Object detectors output a dynamic list of bounding boxes with coordinates and confidence scores. When a box is completely missed (zero IoU overlap), there is no output score or box prediction for SHAP or LIME to attribute feature importance back to, making them unable to explain the missing prediction.

## What did your attack show?

<!-- Using fairness_report.json["adversarial"]: at what eps does each flagged
     class fall further? Which class is most fragile, and is it the same
     class the clean audit flagged? Compare the drop ranking
     (most_fragile) with lowest_recall_under_attack — do they agree, and
     which is the better measure of who is hurt? What does that say about who bears the
     cost of an attack (or of an unmonitored failure)? Then: what would
     adversarial training or input validation look like for this detector,
     and why does a rule this simple break so much more easily than a CNN
     (or does it)? -->
Looking at `fairness_report.json`, both flagged classes fell further as eps increased. Bicycle dropped from 0.8947 at eps=0 down to 0.6842 at eps=10, and Two-wheeler dropped from 0.8182 to 0.7273. At eps=20, Bicycle had the largest recall drop (0.3684 drop, down to 0.5263), making it the most fragile class. This is the same class flagged in the clean audit. 

Comparing the rankings at eps=20, `most_fragile` ranked Bicycle (0.3684 drop), Sedan (0.3636 drop), and Van (0.2857 drop), while `lowest_recall_under_attack` listed Bicycle (0.5263), Two-wheeler (0.6364), and Sedan (0.6364). They do not completely agree because `most_fragile` measures relative loss, whereas `lowest_recall_under_attack` measures absolute remaining performance. `lowest_recall_under_attack` is a better measure of who bears the cost because users in the real world suffer from total missed detections, not just relative drops.

Adversarial training for this model would mean generating perturbed images during testing and tuning color threshold tolerances. Input validation would involve adding a preprocessing step like color normalization or histogram equalization before passing images to the detector. This hand-written rule breaks much easier than a CNN because it relies on hardcoded RGB logic (r > 120 and r - g > 40 and r - b > 40), meaning a tiny channel shift immediately breaks the hard threshold across all pixels, whereas a CNN learns soft spatial feature abstractions.