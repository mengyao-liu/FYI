import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import SessionState
import dill
import json
from PIL import Image
import re
import fig_wc




def pageZero(sesh, merchant):
    st.header('Stay tuned...')


def pageOne(sesh, merchant):
    with open(merchant+'/ins_'+merchant+'_top50_3months_rank.dill', 'rb') as in_strm:
        df_score = dill.load(in_strm) 
    d = df_score.reset_index().rename({'username':'Influencer', 'score':'Score'}, axis='columns')
    d.loc[:,'Score'] = ['%.2f'%i for i in d['Score']]
    d.loc[:,'Influencer'] = ['@'+i for i in d['Influencer']]
    d.index  += 1
    with open(merchant+'/chart_'+merchant+'.json', "rb") as f:
        chart = json.load(f)
    

    if not sesh.button_sent:
        st.balloons()
    st.header('Here are the top 5 influencers we recommend for you!')
    st.markdown('###')
    st.write(d[:5])
    st.write('Out of *375* active verified influencers with No. of followers 100 - 1k')
    
    st.markdown('#')    
    st.header('Check out the key metrics.')
    st.markdown('###')
    st.vega_lite_chart(chart, width=800, height=400)
    
    st.markdown('#') 
    st.header("Check out what **your influencer's** ***followers*** are talking about recently.")
    show_wc(merchant)
    
          
def show_wc(merchant):
    ins = st.text_input('Influencer', )
    insname = re.sub('[\s]*[@]*', '', ins)
    if len(insname)>0:
        try:
            image = Image.open(merchant+'/wc/'+insname+'_followers_tweetstext.png')
            st.image(image, caption='Word cloud of '+insname+"'s followers in their recent 30 tweets")
        except Exception:
            with st.spinner("Generating the word cloud..."):
                image = fig_wc.plot(merchant, insname)
                st.pyplot(image, caption='Word cloud of '+insname+"'s followers in their recent 30 tweets")
        #else:
            #image = Image.open('bird.png')
            #st.image(image, caption='Not available yet')
        
    

def pageTwo(sesh, merchant):
    st.header('No match found. Try another influencer type!')
    
    
sesh = SessionState.get(curr_page = 0, curr_index=0, last_index=-1, button_sent=False)
PAGES = [pageZero, pageOne, pageTwo]
#st.set_page_config(layout="wide")

def main():
    #####MAIN PAGE NAV BAR:
    st.markdown(' # Find Your Influencer')
    
    st.markdown(' ## Step 1: Please select your product category')
    cat_list = ['Books 📖','Beauty 💄','Sports 🏸','Clothing 👕','Electronics 🖥']
    cat = st.selectbox('', cat_list)
    loc = {'Books 📖':'book', 'Beauty 💄': 'beauty', 'Sports 🏸':'sports', 'Clothing 👕':'clothing', 'Electronics 🖥':'electronics'}
    
    st.markdown(' ## Step 2: Please select your influencer type')
    inscat_list = ['100 - 1k 💰', '1k - 10k 💰💰', '10k - 100k 💰💰💰', '>100k 💰💰💰💰']
    inscat = st.selectbox("No. of followers", inscat_list)
    
    sesh.curr_index = cat_list.index(cat) + 10*inscat_list.index(inscat)
    st.markdown('##')
    
    
    
    if inscat=='100 - 1k 💰':
        if cat=='Electronics 🖥':
            sesh.curr_page = 2
        else:
            sesh.curr_page = 1
    else:
        sesh.curr_page = 0
        
        
    if sesh.curr_index!=sesh.last_index:
        sesh.button_sent=False
        sesh.last_index = sesh.curr_index
    
    
    if st.button('Submit'):    
        with st.spinner("Getting your influencers..."):
            st.markdown('##')            
            page_turning_function = PAGES[sesh.curr_page]
            page_turning_function(sesh, loc[cat])
            sesh.button_sent = True
            
            
    elif sesh.button_sent: 
        st.markdown('##') 
        page_turning_function = PAGES[sesh.curr_page]
        page_turning_function(sesh, loc[cat])
        
     
    # documentation
    link1 = '[About this app](https://github.com/mengyao-liu/FYI)'
    st.markdown('##')
    st.markdown(link1, unsafe_allow_html=True)
    # author
    link2 = '[About the author](https://www.linkedin.com/in/mengyao-cecily-liu/)'
    st.markdown(link2, unsafe_allow_html=True)
    

if __name__=='__main__':
    main()
