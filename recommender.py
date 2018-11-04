"""
This recommender system utilizes K-Nearest-Neighbors algorithm to generate
a list of translators with which a user will be most satisfied with based
on ratings from similar users. It is dedicated for maximal user utility.
"""

from sklearn.neighbors import NearestNeighbors
import numpy as np

# Rows are users and columns are translators.
# A_{ij} indicates the computed rating the i^{th} user gives to the j^{th} translator.
# Ratings are on 1 to 5 scale.
# For example, the 3rd user has given the 5th translator an average rating of 5.
user_ratings = [
    [2, 0, 0, 3, 0, 0, 0],
    [5, 0, 5, 5, 0, 4, 0],
    [0, 0, 0, 0, 5, 0, 0],
    [0, 0, 0, 0, 0, 4, 0],
    [0, 1, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 3]
]

user_names = [
    "George Washington",
    "John Adams",
    "Thomas Jefferson",
    "Abraham Lincoln",
    "Theodore Roosevelt",
    "Woodrow Wilson"
]

translator_names = [
    "Superman",
    "Batman",
    "Doctor Strange",
    "Thor",
    "Captain America",
    "John Denero",
    "Cal Golden Bear"
]

num_users = len(user_ratings)
num_translators = len(user_ratings[0])

avail = [1, 0, 1, 0, 1, 0, 1]

X = user_ratings
knn = NearestNeighbors().fit(X)

def add_user(name):
    user_names.append(name)
    num_users += 1
    user_ratings.append([0 for i in range(num_translators)])

def add_translator(name):
    translator_names.append(name)
    num_translators += 1
    for i in num_users:
        user_ratings[i].append(0)

def change_availability(t):
    avail[t] = 1 - avail[t]

def rate(n, u, t):
    user_ratings[u][t] = n

def recommend(old, new):
    return [i for i in range(num_translators) if (old[i] and not new[i])]

def generate_translators(rating, neighbors):
    recommend_list = []
    for n in neighbors[0]:
        never = recommend(user_ratings[n], rating)
        for tr in never:
            if tr not in recommend_list and avail[tr]:
                recommend_list.append(tr)
    return recommend_list

def display_result(user, lst):
    message = "The following translators will be recommended to {} in order:".format(user_names[user])
    for tr in lst:
        message += " " + translator_names[tr] + ","
    print(message[:len(message)-1] + ".")

rating = [1, 0, 1, 0, 0, 0, 0]
neighbors = knn.kneighbors([rating], n_neighbors=6, return_distance=False)
recommend_list = generate_translators(rating, neighbors)
print(recommend_list)
display_result(5, recommend_list)

a = eval(input("Now type in a new user rating:\n"))
a_neighbors = knn.kneighbors([a], n_neighbors=6, return_distance=False)
a_rec_list = generate_translators(a, a_neighbors)
print(a_rec_list)
display_result(5, a_rec_list)
