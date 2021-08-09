# Imports
import time

from selenium import webdriver
import os
from util import already_applied, findFileLocationForCompany, moveOldJobs

'''
Guidance:
1. The program will update oldJobs and will refresh new Jobs
'''


def findJobsElbit(file_object_new, table):
    # table = driver.find_element_by_xpath('/html/body/main/div/div[1]/div[1]/div/div[2]/form/table')
    for row in table.find_elements_by_xpath(".//tr")[1:]:
        row_details = row.find_elements_by_tag_name('td')
        job_name = str(row_details[0].text)
        job_id = str(row_details[1].text)
        if job_name.find('תכנה') > 0 or \
                job_name.find('תוכנה') > 0 or \
                job_name.lower().find('software') > 0:
            if not already_applied(job_id):
                file_object_new.write(f'''
{job_name}
{job_id}
''')


def findJobsIntel(file_object_new, table):
    for row in table.find_elements_by_xpath(".//tr")[1:]:
        row_details = row.find_elements_by_tag_name('td')
        job_id = str(row_details[0].text).split(' ')[0]
        job_name = str(row_details[0].text).split(' - ')[1]
        job_location = str(row_details[2].text)
        job_link = row.find_element_by_tag_name('a').get_attribute('href')

        if job_location != 'Haifa':
            pass

        if job_name.lower().find('data') > 0 \
                or job_name.lower().find('computer') > 0 \
                or job_name.lower().find('software') > 0 \
                or job_name.lower().find('deep') > 0 \
                or job_name.lower().find('algorithms') > 0\
                or job_name.lower().find('development') > 0:
            if not already_applied(job_id):
                file_object_new.write(f'''
{job_name}
{job_id}
{job_link}
''')


def elbit():
    file_object_new = open("NewJobs.txt", 'a')
    file_object_new.write("Elbit systems:\n")
    page = 1
    while True:
        driver.get(
            f'https://elbitsystemscareer.com/search-results/?pager-page={page}&professionalFields%5B0%5D=46&areas%5B%5D=6')
        table = driver.find_element_by_xpath('/html/body/main/div/div[1]/div[1]/div/div[2]/form/table')
        # Table size with headlines only is 72
        if table.find_elements_by_xpath(".//tr").__sizeof__() > 72:
            findJobsElbit(file_object_new, table)
            page += 1
        else:
            file_object_new.close()
            return


def intel():
    file_object_new = open("NewJobs.txt", 'a')
    file_object_new.write("Intel:\n")
    page = 1
    while True:
        driver.get(f'https://jobs.intel.com/page/show/student-jobs-israel/Page-{page}')
        table = driver.find_element_by_xpath(
            '//*[@id="mainContent"]/div/div[2]/div/div/div[1]/span/span/span/div/table')
        # Table height with headlines only is 38
        table_size = int(table.find_element_by_xpath('.//tr').size['height'])
        if table_size > 38:
            findJobsIntel(file_object_new, table)
            page += 1
        else:
            file_object_new.close()
            return


driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe')
# driver.minimize_window()

if not os.path.exists('OldJobs.txt'):
    handle = open('OldJobs.txt', "w")
    handle.close()

if not os.path.exists('NewJobs.txt'):
    handle = open("NewJobs.txt", "w")
    handle.close()

# Move all old jobs to old jobs file
moveOldJobs()

# Calling fucntions according to the sites.
driver.minimize_window()
elbit()
intel()
driver.close()
