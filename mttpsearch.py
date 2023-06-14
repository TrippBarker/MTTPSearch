from googlesearch import search
from datetime import date

today = date.today()

query = f'"clinical" "application" "specialist" "remote" -"research" -"trial" -"trials" -"pharmacy technician" after:{today} site:"www.linkedin.com"'

for i in search(query, tld="com", num=10, stop=20, pause=2):
    print(i)