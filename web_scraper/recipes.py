from bs4 import BeautifulSoup
import requests
import re
import pprint

def get_ingredients(ingredient_text):
    ingredents = []

    items = ingredient_text.select(".nametemplate")
    for item in items:
        name = item.select("a")[0].text
        amount = re.search(r'\d+', item.text).group()
        ingredents.append({ name: amount})

    return ingredents

def get_recipe_source(recipe_source_text):
    sources = []
    queen_of_sauce = recipe_source_text.find("a", title="The Queen of Sauce")
    if queen_of_sauce:
        parent_tr = queen_of_sauce.find_parent("tr")
        date_tr = parent_tr.find_next_sibling("tr")
        date = date_tr.find("td").text.replace("\n", "")
        sources.append({ "queen_of_sauce": date })

    villager_ps = recipe_source_text.find_all("p")
    for villager_p in villager_ps:
        villager_text = villager_p.text
        if not villager_p:
            continue
        if "Mail -" in villager_text or "heart event" in villager_text:
            person = villager_text.split("\xa0")[0].strip()
            hearts = re.search(r'\d+', villager_text).group()
            sources.append({ "villager": person, "hearts": hearts })

    source_text = recipe_source_text.text.strip()
    if "Level" in source_text:
        skill = source_text.split(" ")[0].strip()
        skill = skill.split("\xa0")[0].strip()
        level = re.search(r'\d+', source_text).group()
        sources.append({ skill: level})
    elif "Stardrop Saloon" in source_text:
        amount = re.search(r'data-sort-value="(\d+)"', source_text).group(1)
        sources.append({"stardrop_saloon": int(amount)})
    elif "Dwarf Shop" in source_text:
        amount = re.search(r'data-sort-value="(\d+)"', source_text).group(1)
        sources.append({"dwarf_shop": int(amount)})
    elif "Island Trader" in source_text:
        amount = re.search(r'\d+', source_text).group()
        sources.append({"island_trader": { "item": 298, "amount": int(amount)}})
    elif "Ginger Island Resort" in source_text:
        amount = re.search(r'data-sort-value="(\d+)"', source_text).group(1)
        sources.append({"ginger_island_resort": int(amount)})

    return sources

def get_recipes():
    base_url = 'https://stardewvalleywiki.com/Cooking'
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    recipes = []

    table = soup.find("table")
    body = table.find("tbody")
    for recipe_tr in body.find_all("tr", recursive=False):
        recipe_tds = recipe_tr.find_all("td", recursive=False)
        if len(recipe_tds) >= 7:
            name = recipe_tds[1].text.strip()
            ingredients = get_ingredients(recipe_tds[3])
            recipe_source = get_recipe_source(recipe_tds[7])

            recipes.append((name, ingredients, recipe_source))

    return recipes

    
for recipe in get_recipes():
    if not recipe[1]:
        pprint.pprint(recipe)


def insert_items(cur):
    items = get_items()
    sql_string = "INSERT INTO items(item_name, seasons, sources) VALUES (%s, %s, %s);" 
    
    cur.executemany(sql_string, [item for item in items])