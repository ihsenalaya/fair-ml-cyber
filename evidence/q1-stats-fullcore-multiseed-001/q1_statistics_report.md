# Q1 Robust Statistics Snapshot

This report is generated from verified result CSV files. Bootstrap intervals are over
available experimental units, not over individual flow-level predictions.

## Inputs

- `evidence/fullcore-mem-s42-001/fullcore_mem_s42_results.csv`
- `evidence/fullcore-mem-s7-001/fullcore_mem_s7_results.csv`
- `evidence/fullcore-mem-s99-001/fullcore_mem_s99_results.csv`

Metric: `macro_f1`

## Random vs Stress Paired Comparisons

| model | stress_split | n_pairs | baseline_mean | stress_mean | mean_delta | delta_ci_low | delta_ci_high | mean_ratio | ratio_ci_low | ratio_ci_high | paired_effect_size_dz | sign_flip_p_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting | day_holdout_2017-07-07 | 6 | 0.997726 | 0.409003 | -0.588723 | -0.628146 | -0.548573 | 0.409862 | 0.369667 | 0.4505 | -9.65277 | 0.03125 |
| hist_gradient_boosting | endpoint_pair_holdout | 6 | 0.997726 | 0.992373 | -0.005354 | -0.008902 | -0.002039 | 0.99463 | 0.990553 | 0.99796 | -1.1152 | 0.03125 |
| hist_gradient_boosting | scenario_holdout_Web | 6 | 0.997726 | 0.520677 | -0.477049 | -0.499571 | -0.435273 | 0.521896 | 0.499289 | 0.563371 | -9.45086 | 0.03125 |
| hist_gradient_boosting | temporal | 6 | 0.997726 | 0.231523 | -0.766204 | -0.767428 | -0.765048 | 0.232048 | 0.230681 | 0.233743 | -489.449 | 0.03125 |
| logistic_regression | day_holdout_2017-07-07 | 6 | 0.935677 | 0.639422 | -0.296255 | -0.297961 | -0.294663 | 0.683379 | 0.681675 | 0.685066 | -129.527 | 0.03125 |
| logistic_regression | endpoint_pair_holdout | 6 | 0.935677 | 0.881982 | -0.053695 | -0.06318 | -0.044321 | 0.942616 | 0.932511 | 0.952651 | -4.10128 | 0.03125 |
| logistic_regression | scenario_holdout_Web | 6 | 0.935677 | 0.483113 | -0.452564 | -0.453424 | -0.451558 | 0.516326 | 0.515745 | 0.516983 | -345.031 | 0.03125 |
| logistic_regression | temporal | 6 | 0.935677 | 0.540072 | -0.395605 | -0.396435 | -0.394725 | 0.577199 | 0.576708 | 0.577737 | -333.448 | 0.03125 |

## Inter-Seed Variance

| model | feature_tier | split | n_seeds | mean_across_seeds | inter_seed_std | min_seed_metric | max_seed_metric |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting | deployment_safe | day_holdout_2017-07-07 | 3 | 0.367748 | 0.00015 | 0.367575 | 0.367841 |
| hist_gradient_boosting | deployment_safe | endpoint_pair_holdout | 3 | 0.98869 | 0.00512 | 0.982779 | 0.991709 |
| hist_gradient_boosting | deployment_safe | random_stratified | 3 | 0.995933 | 0.000154 | 0.995756 | 0.996036 |
| hist_gradient_boosting | deployment_safe | scenario_holdout_Web | 3 | 0.538742 | 0.071901 | 0.496886 | 0.621766 |
| hist_gradient_boosting | deployment_safe | temporal | 3 | 0.229766 | 0.00018 | 0.229624 | 0.229968 |
| hist_gradient_boosting | no_identity | day_holdout_2017-07-07 | 3 | 0.450258 | 0.06801 | 0.371741 | 0.490819 |
| hist_gradient_boosting | no_identity | endpoint_pair_holdout | 3 | 0.996055 | 0.004766 | 0.990573 | 0.999208 |
| hist_gradient_boosting | no_identity | random_stratified | 3 | 0.99952 | 5e-05 | 0.999463 | 0.999557 |
| hist_gradient_boosting | no_identity | scenario_holdout_Web | 3 | 0.502612 | 0.005453 | 0.498545 | 0.508809 |
| hist_gradient_boosting | no_identity | temporal | 3 | 0.233279 | 0.002514 | 0.230624 | 0.235623 |
| logistic_regression | deployment_safe | day_holdout_2017-07-07 | 3 | 0.63786 | 0.002154 | 0.635844 | 0.64013 |
| logistic_regression | deployment_safe | endpoint_pair_holdout | 3 | 0.880586 | 0.014319 | 0.864981 | 0.893119 |
| logistic_regression | deployment_safe | random_stratified | 3 | 0.935127 | 0.001671 | 0.933859 | 0.93702 |
| logistic_regression | deployment_safe | scenario_holdout_Web | 3 | 0.482991 | 0.000597 | 0.482302 | 0.483354 |
| logistic_regression | deployment_safe | temporal | 3 | 0.539939 | 0 | 0.539939 | 0.539939 |
| logistic_regression | no_identity | day_holdout_2017-07-07 | 3 | 0.640983 | 0.001003 | 0.639923 | 0.641918 |
| logistic_regression | no_identity | endpoint_pair_holdout | 3 | 0.883379 | 0.01455 | 0.867055 | 0.894983 |
| logistic_regression | no_identity | random_stratified | 3 | 0.936227 | 0.000452 | 0.935718 | 0.93658 |
| logistic_regression | no_identity | scenario_holdout_Web | 3 | 0.483235 | 0.000644 | 0.482832 | 0.483978 |
| logistic_regression | no_identity | temporal | 3 | 0.540205 | 0 | 0.540205 | 0.540205 |

## Bootstrap Metric Summary

| model | feature_tier | split | metric | confidence | bootstrap_iterations | n | mean | std | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting | deployment_safe | day_holdout_2017-07-07 | macro_f1 | 0.95 | 5000 | 3 | 0.367748 | 0.00015 | 0.367575 | 0.367841 |
| hist_gradient_boosting | deployment_safe | endpoint_pair_holdout | macro_f1 | 0.95 | 5000 | 3 | 0.98869 | 0.00512 | 0.982779 | 0.991709 |
| hist_gradient_boosting | deployment_safe | random_stratified | macro_f1 | 0.95 | 5000 | 3 | 0.995933 | 0.000154 | 0.995756 | 0.996036 |
| hist_gradient_boosting | deployment_safe | scenario_holdout_Web | macro_f1 | 0.95 | 5000 | 3 | 0.538742 | 0.071901 | 0.496886 | 0.621766 |
| hist_gradient_boosting | deployment_safe | temporal | macro_f1 | 0.95 | 5000 | 3 | 0.229766 | 0.00018 | 0.229624 | 0.229968 |
| hist_gradient_boosting | no_identity | day_holdout_2017-07-07 | macro_f1 | 0.95 | 5000 | 3 | 0.450258 | 0.06801 | 0.371741 | 0.490819 |
| hist_gradient_boosting | no_identity | endpoint_pair_holdout | macro_f1 | 0.95 | 5000 | 3 | 0.996055 | 0.004766 | 0.990573 | 0.999208 |
| hist_gradient_boosting | no_identity | random_stratified | macro_f1 | 0.95 | 5000 | 3 | 0.99952 | 5e-05 | 0.999463 | 0.999557 |
| hist_gradient_boosting | no_identity | scenario_holdout_Web | macro_f1 | 0.95 | 5000 | 3 | 0.502612 | 0.005453 | 0.498545 | 0.508809 |
| hist_gradient_boosting | no_identity | temporal | macro_f1 | 0.95 | 5000 | 3 | 0.233279 | 0.002514 | 0.230624 | 0.235623 |
| logistic_regression | deployment_safe | day_holdout_2017-07-07 | macro_f1 | 0.95 | 5000 | 3 | 0.63786 | 0.002154 | 0.635844 | 0.64013 |
| logistic_regression | deployment_safe | endpoint_pair_holdout | macro_f1 | 0.95 | 5000 | 3 | 0.880586 | 0.014319 | 0.864981 | 0.893119 |
| logistic_regression | deployment_safe | random_stratified | macro_f1 | 0.95 | 5000 | 3 | 0.935127 | 0.001671 | 0.933859 | 0.93702 |
| logistic_regression | deployment_safe | scenario_holdout_Web | macro_f1 | 0.95 | 5000 | 3 | 0.482991 | 0.000597 | 0.482302 | 0.483354 |
| logistic_regression | deployment_safe | temporal | macro_f1 | 0.95 | 5000 | 3 | 0.539939 | 0 | 0.539939 | 0.539939 |
| logistic_regression | no_identity | day_holdout_2017-07-07 | macro_f1 | 0.95 | 5000 | 3 | 0.640983 | 0.001003 | 0.639923 | 0.641918 |
| logistic_regression | no_identity | endpoint_pair_holdout | macro_f1 | 0.95 | 5000 | 3 | 0.883379 | 0.01455 | 0.867055 | 0.894983 |
| logistic_regression | no_identity | random_stratified | macro_f1 | 0.95 | 5000 | 3 | 0.936227 | 0.000452 | 0.935718 | 0.93658 |
| logistic_regression | no_identity | scenario_holdout_Web | macro_f1 | 0.95 | 5000 | 3 | 0.483235 | 0.000644 | 0.482832 | 0.483978 |
| logistic_regression | no_identity | temporal | macro_f1 | 0.95 | 5000 | 3 | 0.540205 | 0 | 0.540205 | 0.540205 |
