__author__ = 'Lalitha Venkatasubramanian'

'''
how to build a recommendation system using pandas, scikit-learn, and numpy.
We've provided a dataset of beer reviews which we'll use for building our product recommender,
but this use case could be easily substituted with a different product.
'''


''' 

'''










import pandas as pd   # used mostly to operate tabular data
import numpy as np    # for complex mathematical operations
import pylab as pl    # this is used for graphic representation

'''
Download the data
'''

# substitute your name here. If you're on windows you'll need a different filepath
df=pd.read_csv("C:/Users/Kirthivasan/Documents/Lalitha_Python/Python/beer_reviews.csv")
#df = pd.read_csv("C:/Users/dell/Documents/Products/Python/DEBAPRIYA/Beer Reccomendation System/beer_reviews/beer_reviews.csv")
df.head() # display top 10 values

'''
Finding People Who Have Reviewed 2 Beers

'''



# beer_1, beer_2 = abc2.sample(), abc.sample()

beer_1, beer_2 = "Dale's Pale Ale", "Fat Tire Amber Ale" # idealy it should be random beer name from abc2 but we have 1 example


beer_1_reviewers = df[df.beer_name==beer_1].review_profilename.unique()

beer_2_reviewers = df[df.beer_name==beer_2].review_profilename.unique()

common_reviewers = set(beer_1_reviewers).intersection(beer_2_reviewers) # to find the common reviewers

print "Users in the sameset: %d" % len(common_reviewers) # total no common reviewers

list(common_reviewers)[:10]      # print first 10 elements of common reviewers set


'''
Extracting Reviews
'''

def get_beer_reviews(beer, common_users):
    mask = (df.review_profilename.isin(common_users)) & (df.beer_name==beer)
    reviews = df[mask].sort('review_profilename')
    reviews = reviews[reviews.review_profilename.duplicated()==False]
    return reviews

beer_1_reviews = get_beer_reviews(beer_1, common_reviewers)
beer_2_reviews = get_beer_reviews(beer_2, common_reviewers)

cols = ['beer_name', 'review_profilename', 'review_overall', 'review_aroma', 'review_palate', 'review_taste']
beer_2_reviews[cols].head()


'''
Calculating Distance
'''

# choose your own way to calculate distance
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import manhattan_distances
from scipy.stats.stats import pearsonr


ALL_FEATURES = ['review_overall', 'review_aroma', 'review_palate', 'review_taste']

def calculate_similarity(beer1, beer2):
    # find common reviewers
    beer_1_reviewers = df[df.beer_name==beer1].review_profilename.unique()
    beer_2_reviewers = df[df.beer_name==beer2].review_profilename.unique()
    common_reviewers = set(beer_1_reviewers).intersection(beer_2_reviewers)


    # get reviews
    beer_1_reviews = get_beer_reviews(beer1, common_reviewers)
    beer_2_reviews = get_beer_reviews(beer2, common_reviewers)
    dists = []
    for f in ALL_FEATURES:
        dists.append(euclidean_distances(beer_1_reviews[f], beer_2_reviews[f])[0][0])

    return dists

calculate_similarity(beer_1, beer_2)


'''
Calculate the Similarity for a Set of Beers
'''

# calculate only a subset for the demo
beers = ["Dale's Pale Ale", "Sierra Nevada Pale Ale", "Michelob Ultra",
         "Natural Light", "Bud Light", "Fat Tire Amber Ale", "Coors Light",
         "Blue Moon Belgian White", "60 Minute IPA", "Guinness Draught"]

# calculate everything for real production
# beers = df.beer_name.unique()

simple_distances = []
for beer1 in beers:
    print "starting", beer1
    for beer2 in beers:
        if beer1 != beer2:
            row = [beer1, beer2] + calculate_similarity(beer1, beer2)
            simple_distances.append(row)
'''
Inspect the Results
'''

cols = ["beer1", "beer2", "overall_dist", "aroma_dist", "palate_dist", "taste_dist"]
simple_distances = pd.DataFrame(simple_distances, columns=cols)
simple_distances.tail()
'''
Allow the User to Customize the Weights
'''

def calc_distance(dists, beer1, beer2, weights):
    mask = (dists.beer1==beer1) & (dists.beer2==beer2)
    row = dists[mask]
    row = row[['overall_dist', 'aroma_dist', 'palate_dist', 'taste_dist']]
    dist = weights * row
    return dist.sum(axis=1).tolist()[0]

weights = [2, 1, 1, 1]
print('Dales Pale Ale : ')
print calc_distance(simple_distances, "Fat Tire Amber Ale", "Dale's Pale Ale", weights)
print ('Michelob Ultra : ')
print calc_distance(simple_distances, "Fat Tire Amber Ale", "Michelob Ultra", weights)


'''
Find Similar Beers for 'Coors Light'
'''
my_beer = "Coors Light"
results = []
for b in beers:
    if my_beer!=b:
        results.append((my_beer, b, calc_distance(simple_distances, my_beer, b, weights)))
sorted(results, key=lambda x: x[2])

