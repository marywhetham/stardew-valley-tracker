from bs4 import BeautifulSoup
import requests
import pprint

def get_item_info(info):
    url = 'https://stardewvalleywiki.com' + info["link"]
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    
    seasons = []
    sources = []

    info_table = soup.select_one("#infoboxtable")
    if info_table:
        season_info = get_info_from_table(info_table, "Season")
        if season_info:
            seasons = [season for season in map(lambda link: determine_season(link.text), season_info) if season is not None]

        source_info = get_info_from_table(info_table, "Source")
        if source_info:
            sources = list(map(lambda link: link.text, source_info))

        growth_time = info_table.find("td", string=lambda text: text and "Growth Time" in text)
        if growth_time:
            sources.append("Farming")

    return (info["name"], seasons if seasons else None, sources if sources else None)

def get_info_from_table(table, desc_name):
    tr_with_source = next(
        (tr for tr in table.find_all("tr") if tr.find("td", string=lambda text: text and desc_name in text)),
        None
    )
    return tr_with_source.select("a") if tr_with_source is not None else None

def determine_season(season):
    if (season == "Spring"):
        return 1
    elif (season == "Summer"):
        return 2
    elif (season == "Fall"):
        return 3
    elif (season == "Winter"):
        return 4

def get_items():
    base_url = 'https://stardewvalleywiki.com/Shipping#Collections'
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    items = soup.select('.wikitable a')
    item_infos = list(map(lambda link: { "name": link.text, "link": link.get("href")}, items))

    final_item_infos = []

    for info in item_infos:
        response = get_item_info(info)
        final_item_infos.append(response)
    
    return final_item_infos


def insert_items(cur):
    items = get_items()
    sql_string = "INSERT INTO items(item_name, seasons, sources) VALUES (%s, %s, %s);" 
    
    cur.executemany(sql_string, [item for item in items])

