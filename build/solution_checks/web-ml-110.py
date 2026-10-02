import math

class Value:
    def __init__(self, data, parents=(), op=''):
        self.data, self.grad = float(data), 0.0
        self._parents, self._backward = parents, lambda: None

    def __add__(self, o):
        o = o if isinstance(o, Value) else Value(o)
        out = Value(self.data + o.data, (self, o))
        def _b():
            self.grad += out.grad
            o.grad += out.grad
        out._backward = _b
        return out

    def __mul__(self, o):
        o = o if isinstance(o, Value) else Value(o)
        out = Value(self.data * o.data, (self, o))
        def _b():
            self.grad += o.data * out.grad
            o.grad += self.data * out.grad
        out._backward = _b
        return out

    def __pow__(self, k):
        out = Value(self.data ** k, (self,))
        def _b():
            self.grad += k * self.data ** (k - 1) * out.grad
        out._backward = _b
        return out

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,))
        def _b():
            self.grad += (1 - t * t) * out.grad
        out._backward = _b
        return out

    def backward(self):
        order, seen = [], set()
        def visit(v):
            if id(v) not in seen:
                seen.add(id(v))
                for p in v._parents:
                    visit(p)
                order.append(v)
        visit(self)
        self.grad = 1.0
        for v in reversed(order):
            v._backward()

x, y = Value(2.0), Value(-3.0)
z = x * y + x ** 2 + x           # z = xy + x^2 + x; dz/dx = y + 2x + 1 = 2, dz/dy = x = 2
z.backward()
assert z.data == -6 + 4 + 2 and x.grad == 2.0 and y.grad == 2.0
a = Value(0.5)
b = (a * a).tanh()
b.backward()
assert abs(a.grad - (1 - math.tanh(0.25) ** 2) * 2 * 0.5) < 1e-12
print("ok")
