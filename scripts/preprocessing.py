from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import pandas as pd
import numpy as np
import pyfpgrowth

def load_and_prepare_data():
    books_df = pd.read_csv('data/Books.csv')
    ratings_df = pd.read_csv('data/Ratings.csv')

    filtered_ratings_df = ratings_df[ratings_df['Book-Rating'] > 5]
    
    df = pd.merge(filtered_ratings_df, books_df[['ISBN', 'Book-Title', 'Image-URL-M', 'Book-Author']], on='ISBN', how='inner')

    df = df.drop_duplicates(['User-ID', 'Book-Title'])

    return df