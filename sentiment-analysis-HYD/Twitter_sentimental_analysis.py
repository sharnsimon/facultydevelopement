import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Download stopwords once, using Streamlit's caching
@st.cache_resource
def load_stopwords():
    nltk.download('stopwords')
    return stopwords.words('english')

# Load model and vectorizer once
@st.cache_resource
def load_model_and_vectorizer():
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

# Define sentiment prediction function
def predict_sentiment(text, model, vectorizer, stop_words):
    # Preprocess text
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [word for word in text if word not in stop_words]
    text = ' '.join(text)
    text = [text]
    text = vectorizer.transform(text)
    
    # Predict sentiment
    sentiment = model.predict(text)
    return "Negative" if sentiment == 0 else "Positive"

# Function to scrape a tweet from a tweet URL using Selenium
def scrape_tweet(tweet_url):
    # tweet_id = tweet_url.split("/")[-1]  # Extract tweet ID
    url = f"{tweet_url}"  # Updated URL for X.com

    # Set up Selenium WebDriver (using Chrome)
    options = Options()
    options.headless = True  # Run in headless mode (no browser window)
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Allow time for the page to load the tweet content

        # Find the tweet content by inspecting the page structure
        tweet_text = None
        tweet_div = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']")  # Updated XPath
        tweet_text = tweet_div.text
        
        return tweet_text if tweet_text else None

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()  # Close the browser

# Function to create a colored card
def create_card(tweet_text, sentiment):
    color = "green" if sentiment == "Positive" else "red"
    card_html = f"""
    <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <h5 style="color: white;">{sentiment} Sentiment</h5>
        <p style="color: white;">{tweet_text}</p>
    </div>
    """
    return card_html

# Main app logic
def main():
    st.title("X.com Sentiment Analysis")

    # Load stopwords, model, and vectorizer only once
    stop_words = load_stopwords()
    model, vectorizer = load_model_and_vectorizer()

    # User input: either text input or tweet link
    st.subheader("Enter a Tweet URL")
    tweet_url = st.text_input("Paste the tweet link here")
    if st.button("Fetch Tweet"):
            tweet_text = scrape_tweet(tweet_url)
            if tweet_text:
                sentiment = predict_sentiment(tweet_text, model, vectorizer, stop_words)  # Predict sentiment of the tweet text
                    
                # Create and display the colored card for the tweet
                card_html = create_card(tweet_text, sentiment)
                st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.write("Could not fetch tweet or an error occurred.")

if __name__ == "__main__":
    main()
