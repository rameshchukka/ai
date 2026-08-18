# 📓 My Course Practice Notebooks — PyTorch Fundamentals

Your uploaded PyTorch course notebooks, reviewed, bug-fixed, verified end-to-end, and extended
with two additional notebooks to complete the neural-network learning arc.

## Review Verdict

Two of your four notebooks were **excellent as-is** — real datasets, correct code, well
commented, no changes needed:

| Notebook | Verdict |
|---|---|
| `03_pytorch_training_pipeline_using_nn_module.ipynb` | ✅ Excellent, no changes. Real breast-cancer dataset, correct standardization → label encoding → tensor pipeline, BCELoss training loop with train/val loss & accuracy tracking, TensorBoard logging, single-sample inference. |
| `05_ann_fashion_mnist_pytorch_gpu.ipynb` | ✅ Excellent, one portability fix. GPU-aware, custom Dataset/DataLoader, a real ANN with correct training/eval loop, model save/load, and a genuinely polished learning-curve plot. |

Two had real bugs that would crash on a fresh run — **fixed and verified**:

| Notebook | Bug found | Fix applied |
|---|---|---|
| `02_pytorch_nn_module.ipynb` | `features` used before it was defined (cell order); two `Model` classes with the same name silently overwrote each other, breaking a later cell that expected the first one's `.network` attribute | Reordered the `features` cell to come first; renamed the two classes to `ModelSequential` and `ModelManual` so both stay usable side by side, matching what the notebook was clearly trying to teach (two ways to define the same architecture) |
| `04_dataset_and_dataloader_demo.ipynb` | `for epoch in epochs:` — `epochs=25` is an int, not iterable, so this line **crashes** with `TypeError: 'int' object is not iterable` | Fixed to `for epoch in range(epochs):`, and completed the loop into a real (small) working training step, since the commented-out `#model = custmode(2)` line showed that was the original intent |
| `05_ann_fashion_mnist_pytorch_gpu.ipynb` | Hardcoded absolute Windows path (`H:\01_Training\...\fmnist_small.csv`) — only runs on that one machine | Made the loader portable: looks for `fmnist_small.csv` next to the notebook first (use your real Fashion-MNIST CSV there for real results), and falls back to a small synthetic placeholder with the same shape so the notebook runs anywhere out of the box |

Every notebook (`02`–`07`) was verified by executing every cell top-to-bottom in a fresh
namespace — no crashes, no undefined variables, no stale state.

## Extended: Two New Notebooks to Complete the Arc

Your original set went straight from a basic ANN (`02`) through a full training pipeline
(`03`, `04`) to a GPU-trained ANN on real image data (`05`). Two concepts that any "learn
neural networks" path needs weren't covered yet, so I added them in the same style
(heavily-commented cells, GPU-aware, same Fashion-MNIST dataset for continuity):

- **`06_regularization_dropout_batchnorm.ipynb`** — deliberately overfits a model first (small
  dataset + some corrupted training labels + high capacity, so memorization is easy to induce
  and visible in the numbers), then fixes it with `nn.Dropout` and `nn.BatchNorm1d`, comparing
  all three side by side with train/test loss curves. Includes a note on a genuine
  Dropout quirk: its own train loss can look *higher* than test loss, because Dropout is only
  active during training.
- **`07_cnn_fashion_mnist_pytorch_gpu.ipynb`** — the natural next step after `05`'s ANN: the
  same dataset and training/eval/save/load structure, but with `nn.Conv2d` + `nn.MaxPool2d`
  layers instead of flattening every image to a vector. Ends with a direct parameter-count
  comparison against the ANN, showing convolution's parameter-sharing advantage.

## Suggested Order

```
02  ->  03  ->  04  ->  05  ->  06  ->  07
nn.Module    training      DataLoader    ANN on real     Dropout &      CNN on the
basics       pipeline      + batching    image data      BatchNorm      same data
                                         (GPU-aware)     (fixes         (parameter
                                                          overfitting)   sharing)
```

## How This Relates to the Zero-to-Hero Series

This folder is **your own course material** (kept separate from the auto-generated content).
If you want the from-scratch mathematical treatment of the same ideas — autograd, the training
loop, backpropagation's chain rule, why CNNs use convolution — see
`../../Zero_to_Hero_Series/04_PyTorch_Zero_to_Hero/` and
`../../Concept_Guides/04_Neural_Networks_Backpropagation_Concept_Guide.pdf`. The two sets
complement each other: this folder is applied, dataset-driven practice; the Zero-to-Hero lab
and concept guide build the same ideas up from first principles.

## Using Your Own Real Fashion-MNIST Data

Notebooks `05`, `06`, and `07` all look for `fmnist_small.csv` in the same folder as the
notebook. Download the real Fashion-MNIST CSV (small/sample version, e.g. from Kaggle) and
place it there to get meaningful accuracy numbers — without it, every notebook still runs
correctly using a small synthetic placeholder dataset generated on the fly.
