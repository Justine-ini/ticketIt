import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search


def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def find_emails_on_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = extract_emails(soup.get_text())
        return emails
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def get_company_email(company_name):
    keywords = ['complaint', 'enquiry', 'support', 'feedback', 'resolution', 'help', 'info', 'customercare', 'customerservice']
    email_found = None

    for keyword in keywords:
        if email_found:
            break
        query = f"{company_name} {keyword} email"
        search_results = search(query, num_results=5)
        
        for url in search_results:
            if email_found:
                break
            print(f"Searching {url} for email addresses...")
            emails = find_emails_on_page(url)
            if emails:
                for email in emails:
                    if any(k in email for k in keywords):
                        print(f"Found email: {email}")
                        email_found = email
                        break
            else:
                print(f"No email addresses found on {url}")

    if not email_found:
        print("No email address found that matches the keywords.")
    
    return email_found
