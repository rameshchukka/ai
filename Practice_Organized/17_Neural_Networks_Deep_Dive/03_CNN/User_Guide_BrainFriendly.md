# Convolutional Neural Networks (CNNs) — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

CNNs use small sliding filters (kernels) to detect local patterns (edges, textures, shapes) in grid-like data such as images, then stack these into deeper, more abstract features.

## What You're About to Learn (and why it matters)

- Convolution operation: kernels, stride, padding
- Pooling layers (max/average) for downsampling
- Why CNNs need far fewer parameters than a fully-connected network on images
- A typical CNN architecture: conv → activation → pool, repeated, then a classifier head
- Transfer learning with a pretrained CNN backbone

## Before You Start — Quick Mindset Tips

- 💡 Start from a pretrained backbone (transfer learning) unless you have a very large dataset — it's almost always faster and better.
- 💡 Padding='same' keeps spatial dimensions unchanged, which simplifies architecture design.
- 💡 Data augmentation (flips, crops, color jitter) is one of the highest-leverage tricks to fight overfitting on images.
- 💡 Visualize a few training images after augmentation — a broken augmentation pipeline is a common silent bug.

## Things That Trip People Up

- 🚧 Feeding un-normalized pixel values (0-255) directly into the network.
- 🚧 Mismatched input image size vs. what the pretrained backbone expects.

## Where You'll Actually Use This

- Image classification, object detection, defect/anomaly detection in manufacturing
- Medical image triage

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
