# get course code
# check if exists
# select offering

import requests
from bs4 import BeautifulSoup
import re
import string

# base url
base_url = "https://programs-courses.uq.edu.au/course.html?course_code="

def main():

    # while True:
    #get course code, check if valid
        ccode = input("What course code would you like to look at: ")
        response = requests.get(base_url + ccode)
        resoup = BeautifulSoup(response.content, 'html.parser')
        content = resoup.find(id="course-notfound")

        while content is not None:
            ccode = input("Course code does not exist. Try again: ")
            response = requests.get(base_url + ccode)
            resoup = BeautifulSoup(response.content, 'html.parser')
            content = resoup.find(id="course-notfound")

        resoup = BeautifulSoup(response.content, 'html.parser')
        cur_offeringss = resoup.find(id="course-current-offerings")
        
        if cur_offeringss is None:
            print("Course is not offered.")
            return
        
        # finding ecp link
        #let user choose
        print("The following offerings are available:")
        offerings = cur_offeringss.findAll(class_="course-offering-year")

        for counter, c in enumerate(offerings, start=1):
            print(str(counter) + ". " + c.text)

        choice = int(input("Which option would you like to view: "))
        while choice < 1 or (choice - 1) > counter:
            choice = int(input("Try again: "))

        all_profiles = cur_offeringss.findAll('a', class_="profile-available", href=True)
        ecp_url = all_profiles[choice - 1]['href']

        # now try accessing the current ecp
        ecp_results = requests.get(ecp_url)
        ecpsoup = BeautifulSoup(ecp_results.content, 'html.parser')
        temp = ecpsoup.find(id="assessment--section").find_all('tr')

        collected_data = []
        for t in temp:
            stuff = t.findAll('p')
            print(stuff)
            print("/////////////////////////////////////////")
            # now regex for due dates and titles
            for s in stuff:
                name_n_datetime = re.search(r"(.*\s)?\d{1,2}\/\d{2}\/\d{4}\s\d{1,2}:\d{1,2}\s[ap]m", s.text)
                if name_n_datetime is not None:
                    separated = re.split(r"(\d{1,2}\/\d{2}\/\d{4}\s\d{1,2}:\d{1,2}\s[ap]m)", name_n_datetime.string.strip())
                    separated = [x for x in separated if x != ""]
                    print(separated)
    


if __name__ == "__main__":
    main()