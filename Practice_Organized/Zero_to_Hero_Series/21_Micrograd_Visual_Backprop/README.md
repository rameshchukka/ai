# 🔥 Micrograd: See Forward Pass & Backprop, Don't Just Read About Them

Inspired directly by Andrej Karpathy's micrograd and his 'spelled-out intro to neural networks and backpropagation' video. Build a real, correct autograd engine from complete scratch (~40 lines), rendering the computation graph after every step so you WATCH forward values and gradients flow, instead of reading formulas. Ends with an exact numerical match against real PyTorch.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. Forward pass, by hand, on paper-simple numbers
2. Wrapping numbers in a Value -- and drawing the graph
3. Manual backprop on ONE multiplication (before any automation)
4. Manual backprop on TWO steps (the chain rule, made visible)
5. Automating it: local gradient rules for +, *, **, tanh
6. The backward() method: topological sort, then one pass
7. Watching gradients flow: data AND grad on the same rendered graph
8. Building a Neuron, a Layer, and a tiny MLP out of Value
9. Training the MLP on a toy dataset -- watch the loss curve fall
10. 🏆 Capstone: verify your engine against real PyTorch, prove it's correct

## Requirements
```
pip install graphviz torch matplotlib   # also needs the system 'dot' binary (apt install graphviz / brew install graphviz)
```

Directly references: https://github.com/karpathy/micrograd and Karpathy's YouTube video 'The spelled-out intro to neural networks and backpropagation: building micrograd'. Capstone verified: gradients match real PyTorch's autograd to 1e-6 precision on a nontrivial expression.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
