import csv
import time
from googlesearch import search
from bs4 import BeautifulSoup
import requests

def get_valid_proxies():
    proxy_list_url = 'https://free-proxy-list.net/'
    response = requests.get(proxy_list_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_data = []
    rows = soup.find_all('tr')[1:]
    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 8:
            ip_address = columns[0].text.strip()
            google_enabled = columns[5].text.strip().lower() == 'yes'
            https_enabled = columns[6].text.strip().lower() == 'yes'
            last_checked = columns[7].text.strip()
            if (last_checked.endswith('mins ago') and int(last_checked.split(' ')[0]) < 15) or last_checked.endswith('hours ago'):
                if google_enabled or https_enabled:
                    proxy_data.append({'ip_address': ip_address, 'google_enabled': google_enabled, 'https_enabled': https_enabled})

    return proxy_data

def rotate_user_agent(proxy):
    if proxy:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    return headers

def scrape_website(url, proxy):
    try:
        headers = rotate_user_agent(proxy)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        paragraphs = soup.find_all('p')
        num_headings = len(headings)
        num_paragraphs = len(paragraphs)
        if num_headings > 0 or num_paragraphs > 0:
            headings_text = ' '.join([heading.text.strip().replace('\n', ' ') for heading in headings])
            paragraphs_text = ' '.join([paragraph.text.strip().replace('\n', ' ') for paragraph in paragraphs])
            extracted_data = {
                "source": url,
                "num_headings": num_headings,
                "num_paragraphs": num_paragraphs,
                "headings_text": headings_text,
                "paragraphs_text": paragraphs_text
            }
            return extracted_data
        else:
            print(f"No relevant tags found on {url}")
            return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def save_data_to_csv(data_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['source', 'num_headings', 'num_paragraphs', 'headings_text', 'paragraphs_text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)

def google_search(query, num_results):
    search_results = list(search(query, num_results=num_results))
    return search_results

def main():
    search_query = 'Causes of death in Pakistan'
    num_results_per_query = 50 
    num_samples_target = 2500
    num_samples_per_site = 100  
    output_filename = 'Scrapped.csv'
    valid_proxies = get_valid_proxies()
    scraped_data = []
    total_samples = 0
    for link in google_search(search_query, num_results_per_query):
        proxy = valid_proxies[total_samples % len(valid_proxies)] if valid_proxies else None
        data = scrape_website(link, proxy)
        if data:
            scraped_data.append(data)
            total_samples += 1
            if total_samples % num_samples_per_site == 0:
                time.sleep(5) 
            if total_samples >= num_samples_target:
                break

    save_data_to_csv(scraped_data, output_filename)

if __name__ == "__main__":
    main()

