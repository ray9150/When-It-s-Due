# get course code
# check if exists
# select offering

import requests
from bs4 import BeautifulSoup

# base url
base_url = "https://programs-courses.uq.edu.au/course.html?course_code="

def main():

    # while True:
    #get course code, check if valid
        ccode = input("What course code would you like to look at: ")
        response = requests.get(base_url + ccode)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find(id="course-notfound")

        print(content)

        while content is not None:
            ccode = input("Course code does not exist. Try again: ")
            response = requests.get(base_url + ccode)
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find(id="course-notfound")

        soup = BeautifulSoup(response.content, 'html.parser')
        cur_offeringss = soup.find(id="course-current-offerings")
        
        if cur_offeringss is None:
            print("Course is not offered.")
            return
        
        # finding ecp link
        cur_offerings = cur_offeringss.find(class_='current')
        cur_offering = cur_offerings.find('a', href=True, class_="profile-available")
        ecp_url = cur_offering["href"]
        print(ecp_url)

        # now try accessing the current ecp
        ecp_results = requests.get(ecp_url)
        print(ecp_results.text)


if __name__ == "__main__":
    main()