## **How to Use**
Clone the Repository: Begin by cloning this repository to your local machine using Git:
git clone <repository_url>
Install Dependencies: Navigate to the directory containing the script and install the required dependencies using pip:
pip install -r requirements.txt
Run the Script: Execute the script by running the main Python file:
python main.py
Review Output: Once the script finishes execution, review the output CSV file named Scrapped.csv. This file contains the scraped data from the websites related to the search query.

## **Configuration**
Search Query: Modify the search_query variable in the script to specify the topic you want to search for.
Number of Results: Adjust the num_results_per_query variable to control the number of search results to retrieve from Google.
Target Samples: Set the num_samples_target variable to determine the total number of samples to collect.
Samples per Site: Define the num_samples_per_site variable to specify how many samples to collect from each website.
Output File: Change the output_filename variable to specify the name of the output CSV file.

## **Proxy Usage**
The script utilizes proxies for web scraping to enhance anonymity and avoid IP blocking. Proxies are obtained from a public proxy list and rotated for each request.

## **Disclaimer**
This script is provided for educational and research purposes only. Ensure that your use of the script complies with the terms of service of the websites being scraped.
Use caution when scraping websites to avoid violating any laws or terms of service.
The authors of this script are not responsible for any misuse or unethical use of the provided code.
