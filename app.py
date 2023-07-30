import streamlit as st
from main import analyze_tweets
from main import get_tweets
import plotly.graph_objs as go
from collections import Counter
from wordcloud import WordCloud

st.set_page_config(page_title="Twitter Sentiment Analysis")

# add a title
st.title("Real-Time Twitter Sentiment Analysis")

# add a project description
st.write("""
           The Twitter Sentiment Analysis is a tool that allows users to search for tweets related to a particular keyword and analyze their sentiment. 
   Simply enter a keyword in the sidebar, select the number of tweets to analyze, and choose the sentiment type to display. 
   The tool will perform sentiment analysis on the tweets and display the results in a data table, pie chart, and bar chart.
   This tool can be useful for businesses and individuals who want to track public opinion about a particular topic or brand on Twitter. 
   """)

# add a text input for the keyword
keyword = st.sidebar.text_input("Enter a keyword to search on Twitter")

# add a slider to select the number of tweets to analyze
count = st.sidebar.slider("Enter the number of tweets to analyze", 1, 1000, 100)

import base64

def add_bg_from_local(image_files):
    with open(image_files[0], "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    with open(image_files[1], "rb") as image_file:
        encoded_string1 = base64.b64encode(image_file.read())
    st.markdown(
    """
    <style>
      .stApp {
          background-image: url(data:image/png;base64,"""+encoded_string.decode()+""");
          background-size: cover;
      }
      .css-6qob1r.e1fqkh3o3 {
        background-image: url(data:image/png;base64,"""+encoded_string1.decode()+""");
        background-size: cover;
        background-repeat: no-repeat;
      }
    </style>"""
    ,
    unsafe_allow_html=True
    )
add_bg_from_local([r'black-rotate.png', r'black-rotate.png'])

# add a button to start the analysis
if st.sidebar.button("Analyze"):
    if not keyword:
        st.write("Please enter a keyword")
    else:
        if keyword:
            # Use a progress bar to show the progress of the sentiment analysis
            progress_bar = st.progress(0)
            status_text = st.empty()
            with st.spinner("Process in progress..."):
                tweets = get_tweets(keyword, count)
                progress_bar.progress(50)
                status_text.text("Performing sentiment analysis...")
                df = analyze_tweets(keyword, count)
                progress_bar.progress(100)
                status_text.text("Analysis Completed!!!")
                progress_bar.progress(100)

            st.write("### Tweets")
            st.dataframe(df[["Tweet", "Sentiment", "Timestamp"]])

            st.sidebar.write("### Sentiment Analysis")
            st.sidebar.write(f"Number of Positive Tweets: {len(df[df['Sentiment'] == 'Positive'])}")
            st.sidebar.write(f"Number of Negative Tweets: {len(df[df['Sentiment'] == 'Negative'])}")
            st.sidebar.write(f"Number of Neutral Tweets: {len(df[df['Sentiment'] == 'Neutral'])}")

            # create pie chart
            sentiments = Counter(df["Sentiment"])
            labels = list(sentiments.keys())
            values = list(sentiments.values())

            st.plotly_chart(
                go.Figure(
                    data=[go.Pie(labels=labels, values=values)],
                    layout=go.Layout(title="Sentiment Analysis", height=600)
                )
            )

            # create a bar chart
            st.write("### Bar Chart of Sentiments")
            st.bar_chart(sentiments)

            # create a word cloud
            st.write("### Word Cloud")
            text = " ".join(df["Tweet"].values)
            wordcloud = WordCloud(width=800, height=600).generate(text)
            st.image(wordcloud.to_array())

            # create a time series plot of tweet timestamps
            st.write("### Time Series Plot of Tweet Timestamps")
            timestamps = df["Timestamp"]
            timestamps = timestamps.value_counts().sort_index()
            timestamps_chart = go.Figure()
            timestamps_chart.add_trace(go.Scatter(x=timestamps.index, y=timestamps.values))
            timestamps_chart.update_layout(title="Tweet Timestamps", xaxis_title="Timestamp",
                                           yaxis_title="Number of Tweets")
            st.plotly_chart(timestamps_chart)

if st.button("Reset"):
    input_sms=""

