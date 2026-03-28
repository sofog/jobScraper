"""
Job Scraper for ThanksBen Careers Page
=======================================
This script scrapes job listings from https://www.thanksben.com/careers
and filters them based on provided keywords.

Requirements:
    pip install requests beautifulsoup4

Usage:
    python job_scraper.py
"""

import requests
from bs4 import BeautifulSoup


def fetch_page(url: str) -> str:
    """
    Fetch the HTML content of a webpage.
    
    Args:
        url: The URL to fetch
        
    Returns:
        The HTML content as a string
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.text


def parse_job_listings(html: str) -> list[dict]:
    """
    Parse job listings from the HTML content.
    
    Args:
        html: The HTML content of the careers page
        
    Returns:
        A list of dictionaries containing job information
    """
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    
    # Find all job listing elements
    # The structure from the site shows jobs in a specific format
    # We'll look for common job listing patterns
    
    # Try to find job cards/links - adjust selectors based on actual HTML structure
    job_elements = soup.find_all("div", href=True)
    
    for element in job_elements:
        href = element.get("href", "")
        
        # Look for links that might be job postings (often contain "apply" or job-related paths)
        if "/jobs/" in href or "apply" in href.lower() or "position" in href.lower():
            title = element.get_text(strip=True)
            if title:  # Only add if there's a title
                jobs.append({
                    "title": title,
                    "url": href if href.startswith("http") else f"https://www.thanksben.com{href}",
                })
    
    # Alternative: Look for specific job listing structures
    # Many sites use specific classes or data attributes for jobs
    job_cards = soup.select("[class*='job'], [class*='career'], [class*='position'], [class*='opening']")
    
    for card in job_cards:
        link = card.find("a", href=True)
        title_elem = card.find(["h2", "h3", "h4", "strong"])
        
        if link and title_elem:
            title = title_elem.get_text(strip=True)
            href = link.get("href", "")
            
            # Avoid duplicates
            if not any(j["title"] == title for j in jobs):
                jobs.append({
                    "title": title,
                    "url": href if href.startswith("http") else f"https://www.thanksben.com{href}",
                })
    
    return jobs


def filter_jobs_by_keywords(jobs: list[dict], keywords: list[str]) -> list[dict]:
    """
    Filter jobs based on keywords found in the title.
    
    Args:
        jobs: List of job dictionaries
        keywords: List of keywords to search for (case-insensitive)
        
    Returns:
        Filtered list of jobs matching at least one keyword
    """
    if not keywords:
        return jobs
    
    keywords_lower = [kw.lower() for kw in keywords]
    filtered = []
    
    for job in jobs:
        title_lower = job["title"].lower()
        # Check if any keyword is in the title
        if any(keyword in title_lower for keyword in keywords_lower):
            filtered.append(job)
    
    return filtered


def display_jobs(jobs: list[dict], title: str = "Job Listings") -> None:
    """
    Display jobs in a formatted way.
    
    Args:
        jobs: List of job dictionaries
        title: Header title to display
    """
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    
    if not jobs:
        print("No jobs found matching your criteria.")
        return
    
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Link: {job['url']}")
    
    print(f"\n{'='*60}")
    print(f"Total: {len(jobs)} job(s) found")
    print(f"{'='*60}\n")


def main():
    """Main function to run the job scraper."""
    
    # Configuration
    URL = "https://www.thanksben.com/careers"
    
    # Keywords to filter jobs - add your desired keywords here
    # KEYWORDS = [
    #     "engineer",
    #     "developer",
    #     "frontend",
    #     "backend",
    #     "senior",
    # ]
    
    print("Job Scraper Starting...")
    print(f"Target URL: {URL}")
    # print(f"Filter Keywords: {', '.join(KEYWORDS)}")
    
    try:
        # Step 1: Fetch the page
        print("\nFetching page...")
        html = fetch_page(URL)
        print("Page fetched successfully!")
        
        # Step 2: Parse job listings
        print("Parsing job listings...")
        all_jobs = parse_job_listings(html)
        print(f"Found {len(all_jobs)} total job(s)")
        
        # Step 3: Display all jobs
        display_jobs(all_jobs, "All Job Listings")
        
        # # Step 4: Filter and display matching jobs
        # if KEYWORDS:
        #     filtered_jobs = filter_jobs_by_keywords(all_jobs, KEYWORDS)
        #     display_jobs(filtered_jobs, f"Jobs Matching Keywords: {', '.join(KEYWORDS)}")
        
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
