# Week 5 Quiz — Recommender System
**Total points: 15** (5 questions × 3 points)

---

### Q1. What is/are the advantage/s of Recommender Systems?
- ( ) Recommender Systems provide a better experience for the users by giving them a broader exposure to many different products they might be interested in.
- ( ) Recommender Systems encourage users towards continual usage or purchase of their product
- ( ) Recommender Systems benefit the service provider by increasing potential revenue and better security for its consumers.
- (●) **All of the above.**

**Why:** All three listed benefits are genuine advantages of recommender systems — better user
experience through discovery, increased engagement/usage, and increased revenue for the
provider.

---

### Q2. What is a **content-based** recommendation system?
- (●) **Content-based recommendation system tries to recommend items to the users based on their profile built upon their preferences and taste.**
- ( ) Content-based recommendation system tries to recommend items based on similarity among items.
- ( ) Content-based recommendation system tries to recommend items based on the similarity of users when buying, watching, or enjoying something.
- ( ) All of above.

**Why:** Content-based filtering builds a **profile of the user's own preferences/taste** (from
what they've liked/interacted with before) and recommends similar items. The other options
describe different approaches: item-similarity is closer to item-based collaborative
filtering, and user-similarity describes user-based collaborative filtering.

---

### Q3. What is the meaning of "Cold start" in collaborative filtering?
- ( ) The difficulty in recommendation when we do not have enough ratings in the user-item dataset.
- (●) **The difficulty in recommendation when we have a new user, and we cannot make a profile for him, or when we have a new item, which has not got any rating yet.**
- ( ) The difficulty in recommendation when the number of users or items increases and the amount of data expands, so algorithms will begin to suffer drops in performance.

**Why:** "Cold start" specifically refers to the **new user / new item** problem — there's no
history yet to build a profile or gather ratings from. (The third option describes a
**scalability** problem, a different, separate challenge from cold start.)

---

### Q4. What is a "Memory-based" recommender system?
- (●) **In memory based approach, we use the entire user-item dataset to generate a recommendation system.**
- ( ) In memory based approach, a model of users is developed in attempt to learn their preferences.
- ( ) In memory based approach, a recommender system is created using machine learning techniques such as regression, clustering, classification, etc.

**Why:** Memory-based approaches work directly off the **entire raw historical dataset** (e.g.
computing similarities directly between users or items) rather than training a learned model.
The other two options actually describe **model-based** approaches, which DO build a trained
model (via regression, clustering, etc.) to learn user preferences — the opposite of
memory-based.

---

### Q5. What is the shortcoming of content-based recommender systems?
- ( ) As it is based on similarity among items and users, it is not easy to find the neighbour users.
- ( ) It needs to find similar group of users, so suffers from drops in performance, simply due to growth in the similarity computation.
- (●) **Users will only get recommendations related to their preferences in their profile, and recommender engine may never recommend any item with other characteristics.**

**Why:** This describes the classic "**filter bubble**" limitation of content-based
filtering — since it only recommends based on a user's own established profile/preferences,
it struggles to suggest genuinely novel items outside what the user has already shown interest
in, unlike collaborative filtering which can surface unexpected items liked by similar users.
