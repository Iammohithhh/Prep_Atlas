# AI/ML Interview & OA Questions — Web Research (collected 2026-10-01)

Partial report — stopped early on request. Covers late 2024 to Sep 2026.

Caveats:
- **Main source is PracHub** (user-submitted, paraphrased). Date = listing date, not necessarily interview date. Round usually "unknown". Difficulty uses PracHub labels: E-M = Easy/Medium, H = Hard.
- **Glassdoor pages blocked (403).** Items marked *(snippet)* come only from search summaries — unverified.
- **tianpan.co** items are a community forum list — marked *(unverified)*.
- **Thin areas:** research roles; Meesho, Zepto, Dream11, DevRev, PayPal (nothing); Flipkart, Myntra, PhonePe (few); Visa, Mastercard, Axtria, ProcDNA, MAQ, Sigmoid (nothing); Fractal, ZS (snippets only); DE Shaw ML; Samsung SRIB (2021 only).

## Source key
| Key | URL |
|---|---|
| PH-G | https://prachub.com/companies/google/positions/machine-learning-engineer |
| PH-G2 | https://prachub.com/companies/google/positions/machine-learning-engineer?page=2 |
| PH-GDS | https://prachub.com/companies/google/positions/data-scientist |
| PH-AMZ | https://prachub.com/companies/amazon/positions/applied-scientist |
| PH-AMZ2 | https://prachub.com/companies/amazon/positions/applied-scientist?page=2 |
| PH-AMZ-MHA | https://prachub.com/coding-questions/implement-multi-head-attention-from-scratch-in-numpy |
| PH-AMZ-NG | https://prachub.com/interview-experiences/amazon-new-grad-applied-scientist-interview-experience-five-virtual-onsite-rounds-mostly-behavioral-end-in-an-l4-offer |
| PH-MS | https://prachub.com/companies/microsoft/positions/machine-learning-engineer |
| PH-UBER | https://prachub.com/companies/uber/positions/machine-learning-engineer |
| PH-LI | https://prachub.com/companies/linkedin/positions/machine-learning-engineer |
| PH-APPLE | https://prachub.com/companies/apple/positions/machine-learning-engineer |
| PH-META2 | https://prachub.com/companies/meta/positions/machine-learning-engineer?page=2 |
| PH-OAI | https://prachub.com/companies/openai/positions/machine-learning-engineer |
| PH-NV | https://prachub.com/companies/nvidia/positions/machine-learning-engineer |
| PH-ADOBE | https://prachub.com/companies/adobe |
| PH-ML | https://prachub.com/categories/machine-learning |
| EXP-G | https://www.tryexponent.com/guides/google-machine-learning-engineer-interview/experiences |
| EXP-MS | https://www.tryexponent.com/guides/microsoft-applied-scientist-as-interview/experiences |
| TARO-G1 | https://www.jointaro.com/interviews/companies/google/experiences/machine-learning-engineer-india-june-9-2025-no-offer-positive-9b559dc0/ |
| TARO-G2 | https://www.jointaro.com/interviews/companies/google/experiences/machine-learning-engineer-hyderabad-july-31-2025-no-offer-positive-b956ec0a/ |
| TARO-G3 | https://www.jointaro.com/interviews/companies/google/experiences/machine-learning-engineer-india-november-5-2025-no-offer-positive-a24b17b1/ |
| GD-G | https://www.glassdoor.ca/Interview/Google-Interview-E9079-RVW95711844.htm (snippet) |
| GD-AMZ | https://www.glassdoor.com.hk/Interview/Amazon-Interview-E6036-RVW95071021.htm + related Amazon AS reviews (snippet) |
| GD-MS | https://www.glassdoor.com.hk/Interview/Microsoft-Interview-E1651-RVW98981291.htm (snippet) |
| GD-QC | https://static.glassdoor.com.ar/Interview/Qualcomm-Interview-E640-RVW102173524.htm (snippet) |
| GD-ADOBE | https://www.glassdoor.sg/Interview/Adobe-Interview-E1090-RVW94070898.htm (snippet) |
| GD-MYN | https://fr.glassdoor.ca/Entretien/Myntra-Entretien-E508705-RVW99547578.htm (snippet) |
| GD-FK | https://fr.glassdoor.ca/Entretien/Flipkart-Entretien-E300494-RVW91644973.htm (snippet) |
| GD-FRAC | https://www.glassdoor.co.uk/Interview/Fractal-Interview-E270403-RVW101552135.htm (snippet) |
| GD-ZS | https://fr.glassdoor.ca/Entretien/ZS-Associates-Entretien-E115506-RVW98968803.htm (snippet) |
| GD-XAI | https://www.glassdoor.co.uk/Interview/xAI-Interview-E10404667-RVW99846515.htm (snippet) |
| GD-ANT | https://static.glassdoor.ie/Interview/Anthropic-Research-Engineer-Scientist-Interview-Questions-EI_IE8109027.0,9_KO10,37.htm (snippet) |
| BL-SARVAM | https://www.teamblind.com/post/sarvams-ai-interviews-have-no-dsa-and-still-offered-84-lpa-instead-l86l5tp0 |
| BL-MSI | https://www.teamblind.com/post/interview-experience-data-applied-scientist-at-microsoft-india-dws5kt7x (Apr 2022, older) |
| LC-PP | https://leetcode.com/discuss/interview-experience/7087077 |
| IITK-HL | https://spo.iitk.ac.in/insights/2024-placement-abu-kashan-hilabs |
| TP-OAI | https://tianpan.co/forum/t/collecting-openai-interview-questions-2025-edition-share-your-experience/38 (unverified) |
| TI-TF | https://www.techinterview.org/post/3233476821/what-llm-interviewers-ask-about-transformers/ |
| IQ-UBER | https://interviewquery.com/interview-guides/uber-machine-learning-engineer |

---

## Trends
1. **Meta AI-assisted coding rounds** (pilot from Jul 2025): one AI-enabled round + one normal coding round at E6 and below; multi-file, test-driven tasks. [BusinessToday](https://www.businesstoday.in/amp/technology/news/story/meta-to-test-job-applicants-with-ai-assisted-coding-interviews-amid-ai-expansion-plans-487200-2025-07-31), [Hello Interview](https://hellointerview.com/blog/meta-ai-enabled-coding)
2. **Canva replaced its CS-fundamentals round with a mandatory AI-assisted coding round** for backend, frontend and ML (Jun 2025). [Canva](https://canva.dev/blog/engineering/yes-you-can-use-ai-in-our-interviews)
3. **Backlash against AI cheating:** Google bringing back in-person rounds; Amazon makes candidates declare no AI; Anthropic banned AI in interviews (2025). Expect proctored OAs. [Storyboard18](https://www.storyboard18.com/brand-makers/google-to-reintroduce-in-person-interviews-amid-rising-ai-cheating-concerns-79624.htm)
4. **ML system design is shifting from "design a recsys" to LLM-application architecture** (RAG, enterprise search, support assistants, eval pipelines, cost/latency). [techinterview.org Jul 2026](https://www.techinterview.org/post/3233474925/ml-engineer-interview-post-llm-era/); PracHub shows the same at Microsoft, Apple, Amazon, OpenAI, Adobe.
5. **Higher bar for from-scratch ML coding:** CNN from scratch went from "hard" (2023) to "entry-level" (2025); attention, KV cache, LoRA, DPO, GRPO now appear. [Reddit snapshot Jun 2026](https://reddit.sentinel-team.org/posts/1u0dz2w/snapshots/2026-06-10T03%3A09%3A11.31048Z); [TorchLeet](https://github.com/Exorust/TorchLeet)
6. **"Debug this ML code" rounds:** OpenAI broken MiniGPT + add KV cache; LinkedIn broken logistic-regression training (2025–26).
7. **Post-training / RL alignment theory spreading beyond frontier labs:** GRPO vs PPO, SFT/DPO/PPO with KL, reward hacking, importance sampling (Siemens, Google, Amazon, 2026).
8. **LLM evaluation and label quality as its own topic:** annotator agreement, LLM-as-judge (Apple), noisy annotators (OpenAI), LLM quality validation (Amazon AS).
9. **Classical ML still matters**, especially Uber/LinkedIn and Amazon AS breadth: bias-variance, bagging vs boosting, XGBoost, calibration, K-means convergence.
10. **Probability tested as code:** weighted sampling, uniform from biased coin, Uniform(0,1) from bits, sampling in a circle (Google, LinkedIn).
11. **Indian GenAI startups skip DSA:** Sarvam (Jul 2026) — 2.5 h onsite building a voice-activity detector, then gradient descent from scratch, self-attention, speech latent-space decomposition. BL-SARVAM
12. **Indian analytics firms now ask GenAI:** Fractal asks RAG, vector DBs, embeddings, agent frameworks alongside Python/SQL. GD-FRAC (snippet)
13. **Amazon AS loops still heavy on Leadership Principles:** Aug 2025 new-grad L4 — 5 rounds, mostly behavioural, ML design in 15–30 min segments. PH-AMZ-NG
14. **Typical Indian campus DS/ML loop:** CPI cutoff → OA → DSA round (two-pointer / binary search) → ML basics + case study → HR (HiLabs, IITK 2024). IITK-HL

---

## Questions

### 1. ML theory / conceptual
| # | Question | Company | Role | Round | Diff | Src | Date |
|---|---|---|---|---|---|---|---|
| 1 | Bias-variance; how to evaluate a classifier | Microsoft | MLE | unknown | E-M | PH-MS | Dec 2025 |
| 2 | Metrics, regularisation, ablation studies | Microsoft | MLE | unknown | E-M | PH-MS | Feb 2026 |
| 3 | How do you choose a model for a problem? | Microsoft | MLE | unknown | E-M | PH-MS | Mar 2026 |
| 4 | DT vs RF vs XGBoost intuition + project deep dive | Microsoft India | D&AS | onsite R1 | E-M | BL-MSI | Apr 2022 |
| 5 | XGBoost depth/regularisation; role of dropout | Uber | MLE | unknown | E-M | PH-UBER | Sep 2025 |
| 6 | Probability calibration and logistic regression | Uber | MLE | phone/onsite | E-M | IQ-UBER | 2025 |
| 7 | Overfitting vs underfitting and fixes | LinkedIn | MLE | unknown | E-M | PH-LI | Feb 2026 |
| 8 | Practical ML: evaluation, feature engineering | LinkedIn | MLE | unknown | E-M | PH-LI | Feb 2026 |
| 9 | Regularisation methods and trade-offs | Google | MLE | unknown | H | PH-G2 | Sep 2025 |
| 10 | Time complexity of training an SVM | Google | MLE | unknown | E-M | EXP-G / GD-G | 2025 |
| 11 | Hyperparameter-tuning methods | Amazon | AS | unknown | E-M | PH-AMZ | Dec 2025 |
| 12 | Logistic regression fundamentals | Amazon | AS (Sr) | unknown | E-M | PH-AMZ | Sep 2025 |
| 13 | How does XGBoost parallelise training? | Amazon | AS | unknown | E-M | PH-AMZ2 | Sep 2025 |
| 14 | Collaborative filtering approaches + evaluation | Amazon | AS | unknown | H | PH-AMZ2 | Sep 2025 |
| 15 | Bias-variance; bagging vs boosting; basic stats | Amazon | AS | onsite | E-M | GD-AMZ | 2025 |
| 16 | Collaborative vs content-based filtering | Amazon | AS | onsite | E-M | GD-AMZ | 2025 |
| 17 | Bias-variance, calibration, model drift | NVIDIA | MLE | unknown | E-M | PH-NV | Feb 2026 |
| 18 | Data leakage, missing data, loss functions | Adobe | MLE | unknown | E-M | PH-ADOBE | Jan 2026 |
| 19 | Classification lifecycle and CTR modelling | Apple | MLE | unknown | E-M | PH-APPLE | Dec 2025 |
| 20 | KNN, ROC-AUC, precision/recall, losses | Myntra | DS | technical | E-M | GD-MYN | 2025 |
| 21 | Random forest and clustering scenarios | Flipkart | DS | technical | E-M | GD-FK | 2025 |
| 22 | Does CV reduce bias, variance, Type I or Type II error? | Headlands | DS | unknown | E-M | PH-ML | Aug 2026 |
| 23 | Can a single k always maximise kNN LOO accuracy? | C3 AI | DS Intern | unknown | E-M | PH-ML | Sep 2026 |
| 24 | Precision vs recall basics (+ CV) | Adobe Research | ML Research Intern | technical | E-M | GD-ADOBE | 2025 |

### 2. Statistics & probability
| # | Question | Company | Role | Round | Diff | Src | Date |
|---|---|---|---|---|---|---|---|
| 25 | Generate values per given weighted probabilities | Google | MLE | unknown | E-M | PH-G | Sep 2025 |
| 26 | Sample from a multinomial efficiently | Google | MLE | unknown | E-M | EXP-G / GD-G | 2025 |
| 27 | Substring search + weighted random sampling | Google | MLE | unknown | E-M | PH-G | Mar 2026 |
| 28 | Simulate Uniform(0,1) from random bits | Google | DS (Sr) | unknown | E-M | PH-GDS | Nov 2025 |
| 29 | Estimate population mean and conversion rate accurately | Google | DS | unknown | H | PH-GDS | Jul 2025 |
| 30 | When/how to use propensity-score matching | Google | DS | unknown | E-M | PH-GDS | Nov 2025 |
| 31 | When to use mixed-effects models | Google | DS | unknown | E-M | PH-GDS | Nov 2025 |
| 32 | Measure causal impact of YouTube ads | Google | DS | unknown | E-M | PH-GDS | Oct 2025 |
| 33 | Test whether bird species are segregated | Google | DS | unknown | E-M | PH-GDS | May 2026 |
| 34 | Causal effect of weather on mental health | Google | DS | unknown | E-M | PH-GDS | Feb 2026 |
| 35 | Sample uniformly from a circle's area | LinkedIn | MLE | unknown | E-M | PH-LI | Feb 2026 |
| 36 | Weighted index sampling (prefix sum + binary search) | LinkedIn | MLE | unknown | E-M | PH-LI | Feb 2026 |
| 37 | Uniform 0–6 from a biased coin | LinkedIn | MLE | unknown | E-M | PH-LI | Feb 2026 |
| 38 | Test whether two user populations differ | Amazon | AS | unknown | E-M | PH-AMZ | Dec 2025 |
| 39 | Multi-armed bandit principles | Amazon | AS (Sr) | unknown | E-M | PH-AMZ | Sep 2025 |
| 40 | KL divergence vs cross-entropy | Amazon | AS | onsite | E-M | GD-AMZ | 2025 |
| 41 | Explain and test a gap in completion rates | Uber | MLE | unknown | E-M | PH-UBER | Mar 2026 |
| 42 | Role of p-value in product decisions | Adobe | DS | unknown | E-M | PH-ADOBE | Aug 2025 |
| 43 | Bayes' rule + forward-pass arithmetic | Netflix | MLE Intern | unknown | E-M | PH-ML | Sep 2026 |
| 44 | p-tests and t-tests | Flipkart | DS | technical | E-M | GD-FK | 2025 |
| 45 | Coding on queuing and probability | Microsoft India | D&AS | coding | E-M | BL-MSI | 2022 |
| 46 | KL divergence between distributions + applications | OpenAI | RS | unknown | H | TP-OAI (unverified) | 2025 |

### 3. Deep learning
| # | Question | Company | Role | Round | Diff | Src | Date |
|---|---|---|---|---|---|---|---|
| 47 | Activations, losses, how Adam works | LinkedIn | MLE | unknown | E-M | PH-LI | Feb 2026 |
| 48 | ML evaluation, sequence models, optimisers | Amazon | AS | unknown | E-M | PH-AMZ | Dec 2025 |
| 49 | LayerNorm in transformers | Amazon | AS (Sr) | unknown | E-M | PH-AMZ | Sep 2025 |
| 50 | CNNs vs fully connected networks | Amazon | AS | unknown | E-M | PH-AMZ2 | Dec 2025 |
| 51 | Transformer in detail; positional encoding; long-range deps | Amazon | AS | onsite | H | GD-AMZ | 2025 |
| 52 | If token order doesn't matter, how to train the transformer? | Amazon | AS | onsite | H | GD-AMZ | 2025 |
| 53 | Transformer architecture and variants | Google | MLE | unknown | H | PH-G2 | Sep 2025 |
| 54 | VAEs: ELBO, KL term, reparameterisation | Google | MLE | unknown | H | PH-G2 | Aug 2026 |
| 55 | Self-attention: implementation, complexity, efficient variants | Meta | MLE | unknown | H | PH-META2 | Jun 2026 |
| 56 | Transformer attention fundamentals | Adobe | MLE | unknown | H | PH-ADOBE | May 2026 |
| 57 | Dataset size vs generalisation; U-Net skip connections | Apple | MLE | unknown | E-M | PH-APPLE | Mar 2026 |
| 58 | Vision encoders and bottlenecks in multimodal LLMs | Apple | MLE | unknown | E-M | PH-APPLE | Nov 2025 |
| 59 | Diagnose failures of a vision model | Apple | MLE | unknown | E-M | PH-APPLE | Mar 2026 |
| 60 | Audio preprocessing and training choices | Apple | MLE | unknown | E-M | PH-APPLE | Feb 2026 |
| 61 | Convolution; NMS in YOLO; count CNN params | Qualcomm | ML/AI | technical | E-M | GD-QC | 2025 |
| 62 | Encoder-only vs decoder-only; GQA; MoE | Qualcomm | ML/AI | technical | E-M | GD-QC | 2025 |
| 63 | Why scale by sqrt(d_k)? Why O(n²) and fixes? RoPE? | General | LLM/MLE | unknown | E-M | TI-TF | Jul 2026 |
| 64 | Why LayerNorm not BatchNorm in transformers | OpenAI | RS | unknown | H | TP-OAI (unverified) | 2025 |
| 65 | Data/model parallelism, collective comms | Amazon | AS | unknown | E-M | PH-AMZ2 | Dec 2025 |
| 66 | Transformers + case study on math intuition in DL | Myntra | DS | R1/R2 | E-M | GD-MYN | 2025 |

### 4. LLM / GenAI
| # | Question | Company | Role | Round | Diff | Src | Date |
|---|---|---|---|---|---|---|---|
| 67 | LLM fundamentals and trade-offs | Amazon | AS | unknown | E-M | PH-AMZ | Jul 2025 |
| 68 | Transformers and Mixture-of-Experts | Amazon | AS | unknown | E-M | PH-AMZ/AMZ2 | Dec 2025 / May 2026 |
| 69 | Tokenisation design; KL-regularised SFT | Amazon | AS | unknown | E-M | PH-AMZ2 | Jun 2026 |
| 70 | Early NLP embeddings → modern LLM embeddings | Amazon | AS | unknown | E-M | PH-AMZ2 | Aug 2026 |
| 71 | Attention; BERT vs GPT; pre-training vs fine-tuning vs post-training | Amazon | AS | onsite | E-M | GD-AMZ | 2025 |
| 72 | Transformers + deploying an LLM safely | Microsoft | MLE | unknown | E-M | PH-MS | Dec 2025 |
| 73 | Calibrate LLM output to Word formatting | Microsoft | MLE | unknown | E-M | PH-MS | Jan 2026 |
| 74 | Clean OCR data, build LLM training set | Microsoft | MLE | unknown | E-M | PH-MS | Feb 2026 |
| 75 | Annotator agreement; LLM-as-judge vs human | Apple | MLE | unknown | H | PH-APPLE | Aug 2025 |
| 76 | KV cache in transformer inference | OpenAI | MLE | unknown | E-M | PH-OAI | Jan 2026 |
| 77 | Tokenisation methods; LLM-based recommendations | Google | MLE | unknown | E-M | PH-G2 | Feb 2026 |
| 78 | Detect and prevent reward hacking | Google | MLE | unknown | H | PH-G2 | Aug 2026 |
| 79 | KL divergence in LM training | Google | MLE | unknown | H | PH-G2 | Aug 2026 |
| 80 | Importance sampling in LLM training | Google | MLE | unknown | H | PH-G2 | Aug 2026 |
| 81 | GRPO vs PPO; sparse vs dense rewards | Siemens | MLE (Sr) | unknown | E-M | PH-ML | Sep 2026 |
| 82 | SFT vs DPO vs PPO; role of KL penalty | Siemens | MLE (Sr) | unknown | E-M | PH-ML | Sep 2026 |
| 83 | MoE and expert parallelism | Mistral AI | SWE | unknown | E-M | PH-ML | Sep 2026 |
| 84 | RAG vs fine-tuning, context limits, state, prompt injection | Mercor | SWE | unknown | E-M | PH-ML | Sep 2026 |
| 85 | Design of a transformer LLM | NVIDIA | MLE | unknown | H | PH-NV | Jul 2025 |
| 86 | Optimise LLM training and serving | Adobe | MLE | unknown | H | PH-ADOBE | May 2026 |
| 87 | Training with noisy human annotators | OpenAI | MLE | unknown | H | PH-OAI | Apr 2026 |
| 88 | LLMs, prompting, RAG, vector DBs, embeddings, agents, retrievers | Fractal | DS/AI | technical | E-M | GD-FRAC | 2025 |
| 89 | Experiment to reduce hallucinations | OpenAI | MLE | design | H | TP-OAI (unverified) | 2025 |
| 90 | Retrieval vs fine-tuning for knowledge; evaluating an LLM system | General | LLM eng | unknown | E-M | TI-TF | Jul 2026 |

### 5. ML coding (from scratch)
| # | Question | Company | Role | Round | Diff | Src | Date |
|---|---|---|---|---|---|---|---|
| 91 | Multi-head attention class + SOTA models | Google | MLE | onsite | E-M | EXP-G / GD-G | 2025 |
| 92 | Transformer block with SwiGLU | Google | MLE | unknown | E-M | PH-G2 | Dec 2025 |
| 93 | Build linear regression in coding round | Google India | MLE | coding | E-M | TARO-G1 | Jun 2025 |
| 94 | Multi-head attention in NumPy only | Amazon | AS | unknown | E-M | PH-AMZ-MHA | Jun 2026 |
| 95 | Decoder-only GPT-style transformer | Amazon | AS | unknown | E-M | PH-AMZ2 | Nov 2025 |
| 96 | K-means (+ interval/frequency tasks) | Amazon | AS | unknown | E-M | PH-AMZ | Dec 2025 |
| 97 | Multi-head self-attention | Uber | MLE | unknown | E-M | PH-UBER | Jan 2026 |
| 98 | Linear and logistic regression | Uber | MLE | unknown | E-M | PH-UBER | Mar 2026 |
| 99 | 1D convex minimisation (ternary/binary search) | Uber | MLE | unknown | E-M | PH-UBER | Sep 2025 |
| 100 | CLIP contrastive loss | Uber | MLE | unknown | E-M | PH-UBER | Apr 2026 |
| 101 | K pickup locations minimising L1 (k-medians) | Uber | MLE | unknown | E-M | PH-UBER | Dec 2025 |
| 102 | K-means + why it converges | LinkedIn | MLE | unknown | E-M | PH-LI | May 2025 |
| 103 | Debug logistic-regression training code | LinkedIn | MLE (Sr) | unknown | E-M | PH-LI | Aug 2026 |
| 104 | Masked multi-head self-attention | Apple | MLE | unknown | E-M | PH-APPLE | Apr 2026 |
| 105 | TF-IDF scoring / bag-of-words similarity | Apple | MLE | unknown | E-M | PH-APPLE | Dec / Aug 2025 |
| 106 | K-means from scratch | Adobe | MLE | unknown | E-M | PH-ADOBE | Jan 2026 |
| 107 | Debug MiniGPT; backprop through matmul | OpenAI | MLE | unknown | E-M | PH-OAI | Apr 2026 |
| 108 | Backprop for a tiny network | OpenAI | MLE | unknown | H | PH-OAI | Apr 2026 |
| 109 | Debug transformer, add KV cache | OpenAI | MLE | unknown | E-M | PH-OAI / PH-ML | Feb / Sep 2026 |
| 110 | Minimal reverse-mode autograd | OpenAI | SWE | unknown | E-M | PH-ML | Sep 2026 |
| 111 | Entropy; 1-NN; vectorise 1-NN as forward pass | OpenAI | MLE | unknown | E-M | PH-OAI / PH-ML | Apr / Aug 2026 |
| 112 | Greedy, top-k, top-p decoding in NumPy | Cohere | MLE | unknown | E-M | PH-ML | Sep 2026 |
| 113 | Softmax cross-entropy fwd/bwd + training loop | Waymo | MLE | unknown | E-M | PH-ML | Sep 2026 |
| 114 | Causal masking for decoder-only (PyTorch) | Qualcomm | ML/AI | technical | E-M | GD-QC | 2025 |
| 115 | Loss function + logistic regression in NumPy | Microsoft Bengaluru | AS | technical | E-M | GD-MS | Apr 2026 |
| 116 | GD from scratch; self-attention; voice-activity detector (2.5 h) | Sarvam AI | ML | onsite | H | BL-SARVAM | Jul 2026 |
| 117 | Build and defend a baseline from a CSV | Microsoft | DS (Sr, AI) | unknown | E-M | PH-ML | Jun 2026 |
| 118 | Multi-head self-attention in PyTorch | xAI | MLE | technical | E-M | GD-XAI | 2025 |
| 119 | Precision/recall from a flaky top-k API | Microsoft | MLE | unknown | E-M | PH-MS | Feb 2026 |
| 120 | Pandas time-series groupby | Amazon | AS (New Grad) | phone | E-M | PH-AMZ-NG | Aug 2025 |
| 121 | Fix 5–6 subtle bugs in PyTorch net; add BN to transformer | OpenAI | MLE | unknown | H | TP-OAI (unverified) | 2025 |

### 6. ML system design
| # | Question | Company | Role | Round | Diff | Src | Date |
|---|---|---|---|---|---|---|---|
| 122 | LLM-based Q&A system | Google India | Staff MLE | onsite | H | EXP-G | Apr 2026 |
| 123 | App helping blind people navigate indoors | Google Hyderabad | MLE | onsite | E-M | TARO-G2 | Jul 2025 |
| 124 | App-store / product / video recommender | Google | MLE | unknown | E-M | PH-G | Feb 2026 / Dec 2025 |
| 125 | Real-time recsys / RL feedback recommender | Google | MLE | unknown | E-M | PH-G | Dec / Jul 2025 |
| 126 | Fraud-detection system | Google | MLE | unknown | E-M | PH-G | Jan 2026 |
| 127 | Large-scale near-duplicate video detection | Google | MLE | unknown | H | PH-G2 | Jan 2026 |
| 128 | Chatbot over structured + unstructured data | Google | MLE | unknown | E-M | PH-G2 | Feb 2026 |
| 129 | Cold-start strategies for ranking | Google | MLE | unknown | E-M | PH-G2 | Mar 2026 |
| 130 | Multi-GPU matrix multiplication | Google | MLE | unknown | H | PH-G2 | Sep 2025 |
| 131 | Find companies similar to a client (embeddings) | Google | DS | unknown | H | PH-GDS | Oct 2025 |
| 132 | RAG system end to end | Amazon | AS | unknown | E-M | PH-AMZ | Sep 2025 |
| 133 | LLM quality-validation system | Amazon | AS | unknown | E-M | PH-AMZ | Dec 2025 |
| 134 | Recsys: cold start, dropout, stability | Amazon | AS | unknown | E-M | PH-AMZ | Jan 2026 |
| 135 | Model worse online than offline — debug | Amazon | AS | unknown | E-M | PH-AMZ2 | Jan 2026 |
| 136 | Spam detection; fraud detection (15 min) | Amazon | AS (New Grad) | onsite | E-M | PH-AMZ-NG | Aug 2025 |
| 137 | Product-search system | Microsoft | MLE | unknown | E-M | PH-MS | Apr 2026 |
| 138 | RAG assistant with agentic tools; optimise vector search | Microsoft | MLE | unknown | E-M | PH-MS | Feb / Jan 2026 |
| 139 | Infer user intent from typing in real time | Microsoft | MLE | unknown | E-M | PH-MS | Jan 2026 |
| 140 | Restaurant recommendations (Uber Eats) | Uber | MLE | unknown | E-M | PH-UBER | Dec 2025 |
| 141 | Real-time grid-based ETA | Uber | MLE | unknown | H | PH-UBER | Sep 2025 |
| 142 | Feed-ranking system | Uber | MLE | unknown | E-M | PH-UBER | Mar 2026 |
| 143 | Ad-bidding forecasting and pacing | LinkedIn | MLE | unknown | E-M | PH-LI | Aug 2026 |
| 144 | LinkedIn Learning recs; skills inference | LinkedIn | MLE | unknown | E-M | PH-LI | Feb 2026 |
| 145 | App Store search; CPA ad bidding | Apple | MLE | unknown | E-M | PH-APPLE | Dec 2025 / Mar 2026 |
| 146 | DCN v1 vs v2 for CTR + A/B test | Apple | MLE | unknown | E-M | PH-APPLE | Mar 2026 |
| 147 | Multimodal RAG / grounded voice assistant | Apple | MLE | unknown | E-M | PH-APPLE | Dec 2025 / Jan 2026 |
| 148 | Ads ranking with calibration | Meta | MLE | unknown | E-M | PH-META2 | Jan 2026 |
| 149 | Detect weapon-sale ads; rank nearby items/notifications | Meta | MLE | unknown | E-M / H | PH-META2 | Jan 2026 |
| 150 | NL Q&A over AEP; multimodal embedding service | Adobe | MLE / SWE | unknown | H | PH-ADOBE | Aug / Sep 2025 |
| 151 | Out-of-distribution detection system | OpenAI | MLE | unknown | E-M | PH-OAI | Dec 2025 |
| 152 | Short-video engagement with skewed data | ByteDance | DS Intern | unknown | E-M | PH-ML | Sep 2026 |
| 153 | ML solution for credit-card target audience from student data | HiLabs | DS (campus) | ML round | E-M | IITK-HL | 2024 |
| 154 | Guesstimate EV-scooter market; place EV chargers | ZS Associates | DAA | case | E-M | GD-ZS | 2025 |

### 7. Research-role specifics (thin)
| # | Question / format | Company | Role | Round | Diff | Src | Date |
|---|---|---|---|---|---|---|---|
| 155 | Present and defend your research; research interests | Google | MLE (research) | unknown | H | PH-G | Jan 2026 |
| 156 | Dissertation and supervision experience | Google | MLE | unknown | E-M | PH-G | Jul 2025 |
| 157 | 30–35 min resume project deep dive, then CV + probability; may read team's paper | Adobe Research | ML Research Intern | technical | E-M | GD-ADOBE | 2025 |
| 158 | Derive closed-form linear regression | Meta | MLE Intern | unknown | E-M | PH-META2 | Feb 2026 |
| 159 | Derive sharded matmul and its backprop | OpenAI | MLE | unknown | E-M | PH-OAI | Apr 2026 |
| 160 | Derive VAE ELBO and reparameterisation | Google | MLE | unknown | H | PH-G2 | Aug 2026 |
| 161 | Speech latent-space decomposition (content vs speaker) | Sarvam AI | ML | onsite | H | BL-SARVAM | Jul 2026 |
| 162 | Derive attention complexity; debug overfitting; derive on the spot | OpenAI | RS | unknown | H | TP-OAI (unverified) | 2025 |
| 163 | Asynchronous RL post-training system | Meta | MLE | unknown | H | PH-META2 | Sep 2025 |
| 164 | Mine novel images from unlabelled data | OpenAI | MLE | unknown | E-M | PH-OAI | Apr 2026 |
| 165 | Find flaws in an ML pipeline case-study report | StackAdapt | MLE | unknown | E-M | PH-ML | Sep 2026 |
| 166 | MSR India Research Fellow: research talk, med-hard LeetCode, linear-algebra algorithms, ML fundamentals | MSR India | Research Fellow | onsite | H | [AmbitionBox](https://www.ambitionbox.com/interviews/microsoft-research-lab-interview-questions/data-scientist) (snippet) | unknown |
| 167 | Anthropic RE: coding test with heavy non-algorithmic logic, then video call | Anthropic | Research Engineer | OA/onsite | H | GD-ANT | 2025 |

### 8. DSA in ML-role loops
| # | Question / topic | Company | Role | Round | Diff | Src | Date |
|---|---|---|---|---|---|---|---|
| 168 | Coin Change; Longest Palindromic Subsequence; Diameter of Binary Tree | Google | AI Eng Intern | unknown | E-M | EXP-G | Jan 2026 |
| 169 | Valid Palindrome | Google India | Staff MLE | onsite | E-M | EXP-G | Apr 2026 |
| 170 | LeetCode-Hard DP instead of theory round | Google Hyderabad | MLE | onsite | H | TARO-G2 | Jul 2025 |
| 171 | Arrays, strings, hashmaps, trees/graphs, recursion, DP | Google India | MLE | coding | E-M | TARO-G3 | Nov 2025 |
| 172 | LRU-like DS; fence-painting DP; BFS/DFS crawler; reachability with distance-threshold edges | Google | MLE | unknown | E-M / H | PH-G2 | Dec 2025 – Feb 2026 |
| 173 | Burst Balloons; string manipulation | Microsoft India | MLE (L4) | onsite | H | EXP-MS | Feb 2025 |
| 174 | Top-k frequent w/ tie rule; min abs diff pairs; cache + merge intervals | Microsoft | MLE | unknown | E-M | PH-MS | Feb 2026 |
| 175 | Two Sum; grid shortest path with obstacles; LFU cache; merge time ranges; highest-avg-salary team | Amazon | AS | unknown | E-M | PH-AMZ/AMZ2 | 2025–26 |
| 176 | Dijkstra w/ obstacles; stock profit; BST LCA; Course Schedule III; LC 3479 | Amazon | AS (New Grad) | phone/onsite | E-M | PH-AMZ-NG | Aug 2025 |
| 177 | Connected delivery zones; dependent-task min time (topo sort); currency conversion graph; first local minimum | Uber | MLE | unknown | E-M | PH-UBER | 2025–26 |
| 178 | Word ladder with caching; total covered interval length; point-to-segment distance | LinkedIn | MLE | unknown | E-M | PH-LI | 2025–26 |
| 179 | Subarray with sum multiple of k? | Adobe | MLE | unknown | E-M | PH-ADOBE | Aug 2025 |
| 180 | OA: 4 Qs (2 DP, 1 tree); interviews: Burning Tree, Shortest Path to Get All Keys (on paper) | PhonePe | Campus SDE | OA + tech | H | LC-PP | 2025 |
| 181 | Two-pointer and binary search (Striver A–Z level) | HiLabs | DS (campus) | DSA round | E-M | IITK-HL | 2024 |
| 182 | Expiring GPU credits (heap); multi-source BFS infection; LRU with TTL | OpenAI | MLE / SWE | unknown | E-M / H | PH-OAI; TP-OAI | 2025–26 |
| 183 | LRU + copy list with random pointer; sparse matrix ops; maze-solver extension | Meta | MLE | unknown | E-M | PH-META2 | Jan–Mar 2026 |

---

## Good resources
1. [TorchLeet](https://github.com/Exorust/TorchLeet) ([site](https://torch-leet.vercel.app)) — 90 PyTorch interview problems incl. attention, KV cache, LoRA, DPO, GRPO
2. LLM-Interview-Questions-and-Answers-Hub (KalyanKS-NLP) — 115+ LLM Q&As; [listing](https://www.sourcepulse.org/projects/20967302) (GitHub URL unchecked)
3. [llmgenai/LLMInterviewQuestions](https://github.com/llmgenai/LLMInterviewQuestions) — 100+ Qs, 15 categories
4. [SimranAnand1/LLMInterviewQuestions](https://github.com/SimranAnand1/LLMInterviewQuestions) — similar bank
5. LLM-Algorithm-Intern-Guide (Junvate) — [listing](https://www.sourcepulse.org/projects/26732793) (may be Chinese)
6. LLMs_interview_notes (km1994) — [listing](https://www.sourcepulse.org/projects/1832739) (probably Chinese)
7. [PracHub ML category](https://prachub.com/categories/machine-learning) — largest recent company-tagged bank found
8. [techinterview.org: LLM transformer probes](https://www.techinterview.org/post/3233476821/what-llm-interviewers-ask-about-transformers/)
9. [techinterview.org: MLE interview post-LLM era](https://www.techinterview.org/post/3233474925/ml-engineer-interview-post-llm-era/)
10. [Hello Interview: Meta AI-enabled coding](https://hellointerview.com/blog/meta-ai-enabled-coding)
11. [interviewing.io: AI-assisted Meta interview](https://interviewing.io/blog/how-to-use-ai-in-meta-s-ai-assisted-coding-interview-with-real-prompts-and-examples)
12. [Canva: AI in interviews](https://canva.dev/blog/engineering/yes-you-can-use-ai-in-our-interviews)
13. [IIT Kanpur SPO Insights](https://spo.iitk.ac.in/insights) — first-hand IIT DS/ML placement write-ups
14. [Exponent](https://www.tryexponent.com/guides/google-machine-learning-engineer-interview/experiences) — dated Google MLE / MS AS experiences (partly paywalled)
15. [Taro](https://www.jointaro.com/interviews/companies/google/experiences/machine-learning-engineer-hyderabad-july-31-2025-no-offer-positive-b956ec0a/) — dated Google MLE India experiences

Not opened this session (check yourself): Chip Huyen's [ML Interviews Book](https://huyenchip.com/ml-interviews-book), [alirezadir/Machine-Learning-Interviews](https://github.com/alirezadir/Machine-Learning-Interviews), [khangich/machine-learning-interview](https://github.com/khangich/machine-learning-interview), [deep-ml.com](https://deep-ml.com).

## Gaps to fill next
- Indian product companies (Flipkart, Meesho, Zepto, Dream11, PhonePe, Myntra) DS/ML rounds
- DE Shaw ML/quant probability
- Samsung SRIB and Qualcomm 2025 OAs
- Visa, Mastercard, PayPal, Axtria, ProcDNA, MAQ, Sigmoid
- Google DeepMind / Research India pre-doc interviews
- Full Glassdoor review text (all blocked)
