from googlesearch import search
from datetime import date
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import time
import requests
import openpyxl

# Read term txt files into lists
def createList(fileLoc):
    termsFile = open(fileLoc, "r")
    termsData = termsFile.read()
    return termsData.split("\n")
clinTermsList = createList("terms/clinicalTerms.txt")
techTermsList = createList("terms/techTerms.txt")
jobTermsList = createList("terms/jobTerms.txt")
badTermComboList = createList("terms/badTermCombo.txt")
sitesList = createList("terms/sites.txt")
nonoTermsList = createList("terms/nonoTerms.txt")
alwaysTermsList = createList("terms/alwaysTerms.txt")
clinTerm = ""
techTerm = ""
jobTerm = ""
site = ""


xlBook = openpyxl.Workbook()
linkedInSheet = xlBook.active
linkedInSheet.title = "LinkedIn"
data = (("date", "company", "job title", "area", "link", "term used"),)

today = date.today()

def getLinkedInJobs(query):
    data = ()
    for i in search(query, tld="com", num=1, stop=1, pause=2):
        page = requests.get(i)
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.find("title")
        if title == None:
            data += (("none", "none", "none", "none", "none", "none"),)
        else:
            if "hiring" in title.string:
                company = title.string[0:title.string.find("hiring")]
                jobTitle = title.string[title.string.find("hiring")+7:title.string.find(" in ")]
                area = title.string[title.string.find(" in ")+4:title.string.find(" | LinkedIn")]
                link = i
                termUsed = f'{clinTerm} {techTerm} {jobTerm}'
                data += ((today, company, jobTitle, area, link, termUsed),)
    for entry in data:
        linkedInSheet.append(entry)

query = f'"{clinTerm}" "{techTerm}" "{jobTerm}" "remote" -"research" -"trial" -"trials" -"pharmacy technician" after:{today} site:"linkedin.com"'
for termOne in clinTermsList:
    badTerm = False
    clinTerm = termOne
    for termTwo in techTermsList:
        techTerm = termTwo
        for termThree in jobTermsList:
            jobTerm = termThree
            query = f'"{clinTerm}" "{techTerm}" "{jobTerm}" "remote" -"research" -"trial" -"trials" -"pharmacy technician" after:{today} site:"linkedin.com"'
            for term in badTermComboList:
                if f'{clinTerm} {techTerm} {jobTerm}' == term:
                    badTerm = True
                    break
            if  badTerm:
                continue
            else:
                try:
                    getLinkedInJobs(query)
                except HTTPError:
                    print("HTTPError occurred")
                    continue
                print(f'{termOne} {termTwo} {termThree} done')
                #time.sleep(10)
            
xlBook.save('mttpJobSearch.xlsx')