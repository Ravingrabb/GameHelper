import eel
import steamfront
import requests
from bs4 import BeautifulSoup
import webbrowser
eel.init('web')

client = steamfront.Client()


@eel.expose
def get_game_by_id(game_id):
    try:
        game = client.getApp(appid=game_id)
        rus = True if 'Russian' in game.supported_languages else False
        output = [game.appid, game.name, game.header_image, rus]
        return output if game.type == 'game' else 'game not found'
    except steamfront.errors.AppNotFound:
        return 'game not found'

@eel.expose
def get_games_list(input_text):
    if ' ' in input_text:
        input_text = input_text.replace(' ', '+')
    info = requests.get(f'https://steamcharts.com/search/?q={input_text}')
    soup = BeautifulSoup(info.content, 'html.parser')
    try:
        rows = soup.table.tbody.find_all('tr')
        data = []
        for row in rows:
            steam_id = row.find('a')['href'].replace('/app/', '')
            image_src = 'https://steamcharts.com' + row.find('img')['src']
            name = row.find('img')['alt']
            players_30 = row.find("td", {"class": "right num-f"}).get_text(strip=True)
            players_30 = players_30.replace(' ', '')
            data.append([steam_id, name, image_src, players_30])
        return data
    except:
        return 'not found'

@eel.expose
def open_browser(url):
    webbrowser.open(url, new=2)

        

eel.start('index.html', size=(500, 500))
