from bs4 import BeautifulSoup
import requests
import csv
import re

url = 'https://skillup.org/blog/tech-careers-in-demand'

response = requests.get(url)

skill_up = response.text

soup = BeautifulSoup(skill_up, 'html.parser')

jobs = soup.find('div', {'class': 'blog-detail-content'})

#use heading as the starting point
job_titles = jobs.find_all('h3')
for job in job_titles:
    job_title_elem = job.text.split()
    del job_title_elem[0]
    job_title = ' '.join(job_title_elem)


    job_description = job.find_next_sibling('p')

    job_p_tag = job_description.find_next_sibling('p')
    job_strong_tags = job_p_tag.find_all('strong')

    #median annual salary
    job_median_base = job_strong_tags[0]
    job_median_amount = job_p_tag.find('a').text
    
    #estimated growth over 10 years
    job_growth_base = job_strong_tags[1]
    job_growth_percent = job_growth_base.next_sibling.text.split()[1]
    job_growth_list = list(job_growth_percent)
    del job_growth_list[0]
    job_growth = ''.join(job_growth_list)


    #skills needed
    skills_needed_base = job_strong_tags[2]
    skills_needed_title = skills_needed_base.text
    skills_needed = skills_needed_base.next_sibling.text.split()
    del skills_needed[0]
    skills = ' '.join(skills_needed)