# Week 2 Quiz — Regression
**Total points: 15** (5 questions × 3 points)

---

### Q1. Multiple Linear Regression is appropriate for:
- ( ) Predicting the sales amount based on month
- ( ) Predicting whether a drug is effective for a patient based on her characteristics
- (●) **Predicting tomorrow's rainfall amount based on the wind speed and temperature**

**Why:** Multiple Linear Regression needs **more than one independent variable** predicting
ONE continuous outcome. "Sales based on month" uses only one predictor (simple, not multiple,
regression). "Drug effective or not" is a categorical (yes/no) outcome — that's
**classification**, not regression. Rainfall predicted from wind speed AND temperature fits
perfectly: two independent variables, one continuous dependent variable.

---

### Q2. Which of the following is the meaning of "Out of Sample Accuracy" in the context of evaluation of models?
- (●) **"Out of Sample Accuracy" is the percentage of correct predictions that the model makes on data that the model has NOT been trained on.**
- ( ) "Out of Sample Accuracy" is the accuracy of an overly trained model (which may captured noise and produced a non-generalized model)

**Why:** Out-of-sample accuracy specifically measures performance on **unseen** data (like a
held-out test set) — it's the honest measure of how well a model generalizes, as opposed to
in-sample accuracy (on training data), which can look artificially high if the model overfit.

---

### Q3. When should we use Multiple Linear Regression? *(select all that apply)*
- (✅) **When we would like to identify the strength of the effect that the independent variables have on a dependent variable.**
- ( ) When there are multiple dependent variables
- (✅) **When we would like to predict impacts of changes in independent variables on a dependent variable.**

**Why:** Multiple Linear Regression has **multiple independent variables** but only **ONE
dependent variable** — "multiple dependent variables" is a common trap/misconception and is
correctly NOT selected. The two correct uses are about understanding/predicting how several
inputs affect one output.

---

### Q4. Which of the following statements are **TRUE** about Polynomial Regression? *(select all that apply)*
- (✅) **Polynomial regression can use the same mechanism as Multiple Linear Regression to find the parameters.**
- (✅) **Polynomial regression fits a curve line to your data.**
- (✅) **Polynomial regression models can fit using the Least Squares method.**

**Why:** All three are true. Polynomial regression fits a **curved** line, but because it's
still *linear in its parameters* (the coefficients), it can be solved with the exact same Least
Squares machinery as ordinary linear regression — this is a subtle but important point: "linear
regression" refers to linearity in the parameters, not the shape of the fitted curve.

---

### Q5. Which sentence is **NOT TRUE** about Non-linear Regression?
- ( ) Nonlinear regression is a method to model non linear relationship between the dependent variable and a set of independent variables.
- ( ) For a model to be considered non-linear, y must be a non-linear function of the parameters.
- (●) **Non-linear regression must have more than one dependent variable.**

**Why:** Like linear regression, non-linear regression still has **ONE** dependent variable —
"non-linear" describes the shape of the relationship/function, not the number of outputs. This
is the false statement, correctly identified.
