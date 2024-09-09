import streamlit as st
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

# Load Data (Here you would replace this with the actual data loading mechanism)
@st.cache
def load_data():
    # Load your dataset (Assume the dataset is preprocessed as pivot_df)
    data_path = 'https://raw.githubusercontent.com/your-username/your-repo/main/amazon_reviews.csv'
    df = pd.read_csv(data_path)
  # Update with actual path
    df = pd.read_csv(data_path)
    return df

st.title("Amazon Food Recommendation System 🍲🍱🥘")
st.write("This app provides food recommendations based on Amazon reviews!")

# Load the dataset
df = load_data()

st.write("## Dataset Preview")
st.dataframe(df.head())  # Show a preview of the data

# Pivot table based on user-item interactions (adjust based on your notebook logic)
pivot_df = df.pivot_table(index='userId', columns='productId', values='rating', fill_value=0)

# Displaying a basic description of the pivot table
st.write("### Pivot Table Preview")
st.dataframe(pivot_df.head())

# Perform Singular Value Decomposition (SVD)
st.write("## Performing Singular Value Decomposition (SVD)...")

# Create sparse matrix
pivot_sparse = csr_matrix(pivot_df.values)

# SVD
U, sigma, Vt = svds(pivot_sparse, k=50)

# Convert sigma to diagonal matrix
sigma = np.diag(sigma)

# Calculate predicted ratings
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)

# Convert to DataFrame
preds_df = pd.DataFrame(all_user_predicted_ratings, columns=pivot_df.columns)

st.write("## Predicted Ratings for Users")
st.dataframe(preds_df.head())

# User-based Recommendation
st.write("## User-based Recommendations")

# Select user
user_id = st.selectbox("Select User ID:", pivot_df.index)

# Recommend top 5 products
sorted_user_predictions = preds_df.loc[user_id].sort_values(ascending=False)

st.write(f"### Top 5 recommendations for User {user_id}:")
top_5_recommendations = sorted_user_predictions.head(5)
st.write(top_5_recommendations)

# Footer
st.write("Made with ❤️ using Streamlit.")


# -*- coding: utf-8 -*-
"""Recommendation based on Amazon food Review

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15phcJQn_7wk-m1Kcu3_igj3o-pWpb2d3
"""

pip install streamlit pandas numpy scipy

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'amazon-fine-food-reviews:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F18%2F2157%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240909%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240909T122756Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D652ed83150a2af8d74d44df33633b0c1d28bb542323befdb68ebf2b9c8199ebc7bc9c3058013546e488b3ca1cfeff2a267a4492fcb5cf0846ac53f5cbff33a1c7e1206822727b9b74fb91298855376e3b9d01c829a05b4294b848b8a9718f747501c02c04e7e1fb5eec823394d01a56b01651aa0cc1789c8c2a74ac13a945b39c30cc9ffcb20c405add6bcbb98177878b29a54a80c6aaa21235df95679da75b563ab59091a3b73054f15821e33dd1e1629963ea233b9a484a9d11a161419b8cc2087f687e079146c8546d4061c52b50a0b06332d791f2ab087a87fa2874c9ea2adcc8936fc25e238518bf5b5d9f7249e654f52cfbfae6dcebbf56f017be96081'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

"""# This kernel aim is to show how to use the recommendation system algorithms.

![image.png](attachment:06db193f-77aa-402d-91ce-f5554348dee3.png)

# Import Necessary Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np
import pandas as pd
import math
import json
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
#from sklearn.externals import joblib
import scipy.sparse
from scipy.sparse import csr_matrix
import warnings; warnings.simplefilter('ignore')
# %matplotlib inline

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

"""# Importing the Dataset

## Read and Explore the Data
"""

#Import the data set
df = pd.read_csv('/kaggle/input/amazon-fine-food-reviews/Reviews.csv')

df.head()

# Dropping the columns
df = df.drop(['Id', 'ProfileName','Time','HelpfulnessNumerator','HelpfulnessDenominator','Text','Summary'], axis = 1)

# see few rows of the imported dataset
df.tail()

# Check the number of rows and columns
rows, columns = df.shape
print("No of rows: ", rows)
print("No of columns: ", columns)

#Check Data types
df.dtypes

# Check for missing values present
print('Number of missing values across columns-\n', df.isnull().sum())

"""### There are no missing values with total records 568454

"""

# Summary statistics of 'rating' variable
df[['Score']].describe().transpose()

# find minimum and maximum ratings

def find_min_max_rating():
    print('The minimum rating is: %d' %(df['Score'].min()))
    print('The maximum rating is: %d' %(df['Score'].max()))

find_min_max_rating()

"""### Ratings are on scale of 1 - 5

"""

import seaborn as sns

# Check the distribution of ratings
with sns.axes_style('white'):
    g = sns.catplot(x="Score", data=df, aspect=2.0, kind='count')
    g.set_ylabels("Total number of ratings")

# Number of unique user id and product id in the data
print('Number of unique USERS in Raw data = ', df['UserId'].nunique())
print('Number of unique ITEMS in Raw data = ', df['ProductId'].nunique())

"""### Take subset of dataset to make it less sparse/more dense. ( For example, keep the users only who has given 50 or more number of ratings )"""

# Top 10 users based on rating
most_rated = df.groupby('UserId').size().sort_values(ascending=False)[:10]
most_rated

"""### Data model preparation as per requirement on number of minimum ratings

"""

counts = df['UserId'].value_counts()
df_final = df[df['UserId'].isin(counts[counts >= 50].index)]

df_final.head()

print('Number of users who have rated 50 or more items =', len(df_final))
print('Number of unique USERS in final data = ', df_final['UserId'].nunique())
print('Number of unique ITEMS in final data = ', df_final['ProductId'].nunique())

"""#### df_final has users  who have rated 50 or more items

#### Calculate the density of the rating matrix
"""

final_ratings_matrix = pd.pivot_table(df_final,index=['UserId'], columns = 'ProductId', values = "Score")
final_ratings_matrix.fillna(0,inplace=True)
print('Shape of final_ratings_matrix: ', final_ratings_matrix.shape)
given_num_of_ratings = np.count_nonzero(final_ratings_matrix)
print('given_num_of_ratings = ', given_num_of_ratings)
possible_num_of_ratings = final_ratings_matrix.shape[0] * final_ratings_matrix.shape[1]
print('possible_num_of_ratings = ', possible_num_of_ratings)
density = (given_num_of_ratings/possible_num_of_ratings)
density *= 100
print ('density: {:4.2f}%'.format(density))

final_ratings_matrix.tail()

# Matrix with one row per 'Product' and one column per 'user' for Item-based CF
final_ratings_matrix_T = final_ratings_matrix.transpose()
final_ratings_matrix_T.head()

"""### Split the data randomly into train and test dataset. ( For example split it in 70/30 ratio)"""

#Split the training and test data in the ratio 70:30
train_data, test_data = train_test_split(df_final, test_size = 0.3, random_state=0)

print(train_data.head(5))

def shape():
    print("Test data shape: ", test_data.shape)
    print("Train data shape: ", train_data.shape)
shape()

"""# Build Popularity Recommender model. (Non-personalised)"""

#Count of user_id for each unique product as recommendation score
train_data_grouped = train_data.groupby('ProductId').agg({'UserId': 'count'}).reset_index()
train_data_grouped.rename(columns = {'UserId': 'score'},inplace=True)
train_data_grouped.head()

#Sort the products on recommendation score
train_data_sort = train_data_grouped.sort_values(['score', 'ProductId'], ascending = [0,1])

#Generate a recommendation rank based upon score
train_data_sort['Rank'] = train_data_sort['score'].rank(ascending=0, method='first')

#Get the top 5 recommendations
popularity_recommendations = train_data_sort.head(5)
popularity_recommendations

# Use popularity based recommender model to make predictions
def recommend(user_id):
    user_recommendations = popularity_recommendations

    #Add user_id column for which the recommendations are being generated
    user_recommendations['UserId'] = user_id

    #Bring user_id column to the front
    cols = user_recommendations.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    user_recommendations = user_recommendations[cols]

    return user_recommendations

find_recom = [15,121,200]   # This list is user choice.
for i in find_recom:
    print("Here is the recommendation for the userId: %d\n" %(i))
    print(recommend(i))
    print("\n")

print('Since this is a popularity-based recommender model, recommendations remain the same for all users')
print('\nWe predict the products based on the popularity. It is not personalized to particular user')

"""# Build Collaborative Filtering model.

#### Model-based Collaborative Filtering: Singular Value Decomposition
"""

df_CF = pd.concat([train_data, test_data]).reset_index()
df_CF.tail()

#User-based Collaborative Filtering
# Matrix with row per 'user' and column per 'item'
pivot_df = pd.pivot_table(df_CF,index=['UserId'], columns = 'ProductId', values = "Score")
pivot_df.fillna(0,inplace=True)
print(pivot_df.shape)
pivot_df.head()

pivot_df['user_index'] = np.arange(0, pivot_df.shape[0], 1)
pivot_df.head()

pivot_df.set_index(['user_index'], inplace=True)

# Actual ratings given by users
pivot_df.head()

"""### SVD method
#### SVD is best to apply on a large sparse matrix
"""

from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

# Convert the DataFrame to a sparse matrix
pivot_sparse = csr_matrix(pivot_df.values)

# Perform Singular Value Decomposition
U, sigma, Vt = svds(pivot_sparse, k=50)

"""### Note that for sparse matrices, you can use the sparse.linalg.svds() function to perform the decomposition.
SVD is useful in many tasks, such as data compression, noise reduction similar to Principal Component Analysis and Latent Semantic Indexing (LSI), used in document retrieval and word similarity in Text mining
"""

# Convert sigma to a diagonal matrix
sigma = np.diag(sigma)

# Predicted ratings
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)

# Create a DataFrame with the predicted ratings
preds_df = pd.DataFrame(all_user_predicted_ratings, columns = pivot_df.columns)

# Show the first few rows
preds_df.head()

# Recommend the items with the highest predicted ratings

def recommend_items(userID, pivot_df, preds_df, num_recommendations):

    user_idx = userID-1 # index starts at 0

    # Get and sort the user's ratings
    sorted_user_ratings = pivot_df.iloc[user_idx].sort_values(ascending=False)
    #sorted_user_ratings
    sorted_user_predictions = preds_df.iloc[user_idx].sort_values(ascending=False)
    #sorted_user_predictions

    temp = pd.concat([sorted_user_ratings, sorted_user_predictions], axis=1)
    temp.index.name = 'Recommended Items'
    temp.columns = ['user_ratings', 'user_predictions']

    temp = temp.loc[temp.user_ratings == 0]
    temp = temp.sort_values('user_predictions', ascending=False)
    print('\nBelow are the recommended items for user(user_id = {}):\n'.format(userID))
    print(temp.head(num_recommendations))

#Enter 'userID' and 'num_recommendations' for the user #
userID = 121
num_recommendations = 5
recommend_items(userID, pivot_df, preds_df, num_recommendations)

"""# Evaluate both the models. ( Once the model is trained on the training data, it can be used to compute the error (RMSE) on predictions made on the test data.)

#### Evaluation of Model-based Collaborative Filtering (SVD)
"""

# Actual ratings given by the users
final_ratings_matrix.head()

# Average ACTUAL rating for each item
final_ratings_matrix.mean().head()

# Predicted ratings
preds_df.head()

# Average PREDICTED rating for each item
preds_df.mean().head()

rmse_df = pd.concat([final_ratings_matrix.mean(), preds_df.mean()], axis=1)
rmse_df.columns = ['Avg_actual_ratings', 'Avg_predicted_ratings']
print(rmse_df.shape)
rmse_df['item_index'] = np.arange(0, rmse_df.shape[0], 1)
rmse_df.head()

RMSE = round((((rmse_df.Avg_actual_ratings - rmse_df.Avg_predicted_ratings) ** 2).mean() ** 0.5), 5)
print('\nRMSE SVD Model = {} \n'.format(RMSE))

"""## Get top - K ( K = 5) recommendations. Since our goal is to recommend new products to each user based on his/her habits, we will recommend 5 new products."""

# Enter 'userID' and 'num_recommendations' for the user #
userID = 200
num_recommendations = 5
recommend_items(userID, pivot_df, preds_df, num_recommendations)

"""# Conclusion

Model-based Collaborative Filtering is a personalised recommender system, the recommendations are based on the past behavior of the user and it is not dependent on any additional information.

The Popularity-based recommender system is non-personalised and the recommendations are based on frequecy counts, which may be not suitable to the user.You can see the differance above for the user id 121 & 200, The Popularity based model has recommended the same set of 5 products to both but Collaborative Filtering based model has recommended entire different list based on the user past purchase history
"""