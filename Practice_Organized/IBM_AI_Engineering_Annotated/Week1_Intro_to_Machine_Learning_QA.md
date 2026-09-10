# Week 1 Quiz — Intro to Machine Learning
**Total points: 15** (5 questions × 3 points)

---

### Q1. Supervised learning deals with unlabeled data, while unsupervised learning deals with labelled data.
- ( ) True
- (●) **False**

**Why:** This has it backwards. **Supervised** learning uses **labeled** data (you have the
correct answer for each example during training). **Unsupervised** learning uses **unlabeled**
data (no correct answer is given; the model finds structure on its own, e.g. clustering).

---

### Q2. Which of the following is **not true** about Machine Learning?
- ( ) Machine Learning was inspired by the learning process of human beings.
- ( ) Machine Learning models iteratively learn from data, and allow computers to find hidden insights.
- ( ) Machine Learning models help us in tasks such as object recognition, summarization, and recommendation.
- (●) **Machine learning gives computers the ability to make decisions by writing down rules and methods and being explicitly programmed.**

**Why:** That description is **traditional/rule-based programming**, the opposite of ML. The
whole point of machine learning is that the computer **learns patterns from data** rather than
being handed explicit rules by a programmer.

---

### Q3. Which of the following groups are **not** Machine Learning techniques?
- ( ) Classification and Clustering
- (✅) **Numpy, Scipy and Scikit-Learn**
- ( ) Anomaly Detection and Recommendation Systems

**Why:** Classification, Clustering, Anomaly Detection, and Recommendation Systems are all
**ML techniques/tasks**. NumPy, SciPy, and Scikit-Learn are **Python libraries/tools** used to
implement ML — not techniques themselves.

---

### Q4. The "Regression" technique in Machine Learning is a group of algorithms that are used for:
- (●) **Predicting a continuous value; for example predicting the price of a house based on its characteristics.**
- ( ) Prediction of class/category of a case; for example a cell is benign or malignant, or a customer will churn or not.
- ( ) Finding items/events that often co-occur; for example grocery items that are usually bought together by a customer.

**Why:** Regression = predicting a **continuous numeric** output. The second option describes
**classification**; the third describes **association rule mining** (market-basket analysis).

---

### Q5. When comparing Supervised with Unsupervised learning: "In contrast to Supervised learning, Unsupervised learning has more models and more evaluation methods that can be used in order to ensure the outcome of the model is accurate." True or False?
- (●) **False**
- ( ) True

**Why:** It's actually the **opposite**. Supervised learning generally has **more** evaluation
methods available, because you have ground-truth labels to directly compare predictions
against (accuracy, precision/recall, etc.). Unsupervised learning is inherently **harder to
evaluate** since there's no "correct answer" to check against.
