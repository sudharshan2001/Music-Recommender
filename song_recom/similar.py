import pandas as pd
import numpy as np
import os
from sklearn.neighbors import NearestNeighbors

df=pd.read_csv("song_recom\\tracks.csv")
df.drop('release_date', axis=1, inplace=True)
df.drop_duplicates('id',inplace=True)
df.dropna(inplace=True)

def data_filter(df):
    '''Chooses only required features and returns that df with id as index'''
    
    df = df[['id', 'danceability', 'energy', 'key', 'valence','popularity']]
    df.set_index('id',inplace=True)
    return df

def artist_verification(song_input,df1=df):
    retrieving_song_id = df1[df1['name'] == song_input]

    checking1 = retrieving_song_id['id']
    data_you_need = pd.DataFrame()
    for i in checking1:
        matched_row1 = df1[df1['id'] == i]
        data_you_need = data_you_need.append(matched_row1)
    data_you_need = data_you_need[['artists', 'id']]
    return data_you_need


def selected_songid(name, artists):
    '''
    name: name of the songs
    artists: name of the artist
    '''
    
    song_name = df.loc[(df['name']==name) & (df['artists']== artists)].head(1)['id'].values[0]
    return song_name

def find_song(selected_song,total=50):
    '''KNN Model'''
    model_knn = NearestNeighbors(metric = 'euclidean', algorithm = 'brute')
    model_knn.fit(data_filter(df))

    
    distances, indices = model_knn.kneighbors(data_filter(df).loc[selected_song,:].values.reshape(1, -1), n_neighbors = total)
    # make a list of all similar songs
    list_of_predicted_songs_ = []
    for j in range(1,total):
        list_of_predicted_songs_.append(f'''{df[df['id']==data_filter(df).index[indices.flatten()[j]]]['name'].values[0]} by {str(df[df['id']==data_filter(df).index[indices.flatten()[j]]]['artists'].values[0])[1:-1].replace("'","")}''')
    return list_of_predicted_songs_
