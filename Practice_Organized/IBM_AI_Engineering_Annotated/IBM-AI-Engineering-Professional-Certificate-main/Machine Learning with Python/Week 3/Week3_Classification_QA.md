# Week 3 Quiz — Classification
**Total points: 15** (5 questions × 3 points)

---

### Q1. Which one **IS NOT** a sample of classification problem?
- ( ) To predict the category to which a customer belongs to.
- ( ) To predict whether a customer switches to another provider/brand.
- (●) **To predict the amount of money a customer will spend in one year.**
- ( ) To predict whether a customer responds to a particular advertising campaign or not.

**Why:** Predicting an **amount of money** is a continuous numeric value — that's a
**regression** problem, not classification. The other three all predict a discrete
category/class (which segment, switch or not, respond or not).

---

### Q2. Which of the following statements are **TRUE** about Logistic Regression? *(select all that apply)*
- (✅) **Logistic regression can be used both for binary classification and multi-class classification**
- (✅) **Logistic regression is analogous to linear regression but takes a categorical/discrete target field instead of a numeric one.**
- (✅) **In logistic regression, the dependent variable is binary.**

**Why:** Logistic regression predicts a **categorical/discrete** outcome (unlike linear
regression's continuous output) and, in its classic/base form, the target is binary
(yes/no, 0/1) — it can also be extended to multi-class problems (e.g. via one-vs-rest).

---

### Q3. Which of the following examples is/are a sample application of Logistic Regression? *(select all that apply)*
- (✅) **The probability that a person has a heart attack within a specified time period using person's age and sex.**
- (✅) **Customer's propensity to purchase a product or halt a subscription in marketing applications.**
- (✅) **Likelihood of a homeowner defaulting on a mortgage.**
- ( ) Estimating the blood pressure of a patient based on her symptoms and biographical data.

**Why:** The first three all predict a **probability/likelihood of a discrete outcome**
(heart attack yes/no, churn yes/no, default yes/no) — classic logistic regression territory.
Estimating blood pressure is a **continuous value**, correctly excluded — that's regression.

---

### Q4. Which one is **TRUE** about the kNN algorithm?
- ( ) kNN is a classification algorithm that takes a bunch of unlabelled points and uses them to learn how to label other points.
- (●) **kNN algorithm can be used to estimate values for a continuous target.**

**Why:** kNN uses **labeled** points (not unlabeled — that would describe clustering), so the
first option is wrong. kNN can indeed be used for **regression** too (predicting a continuous
value by averaging the values of the k nearest neighbors), not just classification — making
the second statement true.

---

### Q5. What is "information gain" in decision trees?
- ( ) It is the information that can decrease the level of certainty after splitting in each node.
- (●) **It is the entropy of a tree before split minus weighted entropy after split by an attribute.**
- ( ) It is the amount of information disorder, or the amount of randomness in each node.

**Why:** Information gain is formally defined as **entropy before the split minus the
weighted entropy after the split**. (The third option is actually describing plain
**entropy** itself, not information gain — a common thing to mix up.)
