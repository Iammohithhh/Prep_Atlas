import torch
import torch.nn as nn

class FFNWithBN(nn.Module):
    def __init__(self, d, hidden):
        super().__init__()
        self.fc1, self.fc2 = nn.Linear(d, hidden), nn.Linear(hidden, d)
        self.bn = nn.BatchNorm1d(d)

    def forward(self, x):                       # x: (B, T, D)
        y = self.fc2(torch.relu(self.fc1(x)))
        B, T, D = y.shape
        y = self.bn((x + y).reshape(B * T, D)).reshape(B, T, D)
        return y

def train_step(model, opt, x, target, loss_fn):
    model.train()
    opt.zero_grad()
    loss = loss_fn(model(x), target)
    loss.backward()
    opt.step()
    return loss.item()

torch.manual_seed(0)
m = FFNWithBN(8, 16)
opt = torch.optim.SGD(m.parameters(), lr=0.1)
x, tgt = torch.randn(4, 5, 8), torch.randn(4, 5, 8)
before = [p.clone() for p in m.parameters()]
l0 = train_step(m, opt, x, tgt, nn.MSELoss())
assert any(not torch.equal(a, b) for a, b in zip(before, m.parameters()))
for _ in range(50):
    l1 = train_step(m, opt, x, tgt, nn.MSELoss())
assert l1 < l0
m.eval()
with torch.no_grad():
    a, b = m(x), m(x)
assert torch.allclose(a, b) and not m.bn.training
print("ok")
