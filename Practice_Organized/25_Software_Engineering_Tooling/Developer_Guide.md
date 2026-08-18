# Software Engineering Tooling for AI/ML Systems — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

The general software-engineering skills that make an ML/AI project into a real, maintainable system: API design, caching, async communication between services, reusable design patterns, efficient data structures, cloud/deployment basics, and observability.

## What You Will Learn

- REST API design principles (resource naming, status codes, versioning)
- Caching strategies (in-memory LRU, and where Redis-style caches fit in)
- Message queues / pub-sub concepts (decoupling producers and consumers, e.g. Kafka/RabbitMQ)
- Core design patterns: Singleton, Factory, Observer — and when each earns its complexity
- Efficient data structures beyond the basics: heaps/priority queues, tries, graph representations
- Cloud & deployment basics: containers, CI/CD pipelines, Kubernetes concepts
- Auth/security basics (OAuth/JWT) and logging/monitoring for production systems
- Web scraping and regular expressions for unstructured data extraction

## Important Pointers / Tips

- **Tip:** Design REST endpoints around resources ('/orders/{id}') not actions ('/getOrder') — this is the core REST convention.
- **Tip:** An LRU cache turns 'expensive to recompute, same input repeated often' into a fast lookup — implement it with an OrderedDict before reaching for external tools.
- **Tip:** Message queues decouple services in time — the producer doesn't need the consumer to be online right now, which is the whole point.
- **Tip:** Don't reach for a design pattern because it's 'best practice' — reach for it when you feel the specific pain it solves (e.g., Observer when many things need to react to one event).
- **Tip:** A heap gives O(log n) insert and O(1) peek-min — the standard tool for 'always process the smallest/highest-priority item next'.
- **Tip:** Write regex incrementally and test against edge cases; an untested regex is a common source of silent data-parsing bugs.

## Common Pitfalls

- ⚠️ Over-engineering a small script with design patterns it doesn't need.
- ⚠️ Caching without an invalidation strategy — stale cached data silently served forever.
- ⚠️ Storing JWTs insecurely (e.g., in localStorage) or never expiring/rotating them.
- ⚠️ Regex that works on the happy-path example but breaks on real-world messy input.

## Real-World Use Cases

- Designing a clean internal API for an ML model-serving service
- Caching repeated LLM/embedding calls to cut cost and latency
- Decoupling an ingestion pipeline from a processing pipeline with a queue
- Extracting structured fields (emails, prices, dates) from unstructured text with regex

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
