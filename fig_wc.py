import dill
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re

def plot(merchant, ins):
    with open(merchant+'/ins_'+merchant+'_top50_followers_30tweets.dill', 'rb') as in_strm:
        d_followers_tweetstext = dill.load(in_strm)  

    text = ' '.join([re.sub('(https://[\w\./]*)', ' ', re.sub('(@[\w]*)', ' ', i)) for i in d_followers_tweetstext[ins].values()])


    def transform_format(val):
        if val == 0:
            return 255
        else:
            return 88

    bird_mask = np.array(Image.open("bird.png"))
    transformed_bird_mask = np.ndarray((bird_mask.shape[0],bird_mask.shape[1]), np.int32)
    for i in range(len(bird_mask)):
        transformed_bird_mask[i] = list(map(transform_format, bird_mask[i]))    



    stop_words = set(stopwords.words('english')+['https','RT','amp','u','one',"I'm"])
    wordcloud = WordCloud(stopwords=stop_words, max_words=30, background_color="white", mask=transformed_bird_mask, contour_width=2, contour_color='lightblue',repeat=True).generate(text)


    fig = plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    #plt.show()
    #wordcloud.to_file(merchant+'/wc/'+ins+"_followers_tweetstext.png")
    return fig
