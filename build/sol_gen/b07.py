import sys
sys.path.insert(0, 'build/sol_gen')
from common import D, save


def SD(goals, data, features, model, evalu, serving, monitoring, followups=()):
    out = ('### Clarify goals and metrics\n' + goals + '\n\n### Data and labels\n' + data + '\n\n### Features\n' + features +
           '\n\n### Model choice\n' + model + '\n\n### Training and evaluation\n' + evalu +
           '\n\n### Serving and latency\n' + serving + '\n\n### Monitoring and failure modes\n' + monitoring + '\n')
    if followups:
        out += '\n### Likely follow-ups\n' + '\n'.join(f'- **{q}** {a}' for q, a in followups) + '\n'
    return out


D['web-ml-122'] = SD(
 'Goal: answer questions from a document collection accurately, with citations, within about 2-3 s. Metrics: retrieval recall@k, answer faithfulness and correctness, citation accuracy, user resolution rate, latency, cost per query.',
 'Ingest documents (PDF, wiki, tickets), parse, clean and chunk (300-500 tokens, overlap, keep headings and metadata such as source, date, ACL). Build an evaluation set of real questions with reference answers and supporting passages.',
 'Chunk embeddings plus BM25 terms; metadata filters (product, date, permissions); query rewriting using conversation history.',
 'Hybrid retrieval (BM25 plus dense bi-encoder), a cross-encoder reranker (top 50 to 5), then an LLM prompted to answer only from the context, cite sources and abstain if the context is insufficient. Fine-tune the embedder or reranker on in-domain click and label data if recall is low.',
 'Offline: retrieval recall@k and MRR, faithfulness (claim-level support), answer correctness with a validated LLM judge plus human spot checks; ablate chunk size and k. Online: A/B on resolution rate, thumbs, escalations.',
 'Vector index (HNSW) with incremental updates; caching of frequent queries; streaming generation; filter by user permissions before retrieval; budget about 300 ms retrieval and the rest for generation.',
 'Failures: stale index, missing permissions, prompt injection in documents, hallucination when retrieval misses. Monitor recall proxy, abstention rate, injection tests, groundedness checks, cost and latency.',
 [('How do you handle updates?', 'Incremental re-embedding on document change with versioning.'),
  ('How to stop leakage across users?', 'Apply ACL filters at retrieval time.'),
  ('What if retrieval fails?', 'Abstain or ask a clarifying question.')])

D['web-ml-123'] = SD(
 'Goal: help blind users navigate indoors safely with spoken guidance. Metrics: obstacle detection recall (safety-critical), false alarm rate, localisation error (metres), task completion, user trust, latency under 200 ms for hazards, battery use.',
 'Collect video and depth/IMU data in diverse buildings with annotations for obstacles, doors, stairs, signs and walkable space; maps (floor plans, BLE beacons) where available. Labels from human annotators plus user-reported feedback.',
 'Camera frames, depth (LiDAR or stereo), IMU, Wi-Fi/BLE signal strengths, floor-plan graph; text from signs via OCR.',
 'On-device detection and segmentation (a lightweight CNN or transformer: object detector plus free-space segmentation), visual-inertial odometry plus map matching for localisation, path planning on a navigation graph, and a speech or haptic interface. Cloud only for non-critical tasks such as scene description with a multimodal model.',
 'Test per hazard class with high recall; indoor navigation trials with blind participants; metrics: collision-free rate, time to destination, localisation error; compare with a cane-only baseline. Safety review and staged rollouts.',
 'Hazard detection on device with quantised models (INT8), 15-30 fps; fallbacks if tracking fails; audio prioritisation (hazards interrupt directions); offline-first.',
 'Failures: poor lighting, glass, crowds, localisation drift, false reassurance. Monitor near-miss reports, per-environment metrics, confidence-based warnings ("I am not sure"), and always keep the user in control.',
 [('Why on-device?', 'Latency and reliability for safety.'),
  ('How to localise without GPS?', 'Visual-inertial odometry with map matching and beacons.'),
  ('What if confidence is low?', 'Warn and slow down guidance.')])

D['web-ml-124'] = SD(
 'Goal: show relevant apps, products or videos to maximise long-term engagement or conversion. Metrics offline: recall@k, NDCG, calibration; online: CTR, conversion, watch time, retention, diversity, guardrails (complaints).',
 'Interaction logs (impressions, clicks, installs, watch time) with timestamps, item metadata, user profile and context. Labels: positive = engagement; negatives from impressions without action plus sampled negatives; correct for position bias.',
 'User: history embeddings, recency and frequency, demographics, device; item: content embedding, category, popularity, freshness, quality; context: time, location, device; cross features.',
 'Two-stage: candidate generation (two-tower retrieval with ANN, plus popularity and collaborative sources) then ranking (gradient boosting or deep multi-task network predicting click, install, dwell) and re-ranking for diversity and policy. Cold start: content-based and exploration.',
 'Time-based splits; metrics NDCG, AUC, calibration; counterfactual evaluation (IPS) where possible; online A/B with guardrails and holdout; long-term effects measured with retention.',
 'Retrieval under 20 ms with a vector index, ranking of about 500 candidates under 50 ms, features from an online feature store, cache popular lists.',
 'Failures: feedback loops, popularity bias, stale features, cold start. Monitor feature drift, calibration by segment, diversity, exposure fairness, and retrain daily.',
 [('How to handle cold start?', 'Content features, exploration with bandits, popularity priors.'),
  ('Why two stages?', 'Cost: cheap retrieval over millions, expensive ranking over hundreds.'),
  ('How to measure long-term value?', 'Holdouts and retention metrics.')])

D['web-ml-125'] = SD(
 'Goal: a recommender that adapts within a session using immediate feedback (clicks, skips) or RL. Metrics: session engagement, reward per session, latency to adapt, regret vs baseline, diversity, safety guardrails.',
 'Streaming events (impressions, clicks, dwell, skips) via a log pipeline; labels computed with delayed windows; propensity of each shown item logged for off-policy evaluation.',
 'Real-time session features (last N items, dwell, current context), long-term user embeddings, item features and freshness, counters updated in a streaming store.',
 'Baseline: a two-stage ranker with session features. For adaptation: contextual bandits (LinUCB, Thompson sampling over ranker scores) for exploration, or sequential models (transformer over the session) trained with RL objectives (policy gradient or Q-learning with slate decomposition) using logged data with importance weighting and conservative regularisation.',
 'Offline policy evaluation: inverse propensity scoring and doubly robust estimators on logged propensities, simulators where available; online A/B with safety constraints and gradual ramp; track long-term retention not just clicks.',
 'Streaming feature updates under seconds, model refresh hourly or daily, a stable fallback policy, exploration rate capped, logging of propensities.',
 'Failures: reward hacking (clickbait), distribution shift from the policy itself, high-variance estimators. Monitor reward vs guardrail metrics, exploration share, and compare with a randomised holdout.',
 [('Why log propensities?', 'Needed for unbiased off-policy evaluation.'),
  ('Bandit versus full RL?', 'Bandits for immediate rewards, RL when actions affect future states.'),
  ('How to stay safe?', 'Constrain the policy near the baseline and ramp gradually.')])

D['web-ml-126'] = SD(
 'Goal: detect fraudulent transactions in real time with low friction. Metrics: recall at a fixed false-positive rate, precision at top-k reviewed, cost-weighted loss (fraud loss versus review and customer friction), latency under 100 ms.',
 'Transaction logs with confirmed fraud labels (delayed by chargebacks days or weeks), disputes, device and network data. Handle extreme imbalance (0.1% fraud), label delay and label noise (undetected fraud labelled legitimate).',
 'Velocity features (transactions per card, device, IP in windows), amount deviation from user history, merchant risk, geo-distance and time since last transaction, device fingerprint, graph features (shared devices, accounts, cards).',
 'Gradient boosted trees on tabular features as the workhorse, plus a graph model or embeddings for rings, and rules for known patterns; anomaly detection for novel attacks. Use cost-sensitive thresholds, calibrated scores and a manual review queue.',
 'Time-based splits with a gap for label delay; PR-AUC and recall at fixed FPR; backtest on past attack waves; shadow mode before launch; A/B with holdout for true loss measurement.',
 'Feature store with streaming aggregates, model scoring under 50 ms, decision engine combining score, rules and thresholds, step-up authentication for medium risk.',
 'Failures: adversaries adapt, concept drift, label delay, bias against groups. Monitor score distribution, alert rates, chargeback rates, retrain often, keep explainability (reason codes) and human review.',
 [('How to handle label delay?', 'Train on matured windows, use proxies for recent data.'),
  ('Why not accuracy?', 'Extreme imbalance.'),
  ('How to detect new fraud types?', 'Anomaly detection and analyst feedback loops.')])

D['web-ml-127'] = SD(
 'Goal: detect near-duplicate videos among billions with high precision and recall at low cost. Metrics: precision and recall of duplicate pairs on labelled sets, index query latency, storage per video, cost.',
 'Collect labelled duplicate pairs (re-uploads, crops, speed changes, watermarks) from user reports and synthetic augmentation of videos; hard negatives are similar but distinct videos.',
 'Frame sampling (1 fps or scene changes), per-frame image embeddings (CNN or ViT, perceptual hashes), audio fingerprints, temporal aggregation (set of frame embeddings or a video-level embedding), metadata (duration, resolution).',
 'Two-stage: fast candidate retrieval with video-level embeddings or locality-sensitive hashing (MinHash or product quantised ANN), then verification by frame-level alignment (temporal matching of frame embedding sequences, dynamic programming) and audio match. Self-supervised contrastive training with augmentations as positives.',
 'Evaluate pair-level precision at a fixed recall on a held-out labelled set, per transformation type (crop, flip, speed); ablate embeddings and thresholds; human review samples. Online: duplicate removal rate and complaint rate.',
 'Offline batch fingerprinting at upload, ANN index sharded by hash, query under 50 ms, verification only for few candidates; incremental indexing and periodic rebuild.',
 'Failures: adversarial edits, false positives on templates or memes, index growth. Monitor precision via audits, index size, latency; allow appeals.',
 [('Why two stages?', 'Cheap retrieval over a huge set, expensive verification on few candidates.'),
  ('How to handle speed changes?', 'Temporal alignment with warping.'),
  ('How to reduce storage?', 'Product quantisation and keyframe sampling.')])

D['web-ml-128'] = SD(
 'Goal: a chatbot that answers questions over both structured (databases) and unstructured (documents) data. Metrics: answer correctness, execution accuracy of generated queries, groundedness, latency, safety (no unauthorised data).',
 'Schema metadata with descriptions and example queries; document corpus with permissions; a set of real questions labelled with expected answers and SQL.',
 'Table and column descriptions, sample values, join graph, glossary of business terms; document chunk embeddings.',
 'A router classifies intent (structured, unstructured, both); text-to-SQL with schema retrieval and few-shot examples, executed read-only with row limits; RAG for documents; an LLM composes the final answer, citing tables and documents. Validate SQL (parse, dry run, permission check) and retry on errors.',
 'Offline: execution accuracy of SQL against ground truth, retrieval recall, answer correctness with human review; red-team for prompt injection and data exfiltration. Online: user feedback and fallback rate.',
 'Cache schema and embeddings, run queries on read replicas with timeouts, stream answers, enforce row-level security using the user identity.',
 'Failures: wrong joins, ambiguous metrics, stale docs, injection. Monitor query errors, empty results, user corrections; ask clarifying questions for ambiguity; log generated SQL for audit.',
 [('How to ensure safety?', 'Read-only, parameterised, permission-scoped queries.'),
  ('How to handle ambiguity?', 'Clarifying questions and a metric glossary.'),
  ('How to evaluate SQL?', 'Execution match on test databases.')])

D['web-ml-129'] = SD(
 'Goal: rank new users or items well with little history. Metrics: performance on cold items and users separately (NDCG, CTR), time to reach steady state, exploration cost.',
 'Identify cold cohorts in logs; use content metadata, onboarding choices and early interactions as labels.',
 'Item content embeddings (text, image, category), creator quality, context features; for users demographics, device, source, onboarding picks.',
 'Content-based tower or two-tower model with content features so new items get embeddings without IDs; popularity and recency priors; meta-learning or feature-based fallbacks; exploration by Thompson sampling or epsilon boosts for new items; blend scores with a confidence weight that shifts to collaborative signals as data accumulates.',
 'Evaluate on temporally held-out new items and users; offline replay for bandits; online A/B tracking cold-start metrics, exploration cost and overall guardrails.',
 'Real-time embedding of new items at upload, slot reservation for exploration, separate counters for early statistics.',
 'Failures: exposure starvation of new items, quality uncertainty, gaming. Monitor cold-item exposure and quality, and cap exploration for low-quality creators.',
 [('Why content features?', 'They do not require interaction history.'),
  ('How to explore?', 'Bandits with a budget.'),
  ('When does cold start end?', 'When collaborative signals are reliable; blend by confidence.')])

D['web-ml-130'] = SD(
 'Goal: multiply large matrices across several GPUs efficiently. Metrics: throughput (FLOPs), scaling efficiency, communication volume, memory per device.',
 'No dataset: inputs are matrices A (m x k) and B (k x n) that exceed one device\'s memory or compute budget.',
 'Partitioning schemes: 1D column or row splits and 2D block (SUMMA) decomposition.',
 'Row split of A (data parallel): each GPU computes A_i B with B replicated; column split of B (tensor parallel): C_j = A B_j then all-gather; split k: C = sum_i A_i B_i then all-reduce or reduce-scatter. 2D SUMMA on a sqrt(p) x sqrt(p) grid broadcasts panels of A along rows and B along columns, reducing memory and communication.',
 'Cost model: compute 2mnk/p FLOPs per GPU; communication of an all-reduce is about 2(p - 1)/p x |C| bytes per GPU (ring). Choose the split that minimises communication given matrix shapes, overlap communication with compute and use NCCL collectives.',
 'Backprop: for C = A B, dA = dC B^T and dB = A^T dC; sharding determines which collectives are needed (for column-sharded B, dA needs an all-reduce).',
 'Failure modes: load imbalance, slow interconnect (use NVLink within nodes), memory spikes. Profile and verify numerics against a single-device result.',
 [('Which split minimises communication?', 'Depends on shapes: communicate the smaller matrix.'),
  ('Why reduce-scatter?', 'It combines reduction and sharding to save memory.'),
  ('What is SUMMA?', 'A 2D algorithm that broadcasts panels to compute blocks.')])

D['web-ml-131'] = SD(
 'Goal: given a client company, find similar companies. Metrics: precision@k against labelled similar pairs (competitors, same industry), analyst acceptance rate, coverage.',
 'Company descriptions, industry codes, products, financials, news, web text, employee skills; labelled pairs from analysts or industry taxonomies; hard negatives from nearby industries.',
 'Text embeddings of descriptions, structured features (size, region, revenue, tech stack), graph features (customers, investors, partners).',
 'Embed each company with a sentence encoder fine-tuned with contrastive learning on known similar pairs, combine with structured features in a two-tower or concatenated embedding, retrieve by ANN (cosine), rerank with a learned model using metadata and business filters.',
 'Hold out company pairs; precision@k and NDCG; analyst review of top 10; ablation of feature groups; check industry and size balance.',
 'Precompute embeddings for all companies, update periodically, ANN index with filters (region, size), return within milliseconds with explanations (shared products, keywords).',
 'Failures: stale descriptions, bias towards large companies, ambiguous categories. Monitor click and accept rates, re-embed on changes, allow user feedback.',
 [('How to evaluate without labels?', 'Use industry taxonomy agreement and expert sampling.'),
  ('How to explain results?', 'Show top shared attributes.'),
  ('How to handle new companies?', 'Embed from description on ingestion.')])

D['web-ml-132'] = SD(
 'Goal: grounded question answering end to end: ingest, retrieve, generate, evaluate. Metrics: recall@k, faithfulness, answer relevance, latency, cost, refusal correctness.',
 'Documents with metadata and permissions; labelled questions with supporting passages and reference answers; production query logs for realistic distribution.',
 'Chunks (semantic or fixed size with overlap), dense embeddings, sparse term vectors, metadata filters, title and section context added to each chunk.',
 'Hybrid retrieval with a reranker, prompt template with citations and abstain rules, a strong instruction-tuned LLM; optional query rewriting, multi-hop retrieval, and fine-tuned embedding and reranker models.',
 'Retrieval: recall@k and nDCG; generation: faithfulness and correctness (LLM judge calibrated to humans); end-to-end: task success. Ablate chunking, k and rerankers; add adversarial and unanswerable questions.',
 'Index with ANN (HNSW), async ingestion, caching, streaming responses; context budget management; fallback to search results if the LLM fails.',
 'Failures: retrieval misses, conflicting sources, prompt injection, stale content. Monitor recall proxies, groundedness, abstentions, feedback; version indexes and prompts.',
 [('How to tune chunk size?', 'Evaluate recall and answer quality across sizes.'),
  ('How to reduce hallucination?', 'Citations, abstention and faithfulness checks.'),
  ('How to scale?', 'Sharded ANN, caching, batching.')])

D['web-ml-133'] = SD(
 'Goal: validate LLM output quality automatically before and after release. Metrics: agreement with human judgments, defect detection recall, regression rate, cost per evaluation.',
 'Curated test sets (golden, adversarial, long tail), human-labelled quality ratings, production samples with feedback.',
 'Rubrics (correctness, helpfulness, safety, format), reference answers, retrieved context for groundedness checks.',
 'A layered system: deterministic checks (format, schema, regex), reference-based metrics where answers are verifiable, LLM judges with rubrics and pairwise comparisons in both orders, NLI-based groundedness, safety classifiers; calibrate judges against human labels and track their bias.',
 'Evaluate judge reliability (kappa, correlation), run regression suites per model or prompt change with confidence intervals, sample production traffic daily, human audit a slice.',
 'Run offline in CI before releases and sampled online continuously; budget with cheap checks first and expensive judges on a subset.',
 'Failures: judge bias (verbosity, position), drift, gaming. Rotate judges, keep human audits, alert on metric drops.',
 [('How to trust LLM judges?', 'Validate against human labels and monitor biases.'),
  ('How to detect regressions?', 'Versioned test suites with paired comparisons.'),
  ('How to control cost?', 'Tiered checks.')])

D['web-ml-134'] = SD(
 'Goal: stable recommendations that handle cold start and are robust to missing signals. Metrics: ranking quality, stability (rank churn between model versions), coverage, behaviour under feature dropout.',
 'Interaction logs plus item and user features; simulate missing features to test robustness.',
 'Content and metadata features for cold start, embedding features, counts with smoothing.',
 'Use feature dropout (randomly masking features or the user history) during training so the model tolerates missing inputs; content-based fallbacks for cold users and items; regularise towards the previous model or ensemble across seeds for stability; calibrate scores.',
 'Compare rank stability across retrains (Kendall tau, top-k overlap), evaluate on cold-start slices and with masked features, A/B test with guardrails.',
 'Feature availability checks with default values and fallbacks, model snapshot versioning and canary deployment.',
 'Failures: sudden quality drops when a feature pipeline breaks, rank flapping that confuses users. Monitor feature null rates, score distributions and churn.',
 [('Why dropout in recommenders?', 'To make the model robust to missing features.'),
  ('How to measure stability?', 'Top-k overlap between versions.'),
  ('How to avoid flapping?', 'Smooth with previous scores or ensembles.')])

D['web-ml-135'] = SD(
 'Goal: find why a model performs worse online than offline. Metrics: offline versus online metric gap, prediction distribution differences, feature parity.',
 'Compare the logged online features and predictions with offline recomputations for the same requests; check experiment assignment logs.',
 'Training-serving skew candidates: different feature code paths, freshness and delays, default values, time-travel leakage in offline data.',
 'Debug checklist: (1) metric definitions and traffic population (same users, same filters); (2) training-serving skew: recompute offline features for logged requests and compare; (3) leakage: features using future information; (4) data freshness and missing features online; (5) distribution shift between the offline split and live traffic; (6) feedback loops and selection bias; (7) objective mismatch (offline AUC versus online business metric); (8) experiment issues (sample ratio mismatch, novelty effects).',
 'Replay logged requests through the offline pipeline, compare score histograms, run time-based validation, evaluate on a shadow deployment, and ablate suspicious features.',
 'Fixes: share feature code between training and serving (feature store), add data validation, retrain on recent data, align offline metric with online goals.',
 'Monitor skew continuously with feature comparison jobs, input null rates and drift alerts.',
 [('What is training-serving skew?', 'Features computed differently in training and production.'),
  ('How to find leakage?', 'Check feature timestamps against the label time.'),
  ('Why can AUC improve but revenue not?', 'Objective mismatch or position bias.')])

D['web-ml-136'] = SD(
 'Goal: detect spam or fraud with high precision to protect users and recall to stop abuse. Metrics: precision, recall at a threshold, false-positive rate on good users, time to detect, cost.',
 'Labelled spam from user reports, moderator decisions and honeypots; heavy imbalance; adversarial drift. Use delayed labels and active learning.',
 'Content features (text embeddings, URLs, patterns), behavioural features (rate, burstiness, account age), graph features (shared devices, IPs), reputation scores.',
 'Layered approach: rules and blocklists for known patterns, a gradient-boosted or text-model classifier for general detection, graph clustering for coordinated rings, and human review for borderline cases. Threshold set by costs.',
 'Time-based splits, precision-recall curves, recall at fixed precision, human audits of positives and negatives, A/B with holdout to measure true impact.',
 'Real-time scoring under 100 ms for inline blocking and batch processing for heavy graph analysis; feature store with streaming aggregates.',
 'Failures: adversarial adaptation, false positives hurting good users, label bias. Monitor precision via audits, retrain frequently, provide appeals.',
 [('How to answer in 15 minutes?', 'Clarify, give data and features, model, metrics, deployment, monitoring.'),
  ('How to handle drift?', 'Frequent retraining and new-pattern detection.'),
  ('How to set the threshold?', 'From cost of false positives versus false negatives.')])

D['web-ml-137'] = SD(
 'Goal: return relevant products for a text query, optimising conversion and revenue. Metrics: NDCG, click-through, add-to-cart, conversion, revenue per search, zero-result rate, latency.',
 'Search logs (queries, impressions, clicks, purchases), catalogue with attributes, relevance judgments from raters; positions bias correction.',
 'Query features (intent, category, spelling), product text and attributes, behavioural features (CTR, sales, price), personalisation, semantic embeddings.',
 'Pipeline: query understanding (spell correction, intent, rewriting), retrieval (inverted index BM25 plus dense retrieval), learning-to-rank (LambdaMART or neural) with relevance and business signals, then re-ranking for diversity, availability and ads.',
 'Offline NDCG with human relevance labels and click-model-debiased labels; online A/B on conversion and revenue; analyse by query segment (head, torso, tail).',
 'Index sharding, caching of popular queries, under 200 ms end-to-end, feature store for fresh inventory and price.',
 'Failures: popularity bias, cold-start products, unavailable items, query drift. Monitor zero-result rate, relevance audits, latency.',
 [('How to handle long-tail queries?', 'Dense retrieval and query rewriting.'),
  ('How to debias clicks?', 'Position-based click models and propensity weighting.'),
  ('How to combine relevance and revenue?', 'Multi-objective ranking with constraints.')])

D['web-ml-138'] = SD(
 'Goal: a RAG assistant that can also call tools (agentic) and has fast, accurate vector search. Metrics: task success, tool-call accuracy, retrieval recall, latency (p95), cost.',
 'Corpus plus tool API specs; traces of correct tool use; evaluation tasks including multi-step ones.',
 'Embeddings for chunks and tool descriptions, metadata, conversation state.',
 'An orchestrator loop (plan, retrieve, call tool, observe, answer) with step limits; function calling with schemas; retrieval via hybrid search and reranking. Optimise vector search: HNSW (high recall, memory heavy) or IVF-PQ (compressed), tune ef_search and nprobe against recall targets, quantise embeddings, shard, and use metadata pre-filtering.',
 'Evaluate end-to-end task success on scenario suites, tool-call precision and recall, retrieval recall@k versus latency curves, regression tests for prompts.',
 'Cache embeddings and frequent queries, parallelise independent tool calls, stream partial answers, set timeouts and retries; keep p95 within the budget.',
 'Failures: tool loops, wrong tool, injection via retrieved text, stale index. Monitor traces, cost per task, tool error rates; require confirmation for side-effecting tools.',
 [('How to trade recall and latency in ANN?', 'Increase ef_search or nprobe until recall plateaus.'),
  ('How to limit agent risk?', 'Least privilege and confirmations.'),
  ('How to reduce cost?', 'Smaller models for routing, caching.')])

D['web-ml-139'] = SD(
 'Goal: infer user intent from typing in real time (for example query completion or action prediction). Metrics: top-k accuracy of the intent, keystrokes saved, latency under 50 ms, acceptance rate.',
 'Logs of partial and final queries or actions, with timestamps and session context; labels are the final submitted intent or action; privacy filters.',
 'Prefix characters, typing speed, previous queries, time, location, user profile, popularity priors.',
 'Candidate generation with a trie or prefix index of popular queries, then a ranker (gradient boosting or a small neural model) over candidates using context; or a lightweight sequence model (char-level transformer or RNN) predicting the intent distribution; combine with personalisation.',
 'Offline MRR and top-k on held-out prefixes; online A/B for acceptance rate and time saved; analyse by prefix length.',
 'On-device or edge caching, tiny models, precomputed prefix tables; strict latency budget under 50 ms; fallback to popular completions.',
 'Failures: offensive or sensitive suggestions, privacy leaks, feedback loops. Filter suggestions, apply differential privacy or aggregation thresholds, monitor.',
 [('How to hit the latency budget?', 'Prefix index plus a small ranker.'),
  ('How to handle privacy?', 'Aggregate and filter rare queries.'),
  ('How to evaluate?', 'MRR offline and acceptance online.')])

D['web-ml-140'] = SD(
 'Goal: recommend restaurants a user will order from. Metrics: order conversion, NDCG, revenue, delivery time satisfaction, diversity, new restaurant exposure.',
 'Order history, impressions and clicks, restaurant metadata (cuisine, price, rating), delivery time and fees; label an order as positive.',
 'User tastes (cuisine affinities), time and weather, location and distance, ETA and fee, restaurant quality and popularity, freshness, embeddings of past orders.',
 'Candidate retrieval by location and open hours, then a multi-task ranker (predict click, order, rating) using gradient boosting or a deep model with embeddings; add exploration for new restaurants and re-ranking for cuisine diversity and delivery constraints.',
 'Time-split offline NDCG and calibration; online A/B on orders per session and revenue with guardrails (delivery time, cancellations).',
 'Geo-sharded retrieval, features from a real-time store (ETA, availability), ranking under 100 ms.',
 'Failures: availability and ETA staleness, popularity bias, cold start. Monitor by city, update ETA features frequently.',
 [('How to include ETA?', 'As a feature and a business constraint in re-ranking.'),
  ('How to handle new restaurants?', 'Exploration and content features.'),
  ('How to avoid homogeneity?', 'Diversity re-ranking.')])

D['web-ml-141'] = SD(
 'Goal: predict arrival time in real time using a grid-based map representation. Metrics: MAE and MAPE of ETA, P90 error, calibration of intervals, latency.',
 'Historical trips (GPS traces, timestamps), map matching to grid cells, traffic and weather, events; labels are actual trip durations; segment-level speeds.',
 'Grid cell traffic speeds by time of day, route cells sequence, distance, number of turns and traffic lights, weather, day type, current real-time speed per cell.',
 'Baseline: sum of segment travel times from historical averages. Improve with a gradient boosting model on route and traffic features, or a sequence/graph neural network over grid cells; model residual over the baseline; produce quantile predictions for uncertainty.',
 'Time-based splits; MAE and P90; evaluate by distance, hour and city; online A/B on ETA accuracy and user satisfaction.',
 'Precompute cell speeds from streaming data (windowed aggregates), query route cells, predict in under 50 ms, cache; fall back to the baseline if data is stale.',
 'Failures: incidents, road closures, sparse cells, GPS noise. Monitor residuals by area, drift in speeds, and update frequently.',
 [('Why a grid?', 'Simple spatial aggregation of traffic that scales.'),
  ('How to give uncertainty?', 'Quantile regression.'),
  ('How to handle sparse cells?', 'Smooth with neighbours and priors.')])

D['web-ml-142'] = SD(
 'Goal: rank a user\'s feed to maximise long-term value (engagement, satisfaction) under integrity constraints. Metrics: time spent, meaningful interactions, retention, diversity, complaint and hide rates.',
 'Impressions with actions (like, comment, share, dwell, hide); negative feedback is critical; labels per action; position bias.',
 'Author-user affinity, post content embeddings, freshness, engagement counts (smoothed), social graph features, context (time, device), user history.',
 'Candidate sources (follows, similar interests, trending), a multi-task ranker predicting several actions with calibrated heads and a value model combining them: score = sum w_a p_a minus penalties, followed by re-ranking for diversity and policy constraints.',
 'Offline per-task AUC and calibration, counterfactual evaluation; online A/B with long-term holdouts and guardrails on integrity; examine heterogeneity.',
 'Retrieval under 30 ms, ranking of thousands of candidates within about 100 ms with cached features, feature freshness through streaming.',
 'Failures: engagement bait, filter bubbles, feedback loops. Monitor diversity, negative feedback, creator fairness and calibrate weights with product teams.',
 [('How to combine objectives?', 'Weighted value model tuned by experiments.'),
  ('Why negative feedback?', 'It signals harm that clicks hide.'),
  ('How to avoid bait?', 'Penalise low-quality signals and measure long-term retention.')])

D['web-ml-143'] = SD(
 'Goal: forecast ad opportunities and pace spend so budgets are used evenly while meeting performance goals. Metrics: delivery vs budget, pacing error, cost per acquisition (CPA), ROI, win rate.',
 'Auction logs (requests, bids, wins, prices, outcomes), historical traffic by hour, campaign configurations, conversion data with delay.',
 'Time of day and day of week, seasonality, predicted CTR and CVR, competition level (win-price distribution), remaining budget, campaign age.',
 'Traffic and win-rate forecasting with time-series models (gradient boosting or sequence models); bid shading from the win-price distribution; pacing controller (PID or model-predictive) adjusting a bid multiplier to track a target spend curve; predicted CVR calibrated for the bid formula: bid = value x pCVR x multiplier.',
 'Backtest with auction simulators on logged data; measure pacing error and CPA versus baseline; online A/B on goal attainment.',
 'Low-latency bidding under 20 ms, real-time spend counters, periodic multiplier updates (minutes).',
 'Failures: traffic shocks, delayed conversions, budget exhaustion early. Monitor pacing curves, add safeguards and alerts.',
 [('What is pacing?', 'Spreading budget across the day to avoid early exhaustion.'),
  ('How to handle delayed conversions?', 'Delay-aware models and conversion windows.'),
  ('What is bid shading?', 'Lowering bids in first-price auctions to avoid overpaying.')])

D['web-ml-144'] = SD(
 'Goal: recommend learning content and infer members\' skills. Metrics: course starts and completions, skill-assessment alignment, job outcomes, precision and recall of skill extraction.',
 'Member profiles, job titles, learning history, content metadata and transcripts, labelled skill annotations, job-skill demand data.',
 'Text embeddings of profiles and content, skill taxonomy features, role and industry, learning history sequences.',
 'Skills inference: NER and entity linking to a taxonomy plus a multi-label classifier from titles and text, with weak supervision from endorsements and assessments. Recommendations: two-tower retrieval (member and content embeddings) followed by a ranker using skill gaps (target role skills minus current skills).',
 'Evaluate skill extraction with precision and recall on labelled data; recommendation NDCG offline; online A/B on completions and long-term outcomes such as skill additions.',
 'Batch skill inference with incremental updates, online ranking in under 100 ms with cached member embeddings.',
 'Failures: taxonomy drift, bias across demographics, sparse profiles. Monitor fairness metrics and coverage.',
 [('How to find skill gaps?', 'Compare inferred skills to role requirements.'),
  ('How to avoid bias?', 'Audit performance across groups.'),
  ('How to handle new content?', 'Content embeddings for cold start.')])

D['web-ml-145'] = SD(
 'Goal: app store search ranking that serves users and advertisers, plus CPA-based ad bidding. Metrics: relevance NDCG, install rate, revenue, advertiser CPA and ROI.',
 'Search logs with taps and installs, app metadata, relevance labels, ad auction logs with install attribution (delayed).',
 'Query-app text match, semantic embeddings, popularity, ratings and retention, install prediction features, user context.',
 'Organic: retrieve with text and dense search, rank with learning-to-rank on relevance and install probability. Ads: predict pInstall with a calibrated model; for CPA bidding, bid = target CPA x pInstall x pacing multiplier; run a generalised second-price or first-price auction with bid shading; mix organic and ads with quality thresholds.',
 'Offline NDCG and calibration of pInstall; counterfactual and auction simulation; online A/B on installs, revenue and advertiser CPA with guardrails for relevance.',
 'Under 100 ms; real-time budgets; features from a store.',
 'Failures: delayed attribution, calibration drift, relevance harm from ads. Monitor calibration by segment and advertiser goal attainment.',
 [('How is CPA bidding computed?', 'Target CPA times predicted conversion probability.'),
  ('Why calibration?', 'Bids depend directly on probabilities.'),
  ('How to protect relevance?', 'Quality gates for ads.')])

D['web-ml-146'] = SD(
 'Goal: compare DCN v1 and v2 for click-through prediction and test the change safely. Metrics: AUC, log loss, calibration, latency, online CTR and revenue.',
 'Impression logs with clicks, sparse categorical and dense features; split by time.',
 'Embeddings for categorical features concatenated with dense features.',
 'DCN v1 cross layer: x_(l+1) = x_0 (x_l^T w_l) + b_l + x_l (rank-one interactions, parameters O(d)). DCN v2: x_(l+1) = x_0 odot (W_l x_l + b_l) + x_l with a full matrix W (or low-rank mixture of experts form), capturing richer explicit feature crosses at higher cost; usually combined with a deep network (stacked or parallel).',
 'Offline: same data and training budget, compare AUC and log loss with multiple seeds and confidence intervals, ablate cross depth and low rank. Online A/B: randomise users, pre-register primary metric (CTR or revenue per mille), guardrails (latency, calibration), power analysis for the minimum detectable effect, run at least a full weekly cycle.',
 'v2 is heavier (matrix per layer), so use low-rank factorisation if latency is tight; check serving cost.',
 'Monitor calibration and subgroup performance; failures from distribution shift and novelty effects.',
 [('How do v1 and v2 differ?', 'v2 uses full or low-rank matrices instead of rank-one crosses.'),
  ('How long to run the A/B?', 'Until planned sample size and a full weekly cycle.'),
  ('How to control cost?', 'Low-rank crosses and distillation.')])

D['web-ml-147'] = SD(
 'Goal: a voice assistant that answers using multimodal retrieval (text, images, tables) and grounds its answers. Metrics: answer accuracy, grounding rate, word error rate (ASR), end-to-end latency, user satisfaction.',
 'Multimodal corpus (documents, images, video transcripts), recorded voice queries with transcripts and gold answers.',
 'Speech features, text and image embeddings in a shared space (CLIP-like), metadata and permissions.',
 'Pipeline: streaming ASR, query understanding and rewriting, multimodal retrieval (text and image embeddings, rerank), an LLM or multimodal model generating a grounded answer with citations, then TTS. Abstain if evidence is insufficient.',
 'Evaluate ASR (WER), retrieval recall across modalities, grounded correctness and citation accuracy, latency budget per stage; human evaluation of spoken answers.',
 'Streaming for low latency, first-token under about 1 s, caches, on-device wake word and ASR when possible.',
 'Failures: ASR errors, hallucinated claims, injection via images or documents. Monitor groundedness and fallback rates; confirm sensitive actions.',
 [('How to ground voice answers?', 'Retrieved evidence with citations and abstention.'),
  ('How to cut latency?', 'Streaming ASR, LLM and TTS.'),
  ('How to retrieve images?', 'Shared text-image embeddings.')])

D['web-ml-148'] = SD(
 'Goal: rank ads by expected value using calibrated click and conversion probabilities. Metrics: log loss, calibration error, AUC, revenue and advertiser value, auction efficiency.',
 'Impressions with click and conversion labels (delay), position, auction context; downsampled negatives require correction.',
 'User, ad and context features, historical CTR and CVR with smoothing, creative embeddings, positions.',
 'Model pCTR and pCVR (DCN, DeepFM, or GBDT) with log loss; calibrate with isotonic or Platt scaling per segment; rank by expected value eCPM = bid x pCTR x pCVR (or value-based formulas) with quality floors.',
 'Reliability diagrams, ECE and log loss by segment, backtests with auction replay; online A/B on revenue and advertiser outcomes.',
 'Scoring under 30 ms, calibration layer in serving, frequent refresh.',
 'Failures: calibration drift under new traffic, position bias, delayed conversions. Monitor calibration continuously, with automated recalibration.',
 [('Why calibration matters?', 'Bids and prices depend on probabilities.'),
  ('How to correct downsampling?', 'Adjust logit by log of the sampling rate.'),
  ('How to model position?', 'Position as a feature during training, set neutral at serving.')])

D['web-ml-149'] = SD(
 'Goal: detect ads selling weapons (policy violation) and rank nearby items or notifications. Metrics: precision and recall of violations (high recall required), reviewer load, notification CTR and opt-out rate.',
 'Policy-labelled ads from reviewers, user reports, text and image examples; hard negatives (toys, replicas, collectibles); notification logs with engagement.',
 'Text and image embeddings, keywords and OCR, seller history, category, price anomalies, context; for ranking: distance, freshness, affinity, time.',
 'Violation detection: multimodal classifier (text plus image) with rules for known keywords, thresholds giving high recall and human review for borderline; active learning from reviews. Ranking: a learned ranker predicting engagement and quality with distance and diversity constraints and frequency capping.',
 'Precision-recall at the policy threshold on fresh data, recall audits on random samples, adversarial testing (obfuscated text); online A/B with notification opt-outs as guardrail.',
 'Real-time pre-publication scoring under 100 ms; asynchronous deeper checks; review queue prioritisation by score.',
 'Failures: adversarial obfuscation, false positives on lawful categories, over-notification. Monitor evasion trends, appeal outcomes and opt-out rates.',
 [('Why favour recall?', 'Missed violations are costly.'),
  ('How to handle evasion?', 'Retrain on adversarial examples and add multimodal signals.'),
  ('How to cap notifications?', 'Frequency limits and opt-out feedback.')])

D['web-ml-150'] = SD(
 'Goal: natural-language Q&A over a data platform (AEP) and a multimodal embedding service. Metrics: query accuracy, answer groundedness, latency, throughput, embedding retrieval recall.',
 'Platform schemas, datasets, documentation, example queries; images and text for embedding training pairs.',
 'Schema and metadata embeddings, query history; for the embedding service: text, image and multimodal pairs.',
 'NL Q&A: intent classification, schema retrieval, text-to-query generation with validation and permission checks, result summarisation by an LLM. Embedding service: a shared text-image model (contrastive), batched GPU inference behind an API with versioning and caching.',
 'Evaluate query execution accuracy, retrieval recall on benchmark pairs, latency and throughput load tests; A/B on user task success.',
 'Autoscaled GPU workers, request batching, embedding cache and ANN index, rate limits, SLAs.',
 'Failures: wrong queries, access leaks, model version drift. Monitor error rates, audit queries, version embeddings with backfill plans.',
 [('How to version embeddings?', 'Store the model version and re-embed in the background.'),
  ('How to batch inference?', 'Dynamic batching with timeouts.'),
  ('How to enforce access?', 'Permission filters in retrieval and queries.')])

D['web-ml-151'] = SD(
 'Goal: detect inputs that differ from training data so predictions can be flagged or deferred. Metrics: AUROC of in-distribution versus OOD detection, false positive rate at 95% true positive, downstream error reduction.',
 'In-distribution training data; OOD sets (other datasets, corruptions, novel classes); real deployment samples flagged by humans.',
 'Model embeddings, logits, feature statistics.',
 'Scores: maximum softmax probability, energy score (-logsumexp of logits), Mahalanobis distance in feature space, kNN distance in embeddings, density models, ensembles or MC dropout for uncertainty, outlier exposure training with auxiliary OOD data.',
 'Evaluate with AUROC and FPR@95 on diverse OOD sets, near-OOD versus far-OOD; calibrate thresholds on validation data; measure selective prediction (accuracy versus coverage).',
 'Compute the score online with the model forward pass; route OOD samples to fallback (human review, conservative model).',
 'Failures: covariate shift that is benign, adversarial inputs, threshold drift. Monitor OOD rate over time, retrain with new data.',
 [('Why not softmax confidence alone?', 'Networks are overconfident on unfamiliar inputs.'),
  ('What is the energy score?', 'Negative log-sum-exp of the logits.'),
  ('How to set the threshold?', 'At a target true positive rate on validation data.')])

D['web-ml-152'] = SD(
 'Goal: predict short-video engagement when data is highly skewed (few viral videos, many with near-zero views). Metrics: ranking metrics (NDCG), calibrated expected watch time, error on log-scale.',
 'View, like, share and watch-time logs; creator and video metadata; heavy-tailed targets; early engagement signals.',
 'Content embeddings (visual, audio, text), creator history, early engagement (first hour views, completion), context.',
 'Model log-transformed targets or use quantile and Tweedie/Poisson-type losses; separate heads for classification (will it reach X views) and regression; handle imbalance with sampling or focal loss; ranking loss for ordering.',
 'Time-based splits; evaluate by popularity decile, NDCG, and quantile calibration; avoid rewarding only head items; A/B on retention and diversity.',
 'Features available at upload for cold start and updated with early signals; low-latency ranking service.',
 'Failures: popularity bias and feedback loops, creators gaming. Monitor exposure fairness and drift.',
 [('Why log transform?', 'Tames heavy tails and stabilises variance.'),
  ('How to handle imbalance?', 'Quantile or focal losses and stratified evaluation.'),
  ('How to avoid popularity bias?', 'Exploration for new videos.')])

D['web-ml-153'] = SD(
 'Goal: find students likely to want a credit card (target audience) from student data, ethically. Metrics: precision at top-k contacted, conversion rate, uplift, complaint and default rates; fairness metrics.',
 'Student demographics, enrolment, spending and campus data where legally permitted; labels from past campaign responses; privacy constraints and consent are critical.',
 'Age, year of study, spending patterns, income proxies (internships), engagement with offers, geographic features; avoid protected attributes and proxies.',
 'Start with a logistic regression or gradient boosting classifier predicting response (or an uplift model predicting incremental response, which is better for budget targeting) plus credit-risk screening so that offers go to students who can repay.',
 'Time-based validation, lift and gain curves, calibration; fairness audits across groups; randomised pilot to measure uplift; compliance review.',
 'Batch scoring, campaign tooling, consent management and opt-out.',
 'Failures: bias, over-indebtedness, privacy breach. Monitor default rates, complaint rates and subgroup outcomes; keep human oversight.',
 [('Response or uplift model?', 'Uplift targets those who change behaviour because of the offer.'),
  ('What are the ethical concerns?', 'Debt risk, privacy and fairness.'),
  ('How to validate?', 'A randomised pilot.')])

D['web-ml-154'] = SD(
 'Goal: estimate the EV-scooter market size (guesstimate) and choose charger locations. Metrics: estimated demand, utilisation per charger, coverage, cost per charge.',
 'Public data (population, commuters, city area), pilot ride data, charging events, points of interest.',
 'Population density, income, public transport gaps, trip origins and destinations, battery use per trip.',
 'Market sizing (top-down): city population 5M, adults 3.5M, those within the target segment and short-trip range 30% = 1.05M, adoption 5% = 52,500 users; riding 4 trips per week of 4 km = 16 km/week, about 0.1 kWh per 4 km, so energy about 0.4 kWh/week per user and 21 MWh/week in total. Charger placement: cluster trip start and end points (k-means or facility location / maximum coverage with a budget), weigh by demand and walking distance, capacity from charging time and battery use.',
 'Validate the estimate with sensitivity analysis (adoption 2% to 10%), compare with comparable cities, and run a pilot; evaluate placement by simulated coverage and utilisation.',
 'Operational: monitor charger utilisation and move assets; iterate placement with real usage.',
 'Risks: adoption uncertainty, regulation, vandalism, grid constraints. Report ranges, not a single number.',
 [('Top-down versus bottom-up?', 'Top-down from population, bottom-up from unit economics and counts.'),
  ('How to place chargers?', 'Maximum coverage over demand clusters under a budget.'),
  ('How to sanity check?', 'Compare with similar markets and per-capita ratios.')])

save('B_08.json')
