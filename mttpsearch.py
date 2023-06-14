from googlesearch import search

query = '"clinical project manager" +"remote" -"research" -"trial" -"trials"after:2023-06-14 site:"www.linkedin.com"'

for i in search(query, tld="com", num=10, stop=20, pause=2):
    print(i)