# Music-Recommender
Recommend songs based on emotions and help find the song similar to the input

Download the data from this drive link https://drive.google.com/file/d/14xIxaTtg1k0bmyDmldqQKOGNZVbfk2VV/view?usp=sharing and put it in the "song_recom" folder.

Install the dependencies : `pip install -r requirements.txt`

To run the app locally : `streamlit run main.py`

Description:
  There are 3 Features : Manual Selection, Auto Selection, Find Simlar Song
    Manual Selection : We can manually get song recommendation based on the parameters we give
    Auto Selection   : This option will recommend songs based on emotion that is detected from the camera
    Find Simlar Song : This takes an input song and will recommend songs based on that
