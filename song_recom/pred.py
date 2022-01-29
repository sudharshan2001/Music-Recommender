import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.neighbors import NearestNeighbors

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

df=pd.read_csv("song_recom\\tracks.csv")
df.drop('release_date', axis=1, inplace=True)
df['artists']=df.artists.apply(lambda x: ast.literal_eval(str(x)))
df.drop_duplicates('id',inplace=True)
df.dropna(inplace=True)

# To Drop Remix Tracks
def clean_remix(df):
    df.reset_index(inplace=True) #drop=True to drop columns
    to_rmove=['Remix','Mix']
    index_to_remove=[]
    for i in range(len(df)):
        for ii in df.iloc[i]['name'].split():
            if ii in to_rmove:
                index_to_remove.append(i)

    new_list=[]
    for i in index_to_remove:
        if i not in new_list:
            new_list.append(i)

    df.drop(new_list,axis=0,inplace=True)
    return df 

# sort out by popular, artist, high energy, danceability
def choose_option(input_,df):
    '''input_ : preference of the songs :Popular or explore mode
    
       df : dataframe with high valence
    '''
    if input_ == 'popularity':
        temp_df = df.sort_values(ascending=True,by=['popularity'])
    else:
        temp_df = df
    return temp_df

#To Filter out the desired artist
def choose_artist(name, df):
    '''name: name of the artist
     
       df: Filtered Dataframe 
    '''
    name_present=[]
    for i in range(len(df)):
        if name in df.iloc[i]['artists']:
            name_present.append(True)
        else:
            name_present.append(False)
            
    return df[name_present]


# happy 
# high valence means the song is happy, cheerful, etc. We're choosing songs where Valence is greater than 0.7
def happy_mood(input_=None,df=df,name=None):
    '''input_ : preference of the songs :(popularity)
    
       df : dataframe
       
       name: Name of the artist you prefer
    '''
    
    high_val = df[df['valence']>=0.7].sort_values(by=['valence'])
    high_val = high_val.sort_values(ascending=False, by=['energy'])
    high_val = choose_option(input_, df=high_val)
    
    if name is not None:
        high_val = choose_artist(name=name,df=high_val)
    else:
        pass
    high_val['new'] =high_val['name']+' by '+high_val['artists'].map(str)
    return high_val['new']


def sad_mood(input_=None,df=df,name=None):
    '''input_ : preference of the songs : popularity
    
       df : dataframe
    '''
    low_val = df[df['valence']<=0.5].sort_values(by=['valence'])
    low_val = low_val.sort_values(ascending=True, by=['energy'])
    
    if input_ is not None:
        low_val = choose_option(input_, df=low_val)
    else:
        pass
    
    if name is not None:
        low_val = choose_artist(name=name,df=low_val)
    else:
        pass
    low_val['new'] =low_val['name']+' by '+low_val['artists'].map(str)
    return low_val['new']


def neutral_mood(input_=None,df=df,name=None):
    '''input_ : preference of the songs : popularity
    
       df : dataframe
       
       name: Name of the artist you prefer
    '''
    mid_val = df[df['valence']<=0.7]
    mid_val = mid_val[mid_val['valence']>0.4].sort_values(by=['valence'])

    mid_val = mid_val.sort_values(ascending=False, by=['energy'])
    
    if input_ is not None:
        mid_val = choose_option(input_, df=mid_val)
    else:
        pass
    
    
    if name is not None:
        mid_val = choose_artist(name=name,df=mid_val)
    else:
        pass
        
    mid_val['new'] =mid_val['name']+' by '+mid_val['artists'].map(str)
    return mid_val['new']


def angry_mood(input_=None,df=df,name=None):
    '''input_ : preference of the songs : popularity
    
       df : dataframe
       
       name: Name of the artist you prefer
    '''
    ang_val = df[df['valence']<=0.5].sort_values(by=['valence'])

    ang_val = ang_val.sort_values(ascending=False, by=['energy'])
    ang_val = ang_val.sort_values(ascending=True, by=['danceability'])
    ang_val = ang_val.sort_values(ascending=True, by=['speechiness'])
    
    if input_ is not None:
        ang_val = choose_option(input_, df=ang_val)
    else:
        pass
    
    if name is not None:
        ang_val = choose_artist(name=name,df=ang_val)
    else:
        pass
    ang_val['new'] =ang_val['name']+' by '+ang_val['artists'].map(str)
    return ang_val['new']

