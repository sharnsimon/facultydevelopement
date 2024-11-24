import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Function to fetch and count hyperlinks using Selenium
def fetch_hyperlinks_selenium(url):
    # Configure Selenium WebDriver
    options = Options()
    options.add_argument('--headless')  # Run browser in headless mode (no UI)
    options.add_argument('--disable-gpu')  # Disable GPU (for compatibility)
    options.add_argument('--no-sandbox')  # Disable sandbox mode (for Linux)
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)  # Open the webpage
        time.sleep(3)  # Wait for page to load
        
        # Find all <a> tags on the page
        links = driver.find_elements(By.TAG_NAME, 'a')
        
        # Extract valid href attributes
        hyperlinks = [link.get_attribute('href') for link in links if link.get_attribute('href')]

        return len(hyperlinks), hyperlinks  # Return count and list of hyperlinks
    
    except Exception as e:
        return None, f"Error: {e}"
    
    finally:
        driver.quit()  # Close the browser

# Streamlit App
def main():
    st.title("Hyperlink Counter (Selenium)")

    # Input for URL
    url = st.text_input("Enter the URL of the webpage", placeholder="https://example.com")
    
    # Fetch and display hyperlinks
    if st.button("Count Hyperlinks"):
        if url:
            with st.spinner("Fetching hyperlinks..."):
                count, result = fetch_hyperlinks_selenium(url)
            
            if count is not None:
                st.success(f"Total hyperlinks found: {count}")
                
                # Display the hyperlinks if available
                if st.checkbox("Show hyperlinks"):
                    st.write("### Hyperlinks:")
                    for idx, link in enumerate(result, start=1):
                        # Display hyperlinks with numbers
                        st.markdown(f"{idx}. [**{link}**]({link})")
            else:
                st.error(result)
        else:
            st.error("Please enter a valid URL.")

if __name__ == "__main__":
    main()
