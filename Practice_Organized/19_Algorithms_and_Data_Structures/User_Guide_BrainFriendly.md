# Algorithms & Data Structures — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

The core computer-science toolkit underneath efficient code: how to reason about time/space complexity, and the standard structures/algorithms that show up constantly in interviews and in real system design.

## What You're About to Learn (and why it matters)

- Big-O notation: time and space complexity
- Core data structures: array, linked list, stack, queue, hash map, tree, graph
- Sorting algorithms (merge sort, quick sort) and searching (binary search)
- Recursion and when to reach for it
- Basic graph traversal: BFS and DFS
- Dynamic programming: recognizing overlapping subproblems

## Before You Start — Quick Mindset Tips

- 💡 Before optimizing, get a brute-force solution working — correctness first, performance second.
- 💡 A hash map turns most 'have I seen this before / count occurrences' problems into O(n).
- 💡 If a problem mentions 'shortest path' or 'connected components', think graph + BFS/DFS.
- 💡 If you see overlapping subproblems, sketch the recursive solution first, then memoize it (top-down DP) before considering an iterative table (bottom-up DP).

## Things That Trip People Up

- 🚧 Ignoring the space complexity of a recursive solution's call stack.
- 🚧 Reaching for a complex algorithm when a simpler O(n log n) sort + scan solves it.

## Where You'll Actually Use This

- System design interviews and technical interviews generally
- Writing efficient data-processing code that scales to production-size inputs
- Understanding why certain library functions (e.g., dict lookups) are fast

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
