###
# Job Post WebScraper
###

# Use: [get_all_jobs(job_title, city)] function in order to run the code and return a dataframe


import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta


### Indeed Job Scraper


# Pulls Soup from Indeed
def load_indeed_jobs_div(job_title, location):
    getVars = {'q': job_title,'l': location, 'limit':25}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html5lib')
    return soup


#Extracts desired info from soup and creates DataFrame
def extract_job_information_indeed(soup):

    cols = ['titles', 'companies', 'links', 'dates']
    extracted_info = []

    companies = []
    titles = []
    links = []
    dates = []

    for x in soup.findAll(id='resultsCol'):
        for y in soup.findAll('div', class_='jobsearch-SerpJobCard'):

            company = y.find('span', class_='company')
            title = y.find('a')
            #title = y.find('h2', class_='title')
            link = y.find('a')['href']
            date = y.find('span', class_='date')

            companies.append(company.text.strip())
            titles.append(title.text.strip())
            links.append('https://www.indeed.com' + link)
            dates.append(date.text.strip())

    extracted_info.append(titles)
    extracted_info.append(companies)
    extracted_info.append(links)
    extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    indeed_df = pd.DataFrame(jobs_list)

    return indeed_df

# Clean Indeed DataFrame
def clean_indeed_df(indeed_df):

    # change date column to an actual date
    today = date.today()

    for x in range(len(indeed_df['dates'])):

        if indeed_df['dates'][x] == 'Just posted' or indeed_df['dates'][x] == 'Today':
            indeed_df['dates'][x] = today

        elif indeed_df['dates'][x] == '30+ days ago':
            indeed_df['dates'][x] = today - timedelta(days=30)

        else:
            for i in indeed_df['dates'][x].split():
                if i.isdigit():
                    num = int(i)

                indeed_df['dates'][x] = today - timedelta(days=num)

    # sort by dates column

    indeed_df['dates'] = pd.to_datetime(indeed_df['dates'])
    indeed_df['dates'] = indeed_df['dates'].dt.date


    indeed_df = indeed_df.sort_values(by='dates',ascending=False)

    return indeed_df

#Combine Indeed functions to one
def find_jobs_from_indeed(job_title, location):

    soup = load_indeed_jobs_div(job_title, location)
    indeed_df = extract_job_information_indeed(soup)

    indeed_df = clean_indeed_df(indeed_df)

    return indeed_df



### Monster Job Scraper


# Get monster soup
def load_monster_jobs_div(job_title, location):
    getVars = {'q': job_title,'where': location}
    url = ('https://www.monster.com/jobs/search/?' + urllib.parse.urlencode(getVars) + '&stpage=1&page=2')
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    return soup

#Extract data and make dataframe
def extract_job_information_monster(soup):

    cols = ['titles', 'companies', 'links', 'dates']
    extracted_info = []

    companies = []
    titles = []
    links = []
    dates = []

    for x in soup.findAll('section', class_='card-content'):
        for y in x.findAll('div', class_='flex-row'):

            company = y.find('div', class_='company')
            title = y.find('h2', class_='title')
            link = y.find('a')['href']
            date = y.find('time')

            companies.append(company.text.strip())
            titles.append(title.text.strip())
            links.append(link)
            dates.append(date.text.strip())

    extracted_info.append(titles)
    extracted_info.append(companies)
    extracted_info.append(links)
    extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    monster_df = pd.DataFrame(jobs_list)

    return monster_df

#Clean monster dataframe
def clean_monster_df(monster_df):

    #change date column to an actual date

    today = date.today()


    for x in range(len(monster_df['dates'])):

        if monster_df['dates'][x] == 'Posted today':
            monster_df['dates'][x] = today

        elif monster_df['dates'][x] == '+30 days ago':
            monster_df['dates'][x] = today - timedelta(days=30)

        else:
            for i in monster_df['dates'][x].split():
                if i.isdigit():
                    num = int(i)

                    monster_df['dates'][x] = today - timedelta(days=num)


    # sort by dates column

    monster_df['dates'] = pd.to_datetime(monster_df['dates'])
    monster_df['dates'] = monster_df['dates'].dt.date

    monster_df = monster_df.sort_values(by='dates',ascending=False)


    return monster_df

#Combine to one monster function
def find_jobs_from_monster(job_title, location):

    soup = load_monster_jobs_div(job_title, location)
    monster_df = extract_job_information_monster(soup)

    monster_df = clean_monster_df(monster_df)

    return monster_df


### Linkedin Job Scraper


# Get linkedin soup
def load_linkedin_jobs_div(job_title, location):
    getVars = {'keywords': job_title,'location': location}
    url = ('https://www.linkedin.com/jobs/search?' + urllib.parse.urlencode(getVars) + '&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0')
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    return soup

#Extract desired info and make dataframe
def extract_job_information_linkedin(soup):

    cols = ['titles', 'companies', 'links', 'dates']
    extracted_info = []

    companies = []
    titles = []
    links = []
    dates = []

    for x in soup.findAll('ul', class_='jobs-search__results-list'):
        for y in soup.findAll('li', class_='result-card job-result-card result-card--with-hover-state'):

            if y.find('a', class_='result-card__subtitle-link job-result-card__subtitle-link') is None:
                company = y.find('h4', class_='result-card__subtitle job-result-card__subtitle')
            else:
                company = y.find('a', class_='result-card__subtitle-link job-result-card__subtitle-link')

            title = y.find('h3', class_='result-card__title job-result-card__title')
            link = y.find('a', class_='result-card__full-card-link')['href']

            if y.find('time', class_='job-result-card__listdate') is not None:
                date = y.find('time', class_='job-result-card__listdate')

            else:
                date = y.find('time', class_='job-result-card__listdate--new')

            companies.append(company.text.strip())
            titles.append(title.text.strip())
            links.append(link)
            dates.append(date.text.strip())

    extracted_info.append(titles)
    extracted_info.append(companies)
    extracted_info.append(links)
    extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    linkedin_df = pd.DataFrame(jobs_list)

    return linkedin_df

#Clean dataframe
def clean_linkedin_df(linkedin_df):

    #change date column to an actual date

    today = date.today()

    for x in range(len(linkedin_df['dates'])):

        for i in linkedin_df['dates'][x].split():
            if i.isdigit():
                num = int(i)

        linkedin_df['dates'][x] = today - timedelta(days=num)

    # sort by dates column

    linkedin_df['dates'] = pd.to_datetime(linkedin_df['dates'])
    linkedin_df['dates'] = linkedin_df['dates'].dt.date

    linkedin_df = linkedin_df.sort_values(by='dates',ascending=False)


    return linkedin_df

# Combine linkedin to function
def find_jobs_from_linkedin(job_title, location):

    soup = load_linkedin_jobs_div(job_title, location)
    linkedin_df = extract_job_information_linkedin(soup)

    linkedin_df = clean_linkedin_df(linkedin_df)

    return linkedin_df

### Combine all scrapers to one dataframe and clean up
### Final function for the webscraper. Run this function to get the job postings on a dataframe

def get_all_jobs(job_title, location):
    l_df = find_jobs_from_linkedin(job_title,location)
    i_df = find_jobs_from_indeed(job_title,location)
    m_df = find_jobs_from_monster(job_title,location)

    # concat the dataframe together
    # NOTE: Put i_df back in frames list to reintroduce indeed back if you fix it!!!
    frames = [i_df,m_df,l_df]
    job_df = pd.concat(frames)

    # remove duplicates (same title and companies)
    job_df = job_df.drop_duplicates(subset=['titles','companies'])

    # sort new dataframe by date
    job_df = job_df.sort_values(by='dates',ascending=False)

    # now that it's sorted correctly, drop dates column
    #job_df.drop(axis=1,labels='dates',inplace=True)


    # reset index of dataframe so numbers are in order
    job_df = job_df.reset_index(drop=True)

    # turn dataframe into four lists: titles,companies,links,dates
    titles = job_df['titles'].to_list()
    companies = job_df['companies'].to_list()
    links = job_df['links'].to_list()
    dates = job_df['dates'].to_list()

    return (titles,companies,links,dates)
