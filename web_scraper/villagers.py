from bs4 import BeautifulSoup
import requests
import common

def get_villager_info(info):
    url = 'https://stardewvalleywiki.com' + info["link"]
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    birthday = None
    location = None

    info_table = soup.select_one("#infoboxtable")
    if info_table:
        birthday_info = common.get_tr_from_table(info_table, "Birthday")
        if birthday_info:
            birthday = birthday_info.select("a")[0].text + " " + birthday_info.select("#infoboxdetail")[0].find(string=True, recursive=False).strip()

        location_info = common.get_links_from_table(info_table, "Address")
        if location_info:
            location = location_info[0].get("title")

    return (info["name"], birthday, location)


def get_villagers():
    base_url = 'https://stardewvalleywiki.com/Villagers'
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    titles = ["Bachelors", "Bachelorettes", "Non-marriage candidates"]
    links = []
    for title in titles:
        links += get_links(soup, title, 'h2' if title == "Non-marriage candidates" else 'h3')
    villagers = [villager for villager in map(lambda link: { "name": link.text, "link": link.get("href")}, links) if len(villager["name"]) > 0]
    
    final_villager_infos = []

    for villager in villagers:
        response = get_villager_info(villager)
        final_villager_infos.append(response)
    
    return final_villager_infos
    

def get_links(soup, title, h):
    span = soup.find('span', string=title)
    heading = span.find_parent(h)
    ul = heading.find_next_sibling('ul')
    return ul.select('a')
    

def insert_villagers(cur):
    villagers = get_villagers()
    villagers = list(map(lambda villager: update_location(villager, cur), villagers))

    sql_string = "INSERT INTO villagers(villager_name, birthday, home_location_id) VALUES (%s, %s, %s);" 
    cur.executemany(sql_string, [villager for villager in villagers])

def update_location(villager, cur):
    sql_string = "SELECT location_id FROM locations WHERE location_name = %s"
    if not villager[2]:
        return villager[:2] + (392,)
    cur.execute(sql_string, (villager[2],))
    location = cur.fetchone()
    return villager[:2] + (location)