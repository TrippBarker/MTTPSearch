from googlesearch import search
from datetime import date
from bs4 import BeautifulSoup
import requests
import openpyxl

xlBook = openpyxl.Workbook()
linkedInSheet = xlBook.active
data = (("date", "company", "job title", "area", "link"),)

today = date.today()

query = f'"clinical" "application" "specialist" "remote" -"research" -"trial" -"trials" -"pharmacy technician" after:{today} site:"linkedin.com"'


for i in search(query, tld="com", num=10, stop=10, pause=2):
    page = requests.get(i)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find("title")
    if "hiring" in title.string:
        company = title.string[0:title.string.find("hiring")]
        jobTitle = title.string[title.string.find("hiring")+7:title.string.find(" in ")]
        area = title.string[title.string.find(" in ")+4:title.string.find(" | LinkedIn")]
        link = i
        data += ((today, company, jobTitle, area, link),)

for entry in data:
    linkedInSheet.append(entry)
xlBook.save('mttpJobSearch.xlsx')