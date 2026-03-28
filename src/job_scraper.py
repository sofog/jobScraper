"""
Job Scraper Learning Template
==============================
This is a skeleton for you to learn web scraping in Python.
Follow the TODOs in order to build your own job scraper!

LEARNING PATH:
--------------
Phase 1: Basic Scraping (TODOs 1-4)
    - Learn to fetch a webpage
    - Learn to parse HTML
    - Extract job titles and links
    
Phase 2: Filtering (TODOs 5-7)
    - Filter jobs by keywords
    - Handle edge cases
    - Display results nicely

REQUIREMENTS:
-------------
Before starting, install the required libraries:
    
    pip install requests beautifulsoup4

Or if using uv (recommended in this project):
    
    uv add requests beautifulsoup4

RESOURCES TO HELP YOU:
----------------------
- Requests docs: https://docs.python-requests.org/
- BeautifulSoup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- CSS Selectors: https://www.w3schools.com/cssref/css_selectors.asp

"""

# =============================================================================
# IMPORTS
# =============================================================================

# TODO 1: Import the required libraries

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

# =============================================================================
# PHASE 1: BASIC SCRAPING
# =============================================================================

def fetch_injected_html_selenium(url: str) -> list[dict]:
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    
    browser = webdriver.Firefox(options=opts)
    
    try:
        browser.get(url)  # This returns None, just navigates
        
        # Wait for job listings to appear (adjust selector to match the site)
        # This waits up to 10 seconds for elements to load
        WebDriverWait(browser, 10)
        # .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "...")))
        
        # NOW get the fully rendered HTML
        html = browser.page_source
        
        soup = BeautifulSoup(html, "lxml")

        jobs = []
        job_cards = soup.find_all(job="card")

        for job in job_cards:
            title = job.div.h3.string

            link = job.find("a", href=True)
            href = link.get("href", "")

            jobs.append({
                "title": title,
                "url": href
            })
        
        return jobs
        
    finally:
        browser.quit()  # Always close the browser


# Not in use - for static pages
def fetch_page(url: str) -> str:
    """
    Fetch the HTML content of a webpage.
    
    Args:
        url: The URL to fetch (e.g., "https://www.thanksben.com/careers")
        
    Returns:
        The HTML content as a string
        
    Example:
        html = fetch_page("https://www.thanksben.com/careers")
        print(html[:100])  # Print first 100 characters
    """
    
    # TODO 2: Fetch the webpage using requests
    # 1. Create a headers dict with a User-Agent (some sites block requests without it)
    #
    # 2. Use requests.get(url, headers=headers) to fetch the page
    #
    # 3. Check if the request was successful
    #
    # 4. Return the HTML content

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f'HTML for {url} retrieved')
    else:
        print(f'Scraping of {url} failed with code {response.status_code}')
    
    return response.text

# Not in use - for static pages
def parse_job_listings(html: str) -> list[dict]:
    """
    Parse job listings from HTML and extract titles + links.
    
    Args:
        html: The HTML content of the careers page
        
    Returns:
        A list of dictionaries, each containing:
        - 'title': The job title (string)
        - 'url': The link to the full job posting (string)
        
    Example output:
        [
            {"title": "Senior Data Engineer", "url": "https://..."},
            {"title": "Frontend Developer", "url": "https://..."},
        ]
    """
    
    # TODO 3: Create a BeautifulSoup object to parse the HTML
    #
    # BeautifulSoup takes two arguments:
    # 1. The HTML string to parse
    # 2. The parser to use (use "html.parser")
    soup = BeautifulSoup(html, 'html.parser')

    print(soup.prettify())
    
    # TODO 4: Find and extract job listings
    #
    # This is the trickiest part! You need to:
    # 1. Inspect the webpage (right-click > Inspect in browser)
    # 2. Find the HTML pattern for job listings
    # 3. Use BeautifulSoup methods to find those elements
    #
    # Strategy:
    # 1. Create an empty list: jobs = []
    # 2. Find all job elements using soup.find_all() or soup.select()
    # 3. Loop through each element
    # 4. Extract the title and URL
    # 5. Append to jobs list
    # 6. Return the jobs list
    #
    # Tips:
    # - Job links often contain "/jobs/" or "/careers/" in the URL
    # - If URL is relative (starts with "/"), prepend the base URL
    # - Use print() to debug and see what you're finding!
    
    jobs = []
    
    job_cards = soup.find_all(job="card")

    # print(job_cards)
    
    return jobs


# =============================================================================
# PHASE 2: FILTERING
# =============================================================================

def filter_jobs_by_keywords(jobs: list[dict], keywords: list[str]) -> list[dict]:
    """
    Filter jobs to only include those matching at least one keyword.
    
    Args:
        jobs: List of job dictionaries (from parse_job_listings)
        keywords: List of keywords to search for in job titles
        
    Returns:
        Filtered list containing only jobs with matching keywords
        
    Example:
        jobs = [
            {"title": "Senior Data Engineer", "url": "..."},
            {"title": "Marketing Manager", "url": "..."},
        ]
        filtered = filter_jobs_by_keywords(jobs, ["engineer", "developer"])
        # Returns: [{"title": "Senior Data Engineer", "url": "..."}]
    """
    
    # TODO 5: Implement keyword filtering
    #
    # Steps:
    # 1. Handle edge case: if keywords list is empty, return all jobs
    #    if not keywords:
    #        return jobs
    #
    # 2. Convert keywords to lowercase for case-insensitive matching
    #
    # 3. Create an empty list for filtered results
    #
    # 4. Loop through each job
    #
    # 5. Check if ANY keyword is in the job title (use 'in' operator)
    #
    # 6. Return filtered list

    filtered_jobs = []

    for job in jobs:
        title = job['title'].lower()

        if any(keyword in title for keyword in keywords):
            filtered_jobs.append(job)

    return filtered_jobs


def display_jobs(jobs: list[dict], total_jobs:int) -> None:
    """
    Display jobs in a nice, readable format.
    
    Args:
        jobs: List of job dictionaries to display
    """
    
    # TODO 6: Create a nice display for the jobs

    print("=" * 50)
    print("Filtered jobs")
    print("=" * 50)

    print(f"Total: {total_jobs} job(s) found\n")

    for job in jobs:
        print(f'{job['title']}')
        print(f'{job['url']}\n')

# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main():
    """
    Main function that ties everything together.
    """
    
    # Configuration
    URL = "https://www.thanksben.com/careers"
    
    # TODO 7: Add keywords you want to filter by
    KEYWORDS = [
        "engineer", 
        "frontend", 
        "backend",
        "developer"
    ]
    
    print("=" * 50)
    print(" Job Scraper - Learning Version")
    print("=" * 50)
    print(f"\nTarget: {URL}")
    print(f"Keywords: {', '.join(KEYWORDS) if KEYWORDS else 'None (showing all jobs)'}")
    
    all_jobs = fetch_injected_html_selenium(URL)

    if KEYWORDS:
        print(f"\n[Step 4] Jobs matching keywords ({', '.join(KEYWORDS)}):")
        filtered_jobs = filter_jobs_by_keywords(all_jobs, KEYWORDS)
        
        if filtered_jobs is None:
            print("ERROR: filter_jobs_by_keywords returned None. Check your function!")
        else:
            display_jobs(filtered_jobs, len(all_jobs))

    # # Step 1: Fetch the page
    # print("\n[Step 1] Fetching page...")
    # html = fetch_page(URL)
    
    # if html is None:
    #     print("ERROR: Failed to fetch the page. Check your fetch_page function!")
    #     return
    
    # print(f"Success! Fetched {len(html)} characters of HTML")
    
    # # Step 2: Parse job listings
    # print("\n[Step 2] Parsing job listings...")
    # all_jobs = parse_job_listings(html)
    # print(f"Found {len(all_jobs)} job(s)")
    
    # # Step 3: Display all jobs
    # print("\n[Step 3] All Jobs:")
    # display_jobs(all_jobs)
    
    # # Step 4: Filter and display (if keywords provided)
    # if KEYWORDS:
    #     print(f"\n[Step 4] Jobs matching keywords ({', '.join(KEYWORDS)}):")
    #     filtered_jobs = filter_jobs_by_keywords(all_jobs, KEYWORDS)
        
    #     if filtered_jobs is None:
    #         print("ERROR: filter_jobs_by_keywords returned None. Check your function!")
    #     else:
    #         display_jobs(filtered_jobs)


# =============================================================================
# RUN THE SCRIPT
# =============================================================================

if __name__ == "__main__":
    main()


# =============================================================================
# BONUS CHALLENGES (After completing all TODOs)
# =============================================================================
"""
Once you've completed the basic scraper, try these challenges:

CHALLENGE 1: Save to File
--------------------------
Create a function save_jobs_to_csv(jobs, filename) that saves 
the jobs to a CSV file. Use Python's built-in 'csv' module.

CHALLENGE 2: Multiple Keywords Match
--------------------------------------
Modify filter_jobs_by_keywords to accept a parameter 'match_all=False'
When match_all=True, only return jobs that match ALL keywords.

CHALLENGE 3: Scrape Job Details
--------------------------------
For each job URL, fetch the full page and extract:
- Full job description
- Location
- Department
- Requirements

CHALLENGE 4: Multiple Sites
----------------------------
Refactor to support scraping from multiple job sites.
Each site might need different parsing logic!

CHALLENGE 5: Scheduling
------------------------
Use the 'schedule' library to run the scraper every hour
and save new jobs to a file.

"""
