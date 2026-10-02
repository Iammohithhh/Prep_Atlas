import sys
sys.path.insert(0, 'build/sol_gen')
from common import D, T, S, save

D['web-ml-047'] = T(
 'Activation functions add nonlinearity, loss functions define the training objective, and Adam is an adaptive optimiser that combines momentum with per-parameter learning rates.',
 'Without nonlinear activations, stacked linear layers collapse into one linear map. Adam scales each parameter\'s step by a running estimate of its gradient magnitude and smooths the direction with momentum.',
 'Activations: ReLU max(0, x), GELU x Phi(x), sigmoid 1/(1 + e^(-x)), tanh, softmax e^(z_i)/sum e^(z_j). Losses: MSE for regression, cross-entropy -sum y log p for classification. Adam: m_t = b1 m_(t-1) + (1 - b1) g_t; v_t = b2 v_(t-1) + (1 - b2) g_t^2; m_hat = m_t/(1 - b1^t), v_hat = v_t/(1 - b2^t); theta <- theta - eta m_hat/(sqrt(v_hat) + eps), with b1 = 0.9, b2 = 0.999, eps = 1e-8.',
 'For a parameter with consistently large gradients, v_hat is large, so its effective step is reduced; for rarely updated parameters v_hat is small and the step is larger, which helps sparse features.',
 'Adam converges fast with little tuning but can generalise slightly worse than SGD with momentum on some vision tasks; AdamW decouples weight decay. ReLU is cheap but can die; GELU or SiLU are common in transformers. Sigmoid and tanh saturate and vanish gradients in deep nets.',
 [('Why bias correction?', 'The moment estimates are initialised at zero and biased low early on.'),
  ('Adam versus SGD?', 'Adam adapts per parameter; SGD with momentum often generalises better with tuning.'),
  ('Why cross-entropy for softmax?', 'Its gradient p - y is simple and avoids saturation.')])

D['web-ml-048'] = T(
 'ML evaluation measures how well a model generalises; sequence models (RNN, LSTM, GRU, transformers) process ordered data; optimisers (SGD, momentum, Adam) update the weights.',
 'Evaluate on data resembling deployment; sequence models differ in how they carry context; optimisers differ in how they use gradient history.',
 'Evaluation: split by time or group, metrics tied to cost, confidence intervals. RNN: h_t = f(W h_(t-1) + U x_t); LSTM adds gates (forget, input, output) with a cell state c_t = f_t * c_(t-1) + i_t * g_t that eases gradient flow. Transformers use attention: softmax(Q K^T/sqrt(d)) V with parallel training. SGD: theta <- theta - eta g; momentum adds v <- mu v + g; Adam adds second-moment scaling.',
 'Forecasting demand: use a rolling-origin split, evaluate MAE and sMAPE; an LSTM captures local patterns, a transformer long-range ones; AdamW with a warm-up and cosine decay is a common default.',
 'RNNs are sequential and slow to train and struggle with long dependencies; transformers parallelise but cost O(n^2) in length. SGD with momentum often generalises well; Adam converges faster. Use gradient clipping for RNNs.',
 [('What is the vanishing gradient problem?', 'Repeated multiplication by small Jacobians shrinks gradients in long sequences.'),
  ('LSTM versus GRU?', 'GRU has fewer gates and parameters.'),
  ('Why learning-rate warm-up?', 'Adam statistics are unreliable at the start.')])

D['web-ml-049'] = T(
 'Layer normalisation normalises the activations of each token over the feature dimension to zero mean and unit variance, then applies a learned scale and shift.',
 'Transformers process sequences of varying length with small or varying batches; per-token normalisation stabilises activations without depending on the batch.',
 'For x in R^d: mu = (1/d) sum x_i, sigma^2 = (1/d) sum (x_i - mu)^2, LN(x) = gamma * (x - mu)/sqrt(sigma^2 + eps) + beta. The placement matters: post-LN (original transformer) puts LN after the residual sum; pre-LN puts it before each sublayer and trains more stably at depth. RMSNorm drops the mean: x/sqrt(mean(x^2) + eps) * gamma.',
 'A token vector (2, 4, 6, 8): mu = 5, sigma^2 = 5, normalised = (-1.34, -0.45, 0.45, 1.34) before gamma and beta.',
 'Pre-LN is easier to optimise (no warm-up sensitivity) but may give slightly lower final quality; RMSNorm is cheaper and widely used in modern LLMs. LN has no batch statistics, so training and inference behave identically.',
 [('Why not batch norm?', 'Batch statistics are unstable with variable sequence lengths and small batches, and differ between training and inference.'),
  ('Pre-LN versus post-LN?', 'Pre-LN has better gradient flow at depth.'),
  ('What does gamma do?', 'Restores representational scale per feature.')])

D['web-ml-050'] = T(
 'Convolutional networks apply small shared filters over local neighbourhoods, whereas fully connected networks connect every input to every unit.',
 'Images have local structure and translation invariance: a feature detector useful in one place is useful elsewhere, so sharing weights is a strong, sensible prior.',
 'A fully connected layer on a 224 x 224 x 3 image with 1000 units needs 224 x 224 x 3 x 1000 = 150M weights. A conv layer with 64 filters of size 3 x 3 x 3 has 64 x (27 + 1) = 1,792 parameters. Output size: floor((n + 2p - k)/s) + 1. Receptive field grows with depth, and pooling or strides downsample.',
 'For MNIST, an MLP reaches about 98%; a small CNN reaches 99.3% with far fewer parameters and better translation robustness.',
 'CNNs: parameter efficient, strong inductive bias for images and audio, equivariant to translation. Fully connected layers: flexible for tabular data and as classifier heads but data hungry on images. Vision transformers lose some bias but scale better with data.',
 [('What is equivariance?', 'Shifting the input shifts the feature map the same way.'),
  ('Why 3 x 3 filters?', 'Stacks give large receptive fields with fewer parameters.'),
  ('How do you count parameters?', 'k x k x C_in x C_out + C_out per conv layer.')])

D['web-ml-051'] = T(
 'The transformer is a sequence model based on self-attention, with positional information added so the order of tokens is known; it handles long-range dependencies in one attention step.',
 'Every token can attend to every other token directly, so the path length between any two positions is O(1), unlike RNNs where it is O(n).',
 'Attention(Q, K, V) = softmax(Q K^T/sqrt(d_k)) V; multi-head attention concatenates h heads with learned projections. Block: x + MHA(LN(x)), then x + FFN(LN(x)) with FFN = W2 act(W1 x). Positional encodings: sinusoidal PE(pos, 2i) = sin(pos/10000^(2i/d)), PE(pos, 2i + 1) = cos(...); or learned, relative or rotary (RoPE).',
 'For a sentence "the cat sat", the query of "sat" attends strongly to "cat" (subject) regardless of distance; without positional encoding "cat sat the" would look identical.',
 'Self-attention costs O(n^2 d) time and O(n^2) memory; long contexts need sparse, linear or FlashAttention-style kernels. Encoder-only (BERT), decoder-only (GPT) and encoder-decoder (T5) variants suit different tasks.',
 [('Why positional encoding?', 'Attention is permutation-equivariant.'),
  ('Why multiple heads?', 'Different subspaces capture different relations.'),
  ('How are long-range dependencies handled?', 'Direct attention links, at quadratic cost.')])

D['web-ml-052'] = T(
 'If token order did not matter, the task is a bag-of-tokens (set) problem, so the transformer needs no positional information and should be permutation invariant.',
 'Self-attention without positional encodings is permutation-equivariant; pooling the outputs (mean or attention pooling) makes the whole model permutation-invariant. That is exactly right when order carries no information.',
 'Without positions, output_i = sum_j softmax(q_i . k_j/sqrt(d)) v_j depends only on the set of inputs. Set-based architectures: Deep Sets f(X) = rho(sum phi(x)), Set Transformer with induced set attention. To train: use random token order augmentation or no positional embeddings, apply a permutation-invariant pooling and a loss on the pooled output.',
 'Classifying a bag of product tags: embed each tag, run a few self-attention layers without positions, mean-pool, then a linear classifier; shuffling the tags leaves the prediction unchanged.',
 'Remove positional encodings to save parameters and enforce invariance; but if order matters even slightly (for example language), keep them. Pooling choice matters: sum for counts, mean for averages, max for presence.',
 [('Is attention alone order-aware?', 'No, only through positional encodings or masks.'),
  ('How to verify invariance?', 'Shuffle inputs and compare outputs.'),
  ('Which other models are permutation invariant?', 'Deep Sets and graph neural networks with sum aggregation.')])

D['web-ml-053'] = T(
 'The transformer architecture stacks blocks of multi-head self-attention and feed-forward layers with residual connections and normalisation; variants differ in masking and layout.',
 'Encoder blocks attend bidirectionally and are good for understanding; decoder blocks use causal masks and generate text; encoder-decoder models add cross-attention.',
 'Block: x <- x + Attn(Norm(x)); x <- x + FFN(Norm(x)). Causal mask sets future scores to -infinity before the softmax. Cross-attention takes queries from the decoder and keys/values from the encoder. Parameter count per layer is about 12 d^2 (4 d^2 attention, 8 d^2 FFN with hidden size 4d).',
 'BERT (encoder-only, masked language modelling) for classification and retrieval; GPT (decoder-only) for generation; T5 (encoder-decoder) for translation and summarisation; ViT applies the encoder to image patches.',
 'Decoder-only models dominate large language modelling due to simplicity and in-context learning; encoders give better representations for a given size; efficiency variants include MQA/GQA, MoE and sparse attention.',
 [('Why residual connections?', 'They stabilise gradient flow in deep stacks.'),
  ('What is the FFN for?', 'It adds per-token nonlinear capacity and most of the parameters.'),
  ('How does BERT differ from GPT?', 'Bidirectional masked training versus left-to-right next-token training.')])

D['web-ml-054'] = T(
 'A variational autoencoder (VAE) learns a latent-variable generative model by maximising the evidence lower bound (ELBO), using an encoder q(z|x) and a decoder p(x|z) trained with the reparameterisation trick.',
 'The encoder maps x to a distribution over latent z; the decoder reconstructs x from a sample. The KL term keeps the latent distribution close to a simple prior so that sampling z from the prior generates new data.',
 'ELBO = E_q(z|x)[log p(x|z)] - KL(q(z|x) || p(z)) <= log p(x). With q = N(mu, diag sigma^2) and p(z) = N(0, I): KL = 0.5 sum (mu^2 + sigma^2 - log sigma^2 - 1). Reparameterisation: z = mu + sigma * eps, eps ~ N(0, I), which makes sampling differentiable with respect to mu and sigma. A beta-VAE multiplies the KL by beta.',
 'On MNIST with a 2D latent space, similar digits cluster; decoding points between clusters gives smooth morphs. Too small a KL weight gives good reconstructions but a poor prior match; too large causes posterior collapse (the decoder ignores z).',
 'VAEs give stable training and a latent space but blurrier samples than GANs or diffusion; mitigations: KL annealing, free bits, hierarchical or discrete (VQ-VAE) latents.',
 [('Why reparameterise?', 'Gradients cannot flow through random sampling otherwise.'),
  ('What is posterior collapse?', 'q(z|x) equals the prior and the decoder ignores z.'),
  ('Why is the ELBO a lower bound?', 'log p(x) = ELBO + KL(q || p(z|x)) with a nonnegative gap.')])

D['web-ml-055'] = T(
 'Self-attention lets every position compute a weighted sum of all value vectors, with weights from query-key similarity. Its time and memory cost is quadratic in sequence length, so efficient variants exist.',
 'Each token asks "who is relevant to me?" (query), is described by a key and contributes a value.',
 'Q = X W_q, K = X W_k, V = X W_v; A = softmax(Q K^T/sqrt(d_k)); out = A V. Complexity: O(n^2 d) time and O(n^2) memory for the score matrix (O(n d) after FlashAttention, which tiles computation in SRAM). Efficient variants: sparse and local windows (Longformer), low-rank/linear attention (Performer), multi-query/grouped-query attention to shrink the KV cache, FlashAttention for exact attention with IO-awareness.',
 '```python\nimport numpy as np\n\ndef attention(Q, K, V, mask=None):\n    d = Q.shape[-1]\n    s = Q @ K.swapaxes(-1, -2) / np.sqrt(d)\n    if mask is not None:\n        s = np.where(mask, s, -1e9)\n    s = s - s.max(-1, keepdims=True)\n    w = np.exp(s)\n    w = w / w.sum(-1, keepdims=True)\n    return w @ V\n```',
 'Exact attention is best below a few thousand tokens; use sliding windows or retrieval for much longer contexts; GQA/MQA trade a little quality for large inference savings.',
 [('Why divide by sqrt(d_k)?', 'To keep the score variance near 1 so softmax does not saturate.'),
  ('What does FlashAttention change?', 'Memory traffic, not the result.'),
  ('Is linear attention equal in quality?', 'Usually somewhat worse.')])

D['web-ml-056'] = T(
 'Attention computes, for each query, a probability distribution over keys and returns the corresponding mixture of values; it is the core operation of transformers.',
 'It is a soft, differentiable dictionary lookup: queries match keys, and the matched values are blended.',
 'softmax(q . k_j/sqrt(d_k)) gives weights a_j; output = sum_j a_j v_j. Masking: add -infinity to forbidden positions (causal masks, padding). Multi-head: h parallel attentions with dimension d/h each, concatenated and projected by W_o. The gradient flows through the softmax Jacobian diag(a) - a a^T.',
 'With query (1, 0), keys (1, 0) and (0, 1), d_k = 2: scores (0.707, 0) give weights (0.67, 0.33), so the output is 0.67 v_1 + 0.33 v_2.',
 'Attention is flexible and parallel but quadratic; softmax can become peaky at long contexts. Self-attention uses the same sequence for Q, K and V; cross-attention takes K and V from another sequence.',
 [('Self versus cross attention?', 'Same source versus another source for K and V.'),
  ('What if all scores are equal?', 'The output is the mean of the values.'),
  ('How do padding masks work?', 'Padded keys get -infinity scores.')])

D['web-ml-057'] = T(
 'Dataset size affects generalisation: more data reduces variance and lets larger models generalise; U-Net skip connections carry high-resolution encoder features to the decoder for precise localisation.',
 'With little data a model memorises; with more data the gap between training and test error closes. In segmentation, downsampling loses spatial detail that the decoder needs back.',
 'Learning curves: test error typically decreases as a power law n^(-alpha) towards an irreducible floor. U-Net: the encoder halves resolution and doubles channels; the decoder upsamples and concatenates the matching encoder feature map: x_dec = Conv([Up(x_dec), x_enc]). The skip path gives gradients a short route too.',
 'Medical segmentation with 100 images: a U-Net with augmentation (elastic deformations, flips) generalises well; removing skip connections blurs boundaries.',
 'Small data: use pretrained encoders, augmentation, regularisation and simpler models; large data: bigger models. Skips add memory but improve boundaries; alternatives include attention gates and nested skips (U-Net++).',
 [('Why concatenate rather than add?', 'It keeps both feature sets for the next convolution to mix.'),
  ('How to detect data-limited regimes?', 'Learning curves still falling with n.'),
  ('Is more data always better?', 'Only if representative and correctly labelled.')])

D['web-ml-058'] = T(
 'Multimodal LLMs pair a vision encoder (ViT, CLIP, SigLIP) with a language model through a connector (linear layer, MLP, Q-Former, cross-attention); bottlenecks arise from resolution, token count and the connector.',
 'Images must become a limited number of tokens the LLM can read; fine detail (text, small objects) is lost if the encoder resolution or the number of visual tokens is low.',
 'A ViT with patch size 14 on 336 x 336 gives (336/14)^2 = 576 tokens; the connector maps d_vision to d_llm; LLM attention cost grows with visual tokens. Training stages: alignment of the connector on caption data, then instruction tuning. Bottlenecks: contrastive encoders (CLIP) capture global semantics but little spatial or OCR detail; token compression (pooling, Q-Former) saves compute but drops detail.',
 'A model fails to read small receipt text: raise the input resolution, tile the image (AnyRes) and use an encoder trained for text-rich images.',
 'Higher resolution and more tokens give better detail at higher cost; frozen encoders are cheap, unfrozen ones adapt better; data quality and instruction diversity often dominate architecture choices.',
 [('Why not feed raw pixels?', 'Sequence length would be enormous.'),
  ('What does a Q-Former do?', 'A small set of learned queries compresses visual features.'),
  ('How to diagnose failures?', 'Probe separate skills: OCR, counting, spatial relations.')])

D['web-ml-059'] = T(
 'Diagnosing a failing vision model means separating data, model and evaluation problems and testing each with targeted experiments.',
 'Look at where errors concentrate (classes, slices, image conditions) before changing the model.',
 'Steps: (1) check the pipeline (label quality, preprocessing parity train vs serve, resolution); (2) learning curves for bias vs variance; (3) confusion matrix and per-slice metrics (lighting, device, class imbalance); (4) inspect failure examples and saliency (Grad-CAM) to detect shortcut learning; (5) check calibration and distribution shift (embedding distance, PSI); (6) ablate augmentation, resolution and pretraining.',
 'A defect detector with 95% validation accuracy fails in the factory: Grad-CAM shows it keys on the background tray colour. Fix by augmenting backgrounds and collecting deployment-like data.',
 'Quick wins: fix labels, add targeted data, augmentation and class weights; deeper changes: a better backbone, higher resolution, domain adaptation. Always rerun the evaluation on a deployment-like set.',
 [('What is shortcut learning?', 'Using spurious cues that correlate with labels in training.'),
  ('How to detect label noise?', 'High-loss examples reviewed by humans, confident learning.'),
  ('What if train and test differ?', 'Domain shift: collect or adapt with target-domain data.')])

D['web-ml-060'] = T(
 'Audio models usually work on spectrograms (mel features) or learned representations; preprocessing and training choices determine how much speech or sound information is preserved.',
 'Raw waveforms are long (16,000 samples per second); a short-time Fourier transform turns them into a time-frequency image that CNNs and transformers handle well.',
 'Pipeline: resample to a fixed rate (16 kHz), frame (25 ms window, 10 ms hop), STFT, mel filterbank (80 bins), log compression, per-utterance normalisation. Augmentation: SpecAugment (time/frequency masking), noise mixing, speed perturbation. Losses: CTC for alignment-free ASR, cross-entropy for classification, contrastive/self-supervised (wav2vec 2.0).',
 'Keyword spotting on 1 s clips: 98 frames x 40 mel bins, a small CNN with SpecAugment reaches high accuracy with a few hundred kilobytes of parameters.',
 'Mel features are compact and robust; learned front ends (wav2vec) give better accuracy with enough data; longer windows give frequency resolution, shorter ones time resolution. Match the preprocessing between training and serving exactly.',
 [('What is CTC?', 'A loss that sums over all alignments between audio frames and output tokens.'),
  ('Why log-mel?', 'Matches human loudness perception and compresses dynamic range.'),
  ('What is SpecAugment?', 'Random masking of time and frequency bands.')])

D['web-ml-061'] = T(
 'Convolution slides a kernel over the input computing local weighted sums; non-maximum suppression (NMS) removes duplicate detections in YOLO-style detectors; parameter counting multiplies kernel size by channels.',
 'Convolution shares weights spatially. Detectors predict many overlapping boxes for one object; NMS keeps the best-scoring box and removes boxes that overlap it too much.',
 'Conv output: (n + 2p - k)/s + 1; parameters = k_h k_w C_in C_out + C_out. NMS: sort boxes by score; repeatedly take the best box, delete others with IoU > threshold (for example 0.5), where IoU = area(A and B)/area(A or B). Example parameters: conv 3 x 3, 3 -> 16 channels: 3*3*3*16 + 16 = 448; then conv 3 x 3, 16 -> 32: 3*3*16*32 + 32 = 4,640; total 5,088.',
 '```python\ndef iou(a, b):\n    x1, y1 = max(a[0], b[0]), max(a[1], b[1])\n    x2, y2 = min(a[2], b[2]), min(a[3], b[3])\n    inter = max(0, x2 - x1) * max(0, y2 - y1)\n    area = lambda r: (r[2] - r[0]) * (r[3] - r[1])\n    return inter / (area(a) + area(b) - inter)\n\ndef nms(boxes, scores, thr=0.5):\n    order = sorted(range(len(boxes)), key=lambda i: -scores[i])\n    keep = []\n    while order:\n        i = order.pop(0)\n        keep.append(i)\n        order = [j for j in order if iou(boxes[i], boxes[j]) <= thr]\n    return keep\n```',
 'A low IoU threshold removes more duplicates but may drop nearby true objects (crowds); Soft-NMS decays scores instead of removing boxes.',
 [('What is IoU?', 'Intersection over union of two boxes.'),
  ('Complexity of NMS?', 'O(n^2) worst case.'),
  ('How to count BatchNorm parameters?', '2 x channels trainable (gamma, beta).')])

D['web-ml-062'] = T(
 'Encoder-only models (BERT) use bidirectional attention for understanding; decoder-only models (GPT) use causal attention for generation; GQA reduces KV-cache cost; MoE routes tokens to a few expert networks.',
 'Bidirectional context helps classification and retrieval; autoregressive models can generate and in-context learn. GQA and MoE trade parameters and compute differently.',
 'Causal mask: position i attends only to j <= i. Multi-head attention caches K and V of size 2 L n_heads d_head per token; GQA shares each K/V head among a group of query heads (n_kv < n_heads), cutting the cache by n_heads/n_kv; MQA is n_kv = 1. MoE: output = sum_{e in TopK} g_e(x) FFN_e(x), with a gating network g and a load-balancing auxiliary loss; parameters grow with the number of experts but compute only with top-k.',
 'Mixtral-style 8 experts, top-2: total parameters about 47B, active about 13B per token.',
 'Encoder-only: not generative but strong embeddings; decoder-only: general and scalable; GQA: small quality loss for big inference savings; MoE: more capacity per FLOP but communication, load imbalance and memory cost.',
 [('Why use a load-balancing loss?', 'To prevent all tokens from routing to a few experts.'),
  ('MQA versus GQA?', 'GQA interpolates between MHA and MQA.'),
  ('When choose an encoder?', 'Classification, retrieval, short-latency embeddings.')])

D['web-ml-063'] = T(
 'Dot-product attention scales scores by 1/sqrt(d_k) to keep their variance constant; full attention costs O(n^2); RoPE encodes relative position by rotating queries and keys.',
 'If q and k have independent entries of variance 1, q.k has variance d_k, so large d_k gives large scores and a saturated softmax with tiny gradients.',
 'Var(q.k) = d_k, so dividing by sqrt(d_k) gives variance 1. Complexity: the n x n score matrix needs O(n^2 d) compute and O(n^2) memory. Fixes: sparse or local attention (O(n w)), linear attention (O(n d^2)), FlashAttention (exact, memory O(n)), retrieval. RoPE rotates each pair of dimensions by an angle pos x theta_i: q_m = R_m q, k_n = R_n k, so q_m . k_n depends on (m - n).',
 'With d_k = 64 and unscaled scores of standard deviation 8, the softmax is nearly one-hot and gradients vanish; scaling restores standard deviation 1.',
 'RoPE extrapolates better than learned absolute positions and allows context extension via interpolation or NTK scaling; efficient attention variants trade exactness for speed.',
 [('Why O(n^2) memory?', 'Each of n queries scores all n keys.'),
  ('How does FlashAttention help?', 'Computes tiles in fast memory without storing the full matrix.'),
  ('What is relative position?', 'Attention depends on the offset between tokens.')])

D['web-ml-064'] = T(
 'Transformers use LayerNorm instead of BatchNorm because LayerNorm normalises each token independently of other examples and sequence positions.',
 'BatchNorm uses statistics across the batch (and positions), which is unreliable for variable-length sequences, small per-device batches and autoregressive inference, and differs between training and evaluation.',
 'BN: normalise each feature over the batch: (x - mu_B)/sigma_B with running averages at inference. LN: normalise over features of one token: (x - mu_token)/sigma_token. Padding tokens would pollute BN statistics; at inference with batch size 1, BN uses running averages that may mismatch.',
 'In a batch of sentences with lengths from 5 to 100 tokens, BN statistics mix real tokens with padding; LN gives each token the same treatment.',
 'LN costs a per-token reduction but has identical train and test behaviour; BN works well for CNNs with large batches. RMSNorm is a cheaper LN variant.',
 [('Does LN depend on batch size?', 'No.'),
  ('Where is LN placed?', 'Pre-LN before sublayers is more stable.'),
  ('Can BN work in transformers at all?', 'Possible (for example in ViTs) but less stable.')])

D['web-ml-065'] = T(
 'Data parallelism replicates the model and splits the batch; model parallelism splits the model (tensor or pipeline); collective operations (all-reduce, all-gather, reduce-scatter) synchronise the devices.',
 'The goal is to scale beyond one device\'s memory or speed while keeping communication overhead low.',
 'Data parallel: each of N workers computes gradients on B/N samples and all-reduces: g = (1/N) sum g_i; ring all-reduce moves about 2 (N - 1)/N x |g| bytes per worker. Tensor parallel splits matrices: for Y = X W with W split by columns, each device computes X W_i and an all-gather forms Y; row splits need an all-reduce. Pipeline parallel places layers on stages and uses micro-batches to fill the bubble. ZeRO/FSDP shard optimiser states, gradients and parameters (reduce-scatter and all-gather).',
 'A 70B model does not fit on one GPU: use FSDP across 64 GPUs combined with tensor parallelism inside a node (fast NVLink) and data parallelism across nodes.',
 'Data parallel is simplest but needs the model to fit; tensor parallel needs fast interconnect; pipeline reduces memory but has bubbles; combine them (3D parallelism). Overlap communication and computation, and use gradient accumulation or compression when bandwidth is limited.',
 [('What is all-reduce?', 'Every worker ends with the sum of all workers\' tensors.'),
  ('What is the pipeline bubble?', 'Idle time at the start and end of a step.'),
  ('What does ZeRO shard?', 'Optimiser states, then gradients, then parameters.')])

D['web-ml-066'] = T(
 'Math intuition in deep learning means being able to reason about shapes, gradients, scale and conditioning to predict why a model behaves as it does; transformers are the standard architecture to practise on.',
 'Most debugging questions reduce to: what do the dimensions look like, what is the gradient flow, and which quantity explodes or vanishes?',
 'Key facts: gradient of softmax cross-entropy wrt logits is p - y; dL/dW = x^T dL/dy for y = x W; initialisation Var(W) = 2/fan_in (He) or 2/(fan_in + fan_out) (Glorot) keeps activations stable; attention scores scale as sqrt(d); residual connections give an identity path so gradients are 1 + dF/dx; learning-rate and batch-size scale together (linear scaling rule).',
 'Case study: loss spikes in a transformer. Hypotheses: learning rate too high with Adam epsilon, missing gradient clipping, bf16 overflow in attention logits, bad data batch. Test each: clip at norm 1, lower the learning rate, check logit magnitude, find the offending batch.',
 'Build intuition by deriving small cases by hand and checking with code; use unit tests (gradient checks) and scale studies. Trade-offs concern stability versus speed (larger learning rates, lower precision).',
 [('Why scale initialisation by fan-in?', 'To keep activation variance constant across layers.'),
  ('What is the gradient of a matmul?', 'dX = dY W^T, dW = X^T dY.'),
  ('How to debug exploding loss?', 'Gradient norms, activation statistics, clipping, learning-rate warm-up.')])

D['web-ml-067'] = T(
 'Large language models are transformer-based neural networks trained on large text corpora to predict the next token; their behaviour comes from scale, data and post-training.',
 'Predicting the next token forces the model to learn grammar, facts and reasoning patterns; instruction tuning and preference training turn a raw predictor into an assistant.',
 'Pre-training minimises -sum_t log p(x_t | x_<t). Scaling laws: loss falls as a power law in parameters N, data D and compute C (Chinchilla: roughly 20 tokens per parameter for compute-optimal training). Inference: sampling with temperature T divides logits by T; top-k and top-p truncate the distribution. KV caching avoids recomputing past attention.',
 'A 7B model trained on 2T tokens beats a larger under-trained model; fine-tuning on 50k instruction examples makes it follow prompts.',
 'Bigger models are more capable but cost more to train and serve; quantisation, distillation and MoE reduce cost; hallucination, context limits and safety need retrieval, evaluation and guardrails.',
 [('What is temperature?', 'It sharpens (T < 1) or flattens (T > 1) the distribution.'),
  ('Why do LLMs hallucinate?', 'They optimise plausibility, not truth.'),
  ('What is in-context learning?', 'Adapting from examples in the prompt without weight updates.')])

D['web-ml-068'] = T(
 'Mixture-of-Experts (MoE) transformers replace the dense feed-forward layer with many expert FFNs and a router that sends each token to its top-k experts.',
 'Capacity (total parameters) grows with the number of experts while compute per token stays about constant, since only k experts run.',
 'y = sum_{e in TopK(g(x))} softmax(g(x))_e FFN_e(x), with router logits g(x) = W_r x. Load-balancing loss L_aux = N sum_e f_e P_e (f_e = fraction of tokens routed to e, P_e = mean router probability) discourages collapse. Capacity factor limits tokens per expert; overflow tokens are dropped or rerouted.',
 'Switch Transformer uses top-1 routing with up to thousands of experts; Mixtral uses 8 experts with top-2, giving about 3.6x more total parameters than active parameters.',
 'MoE gives better quality per FLOP but needs more memory, all-to-all communication under expert parallelism, and careful load balancing; fine-tuning and serving are harder than for dense models.',
 [('Why a load-balancing loss?', 'Otherwise the router collapses onto a few experts.'),
  ('What is expert parallelism?', 'Experts are placed on different devices with all-to-all token exchange.'),
  ('Dense versus MoE at the same FLOPs?', 'MoE has more parameters and usually better quality.')])

D['web-ml-069'] = T(
 'Tokenisation splits text into units (subwords) the model can embed; KL-regularised supervised fine-tuning (SFT) adds a penalty keeping the tuned model close to a reference model.',
 'Subword tokenisers balance vocabulary size and sequence length; KL regularisation prevents catastrophic forgetting and mode collapse during fine-tuning.',
 'BPE: start from characters and repeatedly merge the most frequent adjacent pair until the vocabulary size V is reached; unigram LM and WordPiece are alternatives; byte-level BPE covers any text. Design trade-offs: larger V gives shorter sequences but a bigger embedding matrix and rarer tokens. KL-regularised SFT: minimise -log p_theta(y | x) + beta KL(p_theta(. | x) || p_ref(. | x)), estimated per token as log p_theta(y_t) - log p_ref(y_t).',
 'Vocabulary 32k versus 128k: a multilingual model with 128k tokens produces about 20 to 30% fewer tokens for non-English text.',
 'Use byte-level BPE for robustness; tune V for the language mix; use KL regularisation when the SFT set is small or narrow, with beta chosen by validation of both task performance and retained general ability.',
 [('Why not word-level tokens?', 'Out-of-vocabulary words and huge vocabularies.'),
  ('Role of beta?', 'Larger beta keeps the model closer to the reference.'),
  ('How are numbers tokenised?', 'Often digit-wise to help arithmetic.')])

D['web-ml-070'] = T(
 'Text embeddings progressed from sparse counts and static word vectors (word2vec, GloVe) to contextual embeddings (ELMo, BERT) and sentence/document embeddings from LLMs.',
 'Static vectors give one vector per word; contextual models give a different vector per occurrence, resolving ambiguity ("bank").',
 'One-hot/TF-IDF: sparse, no similarity between synonyms. word2vec skip-gram maximises sum log sigma(u_c . v_w) with negative sampling; GloVe fits log co-occurrence. BERT embeddings: hidden states of a bidirectional transformer; sentence-BERT fine-tunes with contrastive losses so cosine similarity measures meaning: L = -log exp(sim(a, p)/tau)/sum_j exp(sim(a, n_j)/tau). Modern LLM embedding models (decoder-based) are trained contrastively on large pair datasets.',
 'Semantic search: embed documents with a sentence encoder and queries the same way, retrieve nearest neighbours by cosine similarity with an ANN index.',
 'Static embeddings are cheap but context-blind; contextual encoders are better but heavier; for retrieval use dedicated embedding models and check domain fit, dimension (storage cost) and latency.',
 [('Why contrastive training?', 'It shapes the space so that similar items are close.'),
  ('Dimension trade-off?', 'Larger dimension helps accuracy but costs memory; Matryoshka embeddings allow truncation.'),
  ('Cosine versus dot product?', 'Cosine for normalised vectors.')])

save('B_06.json')
