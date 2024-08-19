import http.client
import json
import csv
from datetime import datetime, timedelta
import os
import re

def extract_job_id(url):
    match = re.search(r'/(\d+)/', url)
    return match.group(1) if match else None

def get_existing_jobs(filename):
    existing_jobs = set()
    if os.path.exists(filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                job_id = extract_job_id(row['Job Posting URL'])
                if job_id:
                    existing_jobs.add(job_id)
    return existing_jobs

def make_api_request(offset=0):
    conn = http.client.HTTPSConnection("linkedin-data-scraper.p.rapidapi.com")
    payload = json.dumps({
        "keywords": "Machine Learning Engineer",
        "location": "United States",
        "count": 100,
        "offset": offset
    })
    x_key = os.getenv("X_API")
    if not x_key:
        print("Error: X_API environment variable is not set.")
        exit(1)
    headers = {
        'x-rapidapi-key': x_key,
        'x-rapidapi-host': "linkedin-data-scraper.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    conn.request("POST", "/search_jobs", payload, headers)
    res = conn.getresponse()
    return res.read()

def is_recent_job(posted_time):
    job_time = datetime.strptime(posted_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    return (datetime.now() - job_time) <= timedelta(days=1)

def process_jobs(json_data, existing_job_ids):
    new_jobs = []
    if 'response' in json_data and json_data['response']:
        for job in json_data['response'][0]:
            job_id = extract_job_id(job['jobPostingUrl'])
            if job_id and is_recent_job(job['listedAt']) and job_id not in existing_job_ids:
                new_jobs.append({
                    'Job ID': job_id,
                    'Job Title': job['title'],
                    'Company Name': job['companyName'],
                    'Job Posting URL': job['jobPostingUrl']
                })
    return new_jobs

def main():
    csv_file = "recent_linkedin_jobs.csv"
    existing_job_ids = get_existing_jobs(csv_file)
    new_jobs = []
    offset = 0

    while len(new_jobs) < 300:
        try:
            data = make_api_request(offset)
            json_data = json.loads(data.decode("utf-8"))
            batch_jobs = process_jobs(json_data, existing_job_ids)
            new_jobs.extend(batch_jobs)
            offset += 100
            if not batch_jobs:
                break  # No more new jobs found
        except Exception as e:
            print(f"Error processing batch: {e}")
            break

    new_jobs = new_jobs[:300]  # Limit to 300 new jobs

    # Append new jobs to the CSV file
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Job ID', 'Job Title', 'Company Name', 'Job Posting URL'])
        if file.tell() == 0:  # File is empty, write header
            writer.writeheader()
        writer.writerows(new_jobs)

    print(f"Number of new jobs added: {len(new_jobs)}")
    print(f"Total unique jobs in file: {len(existing_job_ids) + len(new_jobs)}")

    # Print first few new entries
    print("\nFirst few new entries:")
    for job in new_jobs[:5]:
        print(job)

if __name__ == "__main__":
    main()