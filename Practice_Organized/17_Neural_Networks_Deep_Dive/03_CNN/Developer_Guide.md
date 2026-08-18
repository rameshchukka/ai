# Convolutional Neural Networks (CNNs) — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

CNNs use small sliding filters (kernels) to detect local patterns (edges, textures, shapes) in grid-like data such as images, then stack these into deeper, more abstract features.

## What You Will Learn

- Convolution operation: kernels, stride, padding
- Pooling layers (max/average) for downsampling
- Why CNNs need far fewer parameters than a fully-connected network on images
- A typical CNN architecture: conv → activation → pool, repeated, then a classifier head
- Transfer learning with a pretrained CNN backbone

## Important Pointers / Tips

- **Tip:** Start from a pretrained backbone (transfer learning) unless you have a very large dataset — it's almost always faster and better.
- **Tip:** Padding='same' keeps spatial dimensions unchanged, which simplifies architecture design.
- **Tip:** Data augmentation (flips, crops, color jitter) is one of the highest-leverage tricks to fight overfitting on images.
- **Tip:** Visualize a few training images after augmentation — a broken augmentation pipeline is a common silent bug.

## Common Pitfalls

- ⚠️ Feeding un-normalized pixel values (0-255) directly into the network.
- ⚠️ Mismatched input image size vs. what the pretrained backbone expects.

## Real-World Use Cases

- Image classification, object detection, defect/anomaly detection in manufacturing
- Medical image triage

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
