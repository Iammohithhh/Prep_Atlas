import math
import torch
import torch.nn.functional as F

def causal_attention(q, k, v):
    T, d = q.shape[-2], q.shape[-1]
    scores = q @ k.transpose(-2, -1) / math.sqrt(d)
    mask = torch.tril(torch.ones(T, T, dtype=torch.bool, device=q.device))
    scores = scores.masked_fill(~mask, float('-inf'))
    return torch.softmax(scores, dim=-1) @ v

torch.manual_seed(0)
q, k, v = (torch.randn(2, 4, 5, 8) for _ in range(3))
out = causal_attention(q, k, v)
ref = F.scaled_dot_product_attention(q, k, v, is_causal=True)
assert torch.allclose(out, ref, atol=1e-5)
v2 = v.clone(); v2[..., 3:, :] += 10                 # change future values
assert torch.allclose(causal_attention(q, k, v2)[..., :3, :], out[..., :3, :])
print("ok")
