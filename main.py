# Import necessary modules from Selenium, BeautifulSoup for HTML parsing, and dotenv for environment variable management
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Retrieve the SBR_WEBDRIVER URL from environment variables
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

def scrape_website(website):
    # Print a message indicating the connection to the scraping browser is starting
    print("Connecting to Scraping Browser...")
    
    # Create a remote connection to the scraping browser using the specified webdriver URL and browser type
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    
    # Use the remote connection as the WebDriver instance to control the browser
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        # Navigate to the specified website
        driver.get(website)
        print("Waiting captcha to solve...")

        # Execute a command to wait for captcha to be solved
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",  # Command to wait for captcha resolution
                "params": {"detectTimeout": 10000},  # Timeout for detecting captcha solution
            },
        )
        
        # Print the status of captcha solving
        print("Captcha solve status:", solve_res["value"]["status"])
        
        # Indicate that navigation is complete and scraping will begin
        print("Navigated! Scraping page content...")
        
        # Get the HTML content of the page
        html = driver.page_source
        return html  # Return the scraped HTML content

# Function to extract body content from HTML
def extract_body_content(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Get the <body> element from the parsed HTML
    body_content = soup.body
    
    # If body content is found, return it as a string; otherwise, return an empty string
    if body_content:
        return str(body_content)
    return ""

# Function to clean the body content by removing scripts and styles
def clean_body_content(body_content):
    # Parse the body content using BeautifulSoup
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove <script> and <style> tags from the content
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get the text from the cleaned soup
    cleaned_content = soup.get_text(separator="\n")
    
    # Strip whitespace from each line and filter out empty lines
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content  # Return the cleaned text content

# Function to split the DOM content into chunks of a specified maximum length
def split_dom_content(dom_content, max_length=6000):
    # Create and return a list of substrings from the DOM content, each of max_length size
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
