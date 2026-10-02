import sys
sys.path.insert(0, 'build/sol_gen')
from common import D, T, S, save

D['web-ml-022'] = T(
 'Cross-validation (CV) is a resampling method that estimates generalisation error by training and validating on several different splits. It does not itself reduce bias, variance or the error types of a test; it gives a better estimate of them and enables honest model selection.',
 'It reuses data efficiently: every point is used for validation once and for training K - 1 times. The estimate has its own bias (slightly pessimistic, since each fold trains on less data) and variance.',
 'K-fold CV error = (1/K) sum_k L(model trained without fold k, fold k). Larger K (up to leave-one-out) lowers the estimate\'s bias but raises its variance and cost; K = 5 or 10 is a good compromise. Type I and Type II errors belong to hypothesis tests (false positive and false negative rates); CV does not reduce them, but nested CV with a statistical test (for example a corrected paired t-test) can compare models while controlling them.',
 'With 1000 samples and K = 5, each model trains on 800 points. Variance of the final model is only reduced if you use CV for ensembling or for choosing a regulariser that does so.',
 'Use stratified K-fold for imbalanced classes, grouped K-fold for repeated measures and time-series split for temporal data. Tune hyperparameters inside the inner loop (nested CV) and keep a final test set.',
 [('What is the bias of K-fold?', 'Slightly pessimistic because training sets are smaller; LOO has the least bias.'),
  ('Does CV prevent overfitting?', 'It detects it and guides regularisation but does not remove it.'),
  ('When is CV invalid?', 'When splits leak information (temporal or grouped data).')])

D['web-ml-023'] = T(
 'No single k is guaranteed to maximise leave-one-out (LOO) accuracy of kNN across datasets: the best k depends on the data distribution, noise, dimension and the distance used.',
 'Small k gives flexible, noisy boundaries (low bias, high variance); large k smooths them (high bias, low variance). The LOO accuracy as a function of k is data dependent and often non-monotone.',
 'LOO accuracy(k) = (1/n) sum_i 1[ kNN_k(x_i; data without i) = y_i ]. Counterexample: points of two classes alternating on a line (class A at even positions, B at odd): k = 1 gives LOO accuracy 0 if each point\'s nearest neighbours are the other class, while k = n - 1 gives majority class accuracy near 50%. Another dataset has well-separated clusters where k = 1 is perfect. So no universal k exists.',
 'For two Gaussian blobs with small overlap, k about 5 to 15 maximises LOO accuracy; for XOR-like data the best k may be 1; for very noisy labels larger k is better.',
 'Choose k by cross-validation or LOO on the actual data; use odd k for binary problems to avoid ties; scale features; consider distance weighting. As n grows, the best k grows (k ~ sqrt(n) is a heuristic and k/n -> 0 gives consistency).',
 [('Is k = 1 consistent?', 'No, its error tends to at most twice the Bayes error; k -> infinity with k/n -> 0 is consistent.'),
  ('How does dimension affect k?', 'High dimension makes neighbours less informative, so larger k or dimensionality reduction helps.'),
  ('What about ties?', 'Use odd k or break ties by distance.')])

D['web-ml-024'] = T(
 'Precision is the fraction of predicted positives that are truly positive; recall is the fraction of true positives that are found. Cross-validation estimates both on held-out folds.',
 'Precision answers "when I raise the alarm, am I right?"; recall answers "how many of the real cases do I catch?". Moving the decision threshold trades one for the other.',
 'Precision = TP/(TP + FP); Recall = TP/(TP + FN); F1 = 2PR/(P + R); F-beta weights recall beta^2 times as much. With K-fold CV compute metrics per fold and report the mean and standard deviation, or pool the predictions (pooled precision/recall) and use stratified folds so each fold has positives.',
 'Fraud detection with 0.5% positives: threshold 0.5 gives precision 0.8, recall 0.3; threshold 0.2 gives precision 0.5, recall 0.7. If a missed fraud costs more than a review, favour recall; for spam filtering where false positives are costly, favour precision.',
 'Choose by costs and prevalence; use PR curves for rare positives; report at a fixed operating point (precision at recall 90%). Do not tune the threshold on the test set; choose it by cross-validation.',
 [('Can precision and recall both be 1?', 'Only for a perfect classifier on that data.'),
  ('What if TP + FP = 0?', 'Precision is undefined; define a convention (0 or 1) and report it.'),
  ('Macro versus micro averaging?', 'Macro averages per-class scores equally; micro pools all decisions.')])

D['web-ml-025'] = T(
 'To generate values with given weights, sample from a discrete distribution: the inverse-CDF (cumulative sum) method, the alias method or a library call.',
 'Lay the weights end to end on [0, W); draw a uniform number u in [0, W) and return the item whose segment contains u.',
 'Let prefix[i] = w_1 + ... + w_i. Draw u ~ U(0, W) and find the smallest i with prefix[i] > u by binary search: O(log n) per sample after O(n) preprocessing. The alias method (Walker/Vose) gives O(1) per sample after O(n) preprocessing. Sampling is exact: P(i) = w_i/W.',
 '```python\nimport random, bisect\nfrom itertools import accumulate\n\ndef weighted_sampler(values, weights):\n    prefix = list(accumulate(weights))\n    total = prefix[-1]\n    def draw():\n        u = random.random() * total\n        return values[bisect.bisect_right(prefix, u)]\n    return draw\n\ndraw = weighted_sampler([\'a\', \'b\', \'c\'], [1, 2, 7])\n```\nOver many draws "c" appears about 70% of the time.',
 'Linear scan is fine for few draws; binary search for many draws; alias method for very many draws from a fixed distribution; for streaming data with unknown size use weighted reservoir sampling (key = u^(1/w)).',
 [('How do you handle zero weights?', 'They never get selected because their segment has zero length.'),
  ('Sampling without replacement?', 'Efraimidis-Spirakis keys u^(1/w) and take the top k.'),
  ('What if weights change?', 'Use a Fenwick tree for O(log n) updates and draws.')])

D['web-ml-027'] = T(
 'Two classic tasks: substring search (find whether a pattern occurs in a text) and weighted random sampling (choose items with probability proportional to weights).',
 'Substring search can be done naively in O(nm), with KMP or Z-function in O(n + m), or with rolling hashes (Rabin-Karp) in expected O(n + m). Weighted sampling uses prefix sums and binary search.',
 'KMP: build the failure array pi for the pattern in O(m), then scan the text with it in O(n); matches occur when the matched length reaches m. Rabin-Karp: hash(window) = sum s_i b^(m - i) mod p, update in O(1) with a rolling formula. Weighted sampling: draw u in [0, W), return the first index with prefix sum > u.',
 '```python\ndef kmp_search(text, pat):\n    pi = [0] * len(pat)\n    k = 0\n    for i in range(1, len(pat)):\n        while k and pat[i] != pat[k]:\n            k = pi[k - 1]\n        if pat[i] == pat[k]:\n            k += 1\n        pi[i] = k\n    k = 0\n    for i, ch in enumerate(text):\n        while k and ch != pat[k]:\n            k = pi[k - 1]\n        if ch == pat[k]:\n            k += 1\n        if k == len(pat):\n            return i - k + 1\n    return -1\n```',
 'Naive search is fine for short strings; KMP gives a worst-case guarantee; Rabin-Karp helps with many patterns but has collisions; for sampling, prefix sums with binary search (O(log n)) or the alias method (O(1)).',
 [('Why is KMP linear?', 'The text pointer never moves back and k decreases at most as often as it increases.'),
  ('How do you sample without replacement?', 'Keyed sampling with u^(1/w) and take the top k.'),
  ('How to search many patterns?', 'Aho-Corasick.')])

D['web-ml-028'] = T(
 'To simulate U(0, 1) from fair random bits, build a binary expansion: U = sum_{i >= 1} b_i 2^(-i), where the b_i are independent fair bits.',
 'Each bit decides which half of the remaining interval the number falls in, so k bits pin U down to an interval of length 2^(-k).',
 'With k bits, U_k = sum_{i=1..k} b_i 2^(-i) is uniform on the grid {0, 1/2^k, ..., (2^k - 1)/2^k}, with error below 2^(-k). For doubles, 53 bits give the full mantissa precision. For exact sampling of a threshold event (for example "is U < p?") compare bit by bit with the binary expansion of p and stop at the first difference: expected 2 bits.',
 '```python\nimport random\n\ndef uniform01(bits=53):\n    x = 0\n    for _ in range(bits):\n        x = (x << 1) | random.getrandbits(1)\n    return x / (1 << bits)\n```\nA Bernoulli(p) draw: compare uniform bits with the bits of p.',
 'More bits give finer resolution at linear cost; 53 bits are enough for double precision. Pseudorandom bit sources must be independent and unbiased (if they are biased, apply the von Neumann trick first).',
 [('How would you generate other distributions?', 'Inverse transform: F^(-1)(U).'),
  ('What if the bits are biased?', 'Use the von Neumann extractor (pair 01 -> 0, 10 -> 1, discard others).'),
  ('Is U exactly continuous?', 'No, it is a dyadic rational; the grid shrinks as bits increase.')])

D['web-ml-029'] = T(
 'Estimating a population mean and a conversion rate accurately means using unbiased estimators, quantifying uncertainty with confidence intervals, and controlling for sampling design.',
 'The sample mean is unbiased for the population mean; the conversion rate is a proportion, estimated by successes/trials. Accuracy improves with sample size (standard error ~ 1/sqrt(n)) and with variance reduction.',
 'Mean: x_bar = (1/n) sum x_i, SE = s/sqrt(n), 95% CI x_bar +- t_(0.975, n-1) SE. Conversion rate p_hat = k/n, SE = sqrt(p_hat(1 - p_hat)/n); for small samples use the Wilson or Clopper-Pearson interval. For stratified samples weight by stratum share: sum W_h x_bar_h. Sample size for margin e: n = z^2 p(1 - p)/e^2 (about 385 for e = 5% at p = 0.5).',
 'A/B test: 10,000 visits, 520 conversions: p_hat = 5.2%, SE = 0.22%, 95% CI = [4.77%, 5.63%]. If heavy users are over-represented, reweight by segment or use post-stratification.',
 'Random sampling avoids selection bias; clustering of users needs cluster-robust errors; heavy tails need robust or bootstrap intervals; variance reduction through CUPED or stratification improves precision.',
 [('Why Wilson over normal interval?', 'It behaves better near 0 or 1 and for small n.'),
  ('How to handle outliers in the mean?', 'Trimmed mean, winsorising or bootstrap.'),
  ('Sample size for a 1% margin?', 'About 9,600 at p = 0.5.')])

D['web-ml-030'] = T(
 'Propensity-score matching estimates a treatment effect from observational data by matching treated and untreated units with similar probabilities of receiving treatment given covariates.',
 'In observational data treated and control groups differ in covariates (confounding). The propensity score e(x) = P(T = 1 | X = x) compresses all covariates into a single balancing score; units with the same score are comparable.',
 'Estimate e(x) with logistic regression or gradient boosting; match each treated unit to the nearest control(s) by e(x) within a caliper (for example 0.2 standard deviations of the logit); estimate ATT = mean(Y_treated - Y_matched control). Check covariate balance with standardised mean differences (below 0.1) and overlap of score distributions. Assumptions: unconfoundedness (no hidden confounders) and positivity (0 < e(x) < 1).',
 'Evaluating a loyalty programme: customers who joined differ in spend and tenure. Fit e(x) on those covariates, match 1:1 with a caliper, and compare next-quarter spend; discard unmatched units outside the overlap.',
 'Use when randomisation is impossible and you have rich pre-treatment covariates. Alternatives: inverse probability weighting, doubly robust estimators, regression adjustment, difference-in-differences. It cannot fix unobserved confounding; report sensitivity analyses (Rosenbaum bounds).',
 [('What is the ATT versus ATE?', 'Effect on the treated versus on the whole population.'),
  ('Why not match on all covariates directly?', 'The curse of dimensionality; the score is one-dimensional.'),
  ('How do you check the model?', 'Balance diagnostics after matching, not predictive accuracy of e(x).')])

D['web-ml-031'] = T(
 'Mixed-effects (multilevel) models combine fixed effects (population-level coefficients) with random effects (group-specific deviations) to handle correlated, clustered or repeated-measures data.',
 'Observations from the same user, school or hospital are not independent. Random effects model that shared variation and allow partial pooling: small groups borrow strength from the overall mean.',
 'y_ij = X_ij beta + Z_ij u_j + eps_ij, with u_j ~ N(0, G), eps_ij ~ N(0, sigma^2). The marginal covariance is Z G Z^T + sigma^2 I. Estimation by REML or ML; the intraclass correlation rho = sigma_u^2/(sigma_u^2 + sigma^2) measures clustering. Random slopes let the effect of a covariate vary across groups.',
 'Students nested in schools: score ~ study_hours + (1 + study_hours | school) gives each school its own intercept and slope, shrunk toward the global values. In an A/B test with repeated sessions per user, a random user intercept gives correct standard errors.',
 'Use for repeated measures, hierarchical or longitudinal data, unbalanced groups and when generalising to new groups. Prefer fixed effects when groups are few and of interest themselves, or GEE when you need population-averaged effects. Beware of convergence problems with complex random structures.',
 [('Why not ordinary regression?', 'Ignoring clustering understates standard errors.'),
  ('What is shrinkage?', 'Group estimates are pulled toward the overall mean in proportion to their uncertainty.'),
  ('How many groups do you need?', 'Typically at least 5 to 10 for variance estimates; more is better.')])

D['web-ml-032'] = T(
 'Measuring the causal impact of ads requires comparing outcomes with and without exposure while controlling for who sees the ads; randomised experiments are the gold standard.',
 'People who see ads differ from those who do not (targeting, intent), so naive comparisons are confounded. A holdout group that is eligible but not shown the ad gives the counterfactual.',
 'Randomised lift test: ATE = mean(Y | exposed) - mean(Y | holdout), with a two-sample test and confidence interval; the intent-to-treat effect is diluted by non-exposure, so scale by the exposure rate for the effect on the exposed (Wald/IV estimator). Geo experiments, ghost ads and PSA (placebo) designs reduce cost; difference-in-differences and synthetic control handle regional rollouts; Bayesian structural time series (CausalImpact) estimates the counterfactual from control series.',
 'Randomise 10% of eligible users into holdout for 4 weeks; measure search queries per user for brand terms and conversions; lift = (conv_treat - conv_hold)/conv_hold. Check balance, sample ratio mismatch and novelty effects.',
 'Randomised holdouts are the cleanest; observational methods rely on stronger assumptions (parallel trends, no unobserved confounders). Consider interference (users who talk), long-term effects and ad frequency. Report uncertainty and guardrail metrics.',
 [('Why not compare viewers with non-viewers?', 'Selection bias: viewers are targeted users.'),
  ('What is a ghost ad?', 'Log when the ad would have been shown to control users without showing it.'),
  ('ITT versus treatment on the treated?', 'ITT compares assigned groups; TOT divides by the compliance rate.')])

D['web-ml-033'] = T(
 'To test whether two bird species are segregated (use different areas more than chance predicts), compare the observed spatial association with what independence would give.',
 'If the species are independent, the presence of one at a site tells you nothing about the other; segregation shows up as fewer co-occurrences than expected.',
 'Build a 2 x 2 table over sites: both, only A, only B, neither. Chi-square or Fisher exact test of independence. Expected co-occurrences = n_A n_B / N; the odds ratio or the checkerboard (C-score) index quantifies segregation. For continuous locations, use a Monte Carlo permutation test (shuffle species labels over sites) or a point-pattern cross K-function with a null from random labelling.',
 'N = 100 sites, A present at 40, B at 30. Independence predicts 12 shared sites. Observing 4 shared sites gives a Fisher p-value well below 0.05, indicating segregation. Correct for spatial autocorrelation and habitat effects (include habitat covariates in a logistic regression).',
 'Fisher for small counts, permutation tests when assumptions are doubtful, regression with covariates to separate habitat preference from competition. Multiple comparisons require correction (Bonferroni or FDR).',
 [('Why a permutation test?', 'It builds the null from the data and avoids parametric assumptions.'),
  ('How to separate competition from habitat?', 'Include environment covariates.'),
  ('What if sites are spatially correlated?', 'Use spatial permutation or models with spatial random effects.')])

D['web-ml-034'] = T(
 'Estimating the causal effect of weather on mental health needs a design that separates weather from confounders such as season, location and behaviour.',
 'Weather is not randomly assigned, but day-to-day variation within a place is nearly random with respect to individual traits: that supports a natural experiment.',
 'Panel regression with individual (or location) fixed effects and time controls: Y_it = beta Weather_it + alpha_i + gamma_month + eps_it; beta is identified from within-person weather fluctuations. Alternatives: instrumental variables (for example sunlight at sunrise), distributed-lag models for delayed effects, and difference-in-differences for extreme events. Check for omitted variables (holidays, economy), measurement error and heterogeneity.',
 'Use daily symptom scores from an app linked to local temperature, controlling for person, weekday and month. A coefficient of -0.05 symptom points per 10 C drop in temperature means people feel slightly worse on colder-than-usual days.',
 'Fixed effects remove stable confounders but not time-varying ones; lags capture delayed effects; self-reported outcomes are noisy and selection into the app may bias; report effect sizes with confidence intervals and test robustness.',
 [('Why fixed effects?', 'They remove time-invariant person traits.'),
  ('Association versus causation?', 'Within-person variation supports causal interpretation only under no time-varying confounding.'),
  ('How to handle nonlinearity?', 'Bins or splines for temperature.')])

D['web-ml-035'] = T(
 'To sample uniformly from a disk of radius R, draw the angle uniformly and the radius with density proportional to r, that is r = R sqrt(U).',
 'A naive uniform radius piles points near the centre because rings near the centre have less area. Area grows with r^2, so the CDF of the radius must be r^2/R^2.',
 'Area element dA = r dr dtheta. P(radius <= r) = r^2/R^2, so r = R sqrt(U), U ~ U(0, 1), and theta = 2 pi V, V ~ U(0, 1). Then (x, y) = (r cos theta, r sin theta). Rejection alternative: draw (x, y) uniform in the square [-R, R]^2 and accept if x^2 + y^2 <= R^2 (acceptance pi/4).',
 '```python\nimport math, random\n\ndef sample_disk(R=1.0):\n    r = R * math.sqrt(random.random())\n    t = 2 * math.pi * random.random()\n    return r * math.cos(t), r * math.sin(t)\n```\nCheck: the fraction of samples with radius below R/2 should be 0.25.',
 'The sqrt method needs no rejections and is exact; rejection is simpler but wastes 21% of draws. In 3D use r = R U^(1/3) for a ball, or normalise Gaussian vectors for the sphere surface.',
 [('Why not r = R * U?', 'The density in the plane would be proportional to 1/r.'),
  ('How to sample on the circle itself?', 'Uniform angle only.'),
  ('How to sample inside a sphere?', 'Direction from a normalised Gaussian vector and radius R U^(1/3).')])

D['web-ml-037'] = T(
 'To get a uniform integer on 0 to 6 from a biased coin, first make fair bits (von Neumann trick), then use three fair bits to form a number 0 to 7 and reject 7.',
 'A biased coin with unknown P(H) = p is unfair, but the pair HT and TH are equally likely (p(1 - p) each). Using those pairs as one fair bit removes the bias.',
 'Von Neumann: flip twice; HT -> 0, TH -> 1, otherwise repeat. Probability of a usable pair is 2p(1 - p), so the expected flips per fair bit is 1/(p(1 - p)). Three fair bits give a uniform value in {0,...,7}; if the value is 7, repeat (probability 1/8). Expected number of rounds is 8/7, so the output is exactly uniform on {0,...,6}.',
 '```python\nimport random\n\ndef biased(p=0.8):\n    return random.random() < p\n\ndef fair():\n    while True:\n        a, b = biased(), biased()\n        if a != b:\n            return int(a)\n\ndef uniform7():\n    while True:\n        v = fair() * 4 + fair() * 2 + fair()\n        if v < 7:\n            return v\n```\nSimulation with p = 0.8 gives about 10,000 of each value in 70,000 draws.',
 'This is exact for any unknown p in (0, 1) but wasteful when p is near 0 or 1 (about 1/(p(1 - p)) flips per bit). More efficient extractors (Peres) reuse discarded pairs.',
 [('Why reject 7?', 'Seven outcomes cannot be mapped evenly from eight equally likely values.'),
  ('What if p is known?', 'You could use arithmetic coding for fewer flips.'),
  ('Expected flips?', 'About (8/7) x 3 / (p(1 - p)) x 2 flips.')])

D['web-ml-038'] = T(
 'To test whether two user populations differ, choose a test matched to the metric (mean, proportion, distribution) and its assumptions.',
 'The null hypothesis is that the two populations have the same distribution (or parameter); the test asks whether the observed difference is larger than chance variation.',
 'Means: Welch\'s t-test t = (x1 - x2)/sqrt(s1^2/n1 + s2^2/n2). Proportions: two-proportion z-test z = (p1 - p2)/sqrt(p(1 - p)(1/n1 + 1/n2)) or chi-square. Heavy-tailed data: Mann-Whitney U or bootstrap. Whole distribution: Kolmogorov-Smirnov. Report the effect size and a confidence interval, not just p.',
 'Session lengths for web and mobile users: after checking skew, use a log transform and Welch\'s test or Mann-Whitney; if p = 0.003 and the mean difference is 12 seconds (CI 4-20), the populations differ meaningfully.',
 'Check independence (users appearing in both groups), multiple comparisons across metrics (FDR), and practical significance. For non-randomised populations, differences may reflect confounding; adjust with regression or matching.',
 [('Welch versus Student t-test?', 'Welch does not assume equal variances.'),
  ('When use non-parametric tests?', 'Small samples or strong outliers.'),
  ('What about many metrics?', 'Control the false discovery rate.')])

D['web-ml-039'] = T(
 'A multi-armed bandit repeatedly chooses among actions (arms) with unknown rewards to maximise cumulative reward, balancing exploration and exploitation.',
 'Exploiting the arm that looks best may miss a better one; exploring costs reward now. Bandit algorithms control this trade-off so that regret grows slowly.',
 'Regret R_T = sum_t (mu* - mu_{a_t}). Epsilon-greedy explores with probability epsilon. UCB1 picks argmax mu_hat_a + sqrt(2 ln t/n_a) and has O(log T) regret. Thompson sampling draws a plausible mean from the posterior of each arm (Beta(successes + 1, failures + 1) for Bernoulli rewards) and plays the arm with the largest draw. Contextual bandits (LinUCB) use features to predict each arm\'s reward.',
 'Choosing between three banner designs: Thompson sampling shifts traffic quickly to the best design while still testing the others; compared with a fixed 1/3 split A/B test it loses fewer conversions during the experiment.',
 'Bandits suit continuous optimisation with immediate feedback; A/B tests give cleaner inference for decisions that need unbiased estimates. Delayed rewards, non-stationarity (use discounting or sliding windows) and fairness constraints complicate bandits.',
 [('Why does Thompson sampling work?', 'Uncertain arms have wide posteriors, so they are sampled sometimes.'),
  ('Bandit versus A/B test?', 'Bandits reduce regret; A/B tests give better inference.'),
  ('What is contextual bandit?', 'Arm values depend on context features.')])

D['web-ml-040'] = T(
 'Cross-entropy H(p, q) = -sum p(x) log q(x) measures the expected code length when data from p is encoded with a code optimised for q; KL divergence D_KL(p || q) = sum p log(p/q) is the extra cost over the optimal code.',
 'Cross-entropy equals the entropy of p plus the KL divergence from p to q. Because H(p) does not depend on the model, minimising cross-entropy is the same as minimising KL.',
 'H(p, q) = H(p) + D_KL(p || q). D_KL >= 0 with equality iff p = q (Gibbs inequality) and it is asymmetric. For a one-hot label, H(p, q) = -log q(true class), the usual classification loss. Minimising cross-entropy equals maximum likelihood estimation.',
 'p = (1, 0), q = (0.7, 0.3): H(p, q) = -ln 0.7 = 0.357 nats; since H(p) = 0, KL = 0.357. For p = (0.5, 0.5), q = (0.9, 0.1): KL = 0.5 ln(0.5/0.9) + 0.5 ln(0.5/0.1) = -0.294 + 0.805 = 0.511.',
 'Use cross-entropy as the training loss for classification (smooth, with probabilistic meaning); use KL for matching distributions (VAEs, distillation, policy constraints). KL is asymmetric: forward KL (p || q) is mass-covering, reverse KL (q || p) is mode-seeking.',
 [('Is KL a distance?', 'No: asymmetric and no triangle inequality.'),
  ('Why not squared error for classification?', 'Cross-entropy gives larger gradients for confident errors.'),
  ('What if q(x) = 0 where p(x) > 0?', 'KL is infinite.')])

D['web-ml-041'] = T(
 'To explain and test a gap in completion rates (for example between two groups or versions), first test whether the gap is statistically significant, then investigate mechanisms and confounders.',
 'A difference in completion proportions might be chance, composition (the groups differ in who they contain) or a real effect of the experience.',
 'Two-proportion z-test: z = (p1 - p2)/sqrt(p(1 - p)(1/n1 + 1/n2)), pooled p = (x1 + x2)/(n1 + n2); chi-square or Fisher exact for small counts. Confidence interval for p1 - p2. Adjust for covariates with logistic regression: logit(P(complete)) = a + b Group + c X. Simpson\'s paradox: check segment-level rates.',
 'Completion 62% (n = 5,000) versus 58% (n = 5,200): pooled p = 0.5996, SE = 0.0097, z = 4.1, p < 0.001. Then segment by device and country: if the gap disappears within segments, composition explains it.',
 'Report the absolute gap and its interval, control for confounders, and inspect funnel steps to localise the drop. For randomised variants, the test establishes causality; for observational groups, only association.',
 [('What is Simpson\'s paradox?', 'A trend that reverses when groups are combined or split.'),
  ('How to localise the gap?', 'Step-wise funnel analysis by segment.'),
  ('What sample size is needed?', 'From the power formula for the minimum gap you care about.')])

D['web-ml-042'] = T(
 'A p-value is the probability, assuming the null hypothesis is true, of observing a result at least as extreme as the one seen. In product decisions it signals whether an observed change is likely noise.',
 'A small p-value says the data are surprising under "no effect"; it does not give the probability that the null is true nor the size or importance of the effect.',
 'p = P(T >= t_obs | H0). Decision rule: reject H0 if p < alpha (commonly 0.05), which controls the Type I error rate at alpha. Power = 1 - beta depends on effect size, variance, sample size and alpha. Multiple tests inflate false positives: use Bonferroni or Benjamini-Hochberg.',
 'An experiment shows +0.4% conversion with p = 0.03 and a 95% CI of [0.04%, 0.76%]: statistically significant but tiny; compare with the cost of shipping before deciding. A non-significant result with a wide interval means the experiment was underpowered, not that there is no effect.',
 'Pre-register the metric and sample size, avoid peeking (or use sequential tests), report effect sizes and intervals, consider Bayesian or decision-theoretic framing, and weigh guardrail metrics and practical significance.',
 [('Is p = 0.05 the probability the result is a fluke?', 'No, it is P(data | H0).'),
  ('What is p-hacking?', 'Testing many variations until one is significant.'),
  ('Why use confidence intervals?', 'They show magnitude and uncertainty.')])

D['web-ml-043'] = T(
 'Bayes\' rule updates a prior with evidence: P(A | B) = P(B | A) P(A)/P(B). Forward-pass arithmetic refers to computing a neural network\'s output layer by layer.',
 'Bayes turns "how likely is the evidence given the hypothesis" into "how likely is the hypothesis given the evidence". A forward pass is a chain of matrix products and nonlinearities.',
 'Bayes: P(D | +) = P(+ | D)P(D)/[P(+ | D)P(D) + P(+ | not D)P(not D)]. Example: prevalence 1%, sensitivity 99%, false positive rate 5%: P(D | +) = 0.0099/(0.0099 + 0.0495) = 0.167. Forward pass for one layer: z = W x + b, a = f(z); with x = (1, 2), W = [[0.5, -1], [2, 0.5]], b = (0, 1): z = (0.5 - 2, 2 + 1 + 1) = (-1.5, 4); ReLU gives a = (0, 4).',
 'A diagnostic test with a 1% base rate and a positive result gives only a 16.7% probability of disease: a low prior dominates even for an accurate test.',
 'Bayes shows why base rates matter and underlies naive Bayes classifiers and Bayesian inference; forward-pass arithmetic is the first step in backpropagation checks (compute activations, then gradients with the chain rule).',
 [('What is the posterior if the base rate is 10%?', '0.099/(0.099 + 0.045) = 0.6875.'),
  ('Why is the posterior so low at 1%?', 'False positives from the large healthy group outnumber true positives.'),
  ('How does this relate to naive Bayes?', 'It multiplies likelihoods assuming conditional independence.')])

D['web-ml-044'] = T(
 'A p-test is shorthand for a test that yields a p-value; the t-test compares means using the t distribution when the population variance is unknown; the z-test is for proportions or large samples with known variance.',
 'Each test asks whether the observed difference, measured in standard errors, would be rare under the null.',
 'One-sample t: t = (x_bar - mu_0)/(s/sqrt(n)), df = n - 1. Two-sample (Welch): t = (x1 - x2)/sqrt(s1^2/n1 + s2^2/n2) with Welch-Satterthwaite degrees of freedom. Paired t: t-test on the differences d_i. Proportions: z = (p_hat - p0)/sqrt(p0(1 - p0)/n). Assumptions: independence, approximate normality of the mean (the central limit theorem helps for large n).',
 'Load times before and after an optimisation for the same 30 pages: paired t-test on the differences; mean difference -0.12 s, SD 0.2 s, t = -0.12/(0.2/sqrt(30)) = -3.29, p = 0.003.',
 'Use paired tests for matched data, Welch\'s test by default for unequal variances, non-parametric tests (Mann-Whitney, Wilcoxon) for small or skewed data, and always report an effect size and confidence interval.',
 [('One-tailed or two-tailed?', 'Two-tailed unless you decided on a direction in advance.'),
  ('Why use t not z?', 'The sample variance adds uncertainty, giving heavier tails.'),
  ('What if variances differ?', 'Use Welch.')])

D['web-ml-045'] = T(
 'Queuing problems model arrivals and service, usually with Poisson arrivals and exponential service times (M/M/1), and ask for averages such as waiting time or utilisation; coding versions simulate the queue.',
 'If customers arrive faster than the server can handle, the queue grows without bound; stability requires rho = lambda/mu < 1.',
 'M/M/1 queue: utilisation rho = lambda/mu, mean number in system L = rho/(1 - rho), mean time in system W = 1/(mu - lambda) (Little\'s law L = lambda W), mean waiting in queue W_q = rho/(mu - lambda). Probability the system has n customers: (1 - rho) rho^n.',
 '```python\nimport random\n\ndef simulate_mm1(lam, mu, n=200000):\n    t_arrive = 0.0\n    t_free = 0.0\n    total_wait = 0.0\n    for _ in range(n):\n        t_arrive += random.expovariate(lam)\n        start = max(t_arrive, t_free)\n        total_wait += start - t_arrive\n        t_free = start + random.expovariate(mu)\n    return total_wait / n\n```\nWith lam = 0.8, mu = 1 the theory gives W_q = 0.8/0.2 = 4 time units, and the simulation approaches it.',
 'Simulation handles non-exponential or multi-server cases that have no closed form; use theory for sanity checks. For c servers use the Erlang C formula; for heavy traffic, queues become very sensitive to utilisation near 1.',
 [('What is Little\'s law?', 'L = lambda W for any stable queue.'),
  ('What happens as rho -> 1?', 'Waiting time grows like 1/(1 - rho).'),
  ('What about several servers?', 'M/M/c with Erlang C.')])

D['web-ml-046'] = T(
 'KL divergence D_KL(P || Q) = sum_x P(x) log(P(x)/Q(x)) measures how much information is lost when Q approximates P. It is non-negative and zero only when P = Q.',
 'It is the expected log-likelihood ratio under P: how many extra nats per observation you pay for using the wrong model Q.',
 'Continuous case: integral p log(p/q) dx. Gaussians: KL(N(mu1, s1^2) || N(mu2, s2^2)) = ln(s2/s1) + (s1^2 + (mu1 - mu2)^2)/(2 s2^2) - 1/2. Asymmetry: forward KL (P || Q) forces Q to cover all of P\'s mass; reverse KL is mode-seeking. Jensen-Shannon is a symmetrised, bounded variant.',
 'Applications: VAEs (KL between the posterior and the prior), knowledge distillation (student matches the teacher\'s distribution), RLHF (KL penalty to the reference policy), drift monitoring (feature distribution versus training), variational inference, and model comparison (AIC arises from KL).',
 'Use KL when one distribution is the reference; use JS or Wasserstein when supports differ or a symmetric, finite distance is needed. KL can be infinite when Q(x) = 0 where P(x) > 0; smooth with a small epsilon.',
 [('Is KL symmetric?', 'No.'),
  ('Why does RLHF use KL?', 'To keep the tuned policy close to the base model.'),
  ('What is the KL of two equal Gaussians?', 'Zero.')])

save('B_05.json')
