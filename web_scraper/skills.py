from bs4 import BeautifulSoup
import requests
import common

def get_skills():
    base_url = 'https://stardewvalleywiki.com/Skills'
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    skills = []

    skill_classes = soup.select('.mw-headline')
    for span in skill_classes:
        skill = span.select("a")
        if len(skill) > 0 and "Skill_Icon" in skill[0].get("href"):
            skills.append((span.text.strip(),))

    return skills


def insert_skills(cur):
    skills = get_skills()
    sql_string = "INSERT INTO skills(skill_type) VALUES (%s);" 
    
    cur.executemany(sql_string, [skill for skill in skills])