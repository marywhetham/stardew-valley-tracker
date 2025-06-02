from bs4 import BeautifulSoup
import requests

def get_goals():
    base_url = 'https://stardewvalleywiki.com/Adventurer%27s_Guild'
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    table = next(
        (table for table in soup.find_all("table")
        if table.find("th", string=lambda text: text and "Monster Type" in text)),
        None
    )

    goals = []

    table_body = table.find("tbody")
    for tr in table_body.find_all("tr"):
        first_td = tr.find("td")
        if first_td:
            td_id = first_td.get("id") if first_td else None
            monster = td_id.replace("_", " ")
            quantity_text = first_td.find_next_sibling('td').text
            quantity = quantity_text.replace("\n", "")
            goals.append((monster, quantity))

    return goals

def insert_goals(cur):
    goals = get_goals()
    sql_string = "INSERT INTO monster_slayer_goals(monster_type, quantity) VALUES (%s, %s);" 
    
    cur.executemany(sql_string, [goal for goal in goals])