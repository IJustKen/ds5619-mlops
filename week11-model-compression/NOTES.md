# NOTES.md — Week 11: Model Compression Benchmark

**Student ID used with `generate_for_student.py`:**
142301038


## pruned_dense_fp32 vs. pruned_sparse_coo

<!-- Compare pruned_dense_fp32 and pruned_sparse_coo in your report — same
     weights, same accuracy, very different size_bytes. Explain why in your
     own words (tie it to the lecture's pruning pitfall). -->

pruned_dense_fp32 and pruned_sparse_coo evaluate the exact same set of weights where 70% of the parameters have been zeroed out, resulting in identical 99% accuracy (down from 100% baseline). 

Despite having same weights, their storage sizes is quite different: 1024 bytes for dense versus 616 bytes for sparse COO.

Pruning pitfall:
Setting a weight to 0.0 removes its numerical impact on the model, but it does not free the memory allocated to store that weight. A zero stored as a 32-bit float still consumes 4 bytes. As a result, pruned_dense_fp32 pays 256x4 bytes, achieving a 1.0x compression ratio despite "losing" 70% of its weights.

To actually save disk and memory space from  pruning, non-zero values must be extracted and stored in a sparse layout like Coordinate (COO) format. But sparse storage introduces index overhead.

Since the byte cost is getting doubled (8 bytes vs 4 bytes) due to the additional index saved for each weight, sparse COO only becomes a problem when sparsity is less than 50%.

At 70% sparsity this is effective at compression as can be seen with the ratio of compression 1.66.


## The 0.95-sparsity experiment

<!-- Try editing PRUNE_SPARSITY in src/run_pipeline.py to 0.95 and re-run —
     what happens to accuracy, and why does that make sense given only 40
     of the 256 weights are actually informative? -->
Earlier at 0.7, only 0.7*256 weights were removed = 179. Thus the best 77 weights remain, which includes the 40 informative weights. That is why we see accuracy still being near 100% for even the pruned case.

At PRUNE_SPARSITY 0.95 we are removing 0.95*256 weights from the original weights.
That is 243 weights which means only 256-243 = 13 weights survive.

Given that only 40 of the 256 weights are actually informative (large
magnitude, correlated with the label), the other 216 are near-zero noise, we can see why keeping only best 13 surviving weights instead of near 40 causes the accuracy of predictions to change drastically.

It was near 100 for each label before but now plummets to 79% for both pruned cases (dense and sparse).

