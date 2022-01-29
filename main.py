from tkinter import EXCEPTION
import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from collections import Counter
import pandas as pd
import os, ast, cv2, time
from song_recom.pred import angry_mood, happy_mood, sad_mood, neutral_mood
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from song_recom.similar import find_song, data_filter, artist_verification, selected_songid

face_classifier = cv2.CascadeClassifier(r'haarcascades\haarcascade_frontalface_default.xml')

classifier =load_model(r'bestmodel.h5') #Load the Model

emotion_labels = ['Angry','Happy','Neutral', 'Sad']

st.set_page_config(page_title="Song Recommender",layout ='wide')
mode_choice=st.sidebar.selectbox('Selection Mode',['Manual Selection','Auto Selection', 'Find Simlar Song']) # Choice Auto for detecting emotion, manual for selecting manually 


if mode_choice =='Auto Selection':

    st.info("Make sure the lighting is good and wait for couple of seconds")
    image_placeholder = st.empty()
    cap = cv2.VideoCapture(0)
    labels = ['Neutral']

    # It'll run for 150 iteration
    for i in range(150):
        _, frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)

                prediction = classifier.predict(roi)[0]

                label=emotion_labels[prediction.argmax()]
                labels.append(label)
                label_position = (x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            else:
                cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        # cv2.imshow('Emotion',frame)
        image_placeholder.image(frame, use_column_width=True,clamp = True,channels='BGR')
    cap.release()
    cv2.destroyAllWindows()

    # Choosing the emotion that occured most
    counts = Counter(labels)
    emotion = max(counts, key=counts.get)
    image_placeholder.success(emotion)

    if emotion == 'Angry':
        st.dataframe(angry_mood(),18000, 2000)
    elif emotion == 'Happy':
        st.dataframe(happy_mood(),18000, 2000)
    elif emotion == 'Neutral':
        st.dataframe(neutral_mood(),18000, 2000)
    else:
        st.dataframe(sad_mood(),18000, 2000)
        
elif mode_choice=='Manual Selection':

    new = st.empty()
    choice = new.selectbox('Choose mood', ('---','Neutral','Angry','Happy', 'Sad'))
    
    if choice != '---':
        
        type_ = st.selectbox('Filter Song',('Mixed', 'popularity'))
        if choice == 'Angry':
            st.dataframe(angry_mood(choice),18000, 2000)
        elif choice == 'Happy':
            st.dataframe(happy_mood(choice),18000, 2000)
        elif choice == 'Neutral':
            st.dataframe(neutral_mood(choice),18000, 2000)
        else:
            st.dataframe(sad_mood(choice),18000, 2000) 
    pass

elif mode_choice =='Find Simlar Song':
    
    try:
        
        tempy = pd.read_csv('song_recom\\tracks.csv')
        track_list = tempy['name'].to_list()
        track_list=track_list[:20000]
        simi = st.container()
        selected_song = simi.text_input('Song name')

        if selected_song is not None:
            artist_verification = simi.selectbox('Artists',artist_verification(selected_song))
        
        if artist_verification:
            selected_song = selected_songid(selected_song,artist_verification)
            
        number = st.number_input('How many Recommendations?')
        if selected_song is not None:
            for i in find_song(selected_song,total=int(number)):
                st.info(i)

    except (KeyError,TypeError,ValueError):
        simi.error('Please, Try Again. Make Sure you search with Precise Name')
        
    else:
        pass

