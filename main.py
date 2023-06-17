import csv
import requests
from bs4 import BeautifulSoup

file = open('linkedin-jobs.csv', 'a')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'Location', 'Apply'])

def linkedin_scraper(webpage, page_number):
    next_page = webpage + str(page_number)
    print(str(next_page))
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.content, 'html.parser')

    print(response)
    print(page_number)

    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for job in jobs:
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        job_location = job.find('span', class_='job-search-card__location').text.strip()
        job_link = job.find('a', class_='base-card__full-link')['href']

        writer.writerow([
        job_title.encode('utf-8'),
        job_company.encode('utf-8'),
        job_location.encode('utf-8'),
        job_link.encode('utf-8')])

    print('Data updated')

    if page_number < 25:
        page_number = page_number + 25
        linkedin_scraper(webpage, page_number)
    else:
        file.close()
        print('File closed')

linkedin_scraper('http://api.scraperapi.com?api_key=3aa2658fe9ad992545604156527130e7&url=https://www.linkedin.com/jobs/search?keywords=Grafisch+Ontwerp&location=%27s-Hertogenbosch%2C+Noord-Brabant%2C+Nederland&geoId=103933617&trk=public_jobs_jobs-search-bar_search-submit', 0)


