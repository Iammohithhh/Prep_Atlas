import math
import torch
import torch.nn as nn

class MultiHeadSelfAttention(nn.Module):
    def __init__(self, d_model, n_heads, causal=False):
        super().__init__()
        assert d_model % n_heads == 0
        self.h, self.dh, self.causal = n_heads, d_model // n_heads, causal
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.out = nn.Linear(d_model, d_model)

    def forward(self, x):
        B, T, D = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        q, k, v = (t.view(B, T, self.h, self.dh).transpose(1, 2) for t in (q, k, v))
        s = q @ k.transpose(-2, -1) / math.sqrt(self.dh)
        if self.causal:
            mask = torch.tril(torch.ones(T, T, dtype=torch.bool, device=x.device))
            s = s.masked_fill(~mask, float('-inf'))
        y = torch.softmax(s, dim=-1) @ v
        return self.out(y.transpose(1, 2).reshape(B, T, D))

torch.manual_seed(0)
m = MultiHeadSelfAttention(16, 4, causal=True)
x = torch.randn(2, 6, 16)
y = m(x)
assert y.shape == (2, 6, 16)
y2 = m(x[:, :4])
assert torch.allclose(y[:, :4], y2, atol=1e-5)          # causal
ref = torch.nn.functional.scaled_dot_product_attention(
    *(t.view(2, 6, 4, 4).transpose(1, 2) for t in m.qkv(x).chunk(3, -1)), is_causal=True)
assert ref.shape == (2, 4, 6, 4)
print("ok")
