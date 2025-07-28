
import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os



os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_KEY"


# 🔎 Function to fetch top trends from trends24.in
def fetch_trends(location="india"):
    url = f"https://trends24.in/india/"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    trending = []
    ol = soup.find("ol", class_="trend-list")
    if not ol:
        return trending
    for item in ol.find_all("li", limit=10):
        text = item.get_text(strip=True)
        trending.append(text)
    return trending

st.title("🔥 Tweet Generator from Live X Trends")
st.sidebar.header("Settings")
loc = st.sidebar.selectbox("Select trend region", ["india", "worldwide"])
trends = fetch_trends(loc)

if trends:
    st.subheader(f"Top 10 trending topics in {loc.capitalize()}")
    selected = st.selectbox("Choose a trend:", trends)
else:
    st.warning("Could not fetch trending topics. Please try again later.")
    st.stop()

tone = st.selectbox("Tone:", ["Professional", "Funny", "Witty", "Motivational", "Sarcastic"])
num_tweets = st.slider("Number of Tweets", 1, 5, 3)

if st.button("Generate Tweets"):
    llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a social media expert writing tweets."),
        ("user", "Write {num} {tone} tweets about '{topic}'. Include hashtags if appropriate.")
    ])
    chain = prompt | llm
    resp = chain.invoke({"topic": selected, "tone": tone.lower(), "num": num_tweets})
    st.subheader("📝 Generated Tweets")
    for tweet in resp.content.strip().split('\n'):
        if tweet.strip():
            st.markdown(f"- {tweet.strip()}")
