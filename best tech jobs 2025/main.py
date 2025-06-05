from bs4 import BeautifulSoup
import requests
import csv
import re

url = 'https://skillup.org/blog/tech-careers-in-demand'

response = requests.get(url)

skill_up = response.text

soup = BeautifulSoup(skill_up, 'html.parser')

jobs = soup.find('div', {'class': 'blog-detail-content'})

job_titles = jobs.find_all('h3')
for job in job_titles:
    print(job.text)