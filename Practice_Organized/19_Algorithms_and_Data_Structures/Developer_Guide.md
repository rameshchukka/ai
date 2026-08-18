# Algorithms & Data Structures — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

The core computer-science toolkit underneath efficient code: how to reason about time/space complexity, and the standard structures/algorithms that show up constantly in interviews and in real system design.

## What You Will Learn

- Big-O notation: time and space complexity
- Core data structures: array, linked list, stack, queue, hash map, tree, graph
- Sorting algorithms (merge sort, quick sort) and searching (binary search)
- Recursion and when to reach for it
- Basic graph traversal: BFS and DFS
- Dynamic programming: recognizing overlapping subproblems

## Important Pointers / Tips

- **Tip:** Before optimizing, get a brute-force solution working — correctness first, performance second.
- **Tip:** A hash map turns most 'have I seen this before / count occurrences' problems into O(n).
- **Tip:** If a problem mentions 'shortest path' or 'connected components', think graph + BFS/DFS.
- **Tip:** If you see overlapping subproblems, sketch the recursive solution first, then memoize it (top-down DP) before considering an iterative table (bottom-up DP).

## Common Pitfalls

- ⚠️ Ignoring the space complexity of a recursive solution's call stack.
- ⚠️ Reaching for a complex algorithm when a simpler O(n log n) sort + scan solves it.

## Real-World Use Cases

- System design interviews and technical interviews generally
- Writing efficient data-processing code that scales to production-size inputs
- Understanding why certain library functions (e.g., dict lookups) are fast

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
