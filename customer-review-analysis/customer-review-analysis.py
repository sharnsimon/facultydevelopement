import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk

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
    text = re.sub('[^a-zA-Z]', ' ', text)  # Remove non-alphabetic characters
    text = text.lower()  # Convert to lowercase
    text = text.split()  # Tokenize into words
    text = [word for word in text if word not in stop_words]  # Remove stopwords
    text = ' '.join(text)  # Join words back into a single string
    text = [text]  # Convert to list for vectorizer
    text = vectorizer.transform(text)  # Transform using vectorizer
    
    # Predict sentiment
    sentiment = model.predict(text)
    return "Negative" if sentiment == 0 else "Positive"

# Function to create a colored card
def create_card(review_text, sentiment):
    color = "green" if sentiment == "Positive" else "red"
    card_html = f"""
    <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <h5 style="color: white;">{sentiment} Sentiment</h5>
        <p style="color: white;">{review_text}</p>
    </div>
    """
    return card_html

# Main app logic
def main():
    st.title("Customer Review Sentiment Analysis")

    # Load stopwords, model, and vectorizer only once
    stop_words = load_stopwords()
    model, vectorizer = load_model_and_vectorizer()

    # User input: customer review text
    st.subheader("Enter a Customer Review")
    review_text = st.text_area("Type or paste the review here")

    if st.button("Analyze Sentiment"):
        if review_text.strip():  # Ensure input is not empty
            sentiment = predict_sentiment(review_text, model, vectorizer, stop_words)
            
            # Display result in a colored card
            card_html = create_card(review_text, sentiment)
            st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.write("Please enter a review to analyze.")

if __name__ == "__main__":
    main()
