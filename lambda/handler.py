import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os


def fetch_games():
    web_url = os.environ['WEB_URL']
    page = requests.get(web_url)
    htmls = page.text
    soup = BeautifulSoup(htmls, 'html.parser')
    jogos = soup.find_all('tr', {'class': 'live-subscription'})

    data = {
        "Hour": [],
        "Status": [],
        "Home": [],
        "Home Score": [],
        "Away Score": [],
        "Away": [],
    }

    for jogo in jogos:
        # Time processing
        time = jogo.find('td', {'class': 'hour'}).text.split(
            '\n\t\t\t\t')[-2].strip()
        dt_object = datetime.utcfromtimestamp(int(time))
        data["Hour"].append(dt_object.strftime("%H:%M"))

        # Status processing
        st = jogo.find('td', {'class': 'status'})
        a = st.find('a')
        span = st.find('span')
        txt = (a.text.strip() if a else '') or (
            span.text.strip() if span else '')
        data["Status"].append('Em breve' if txt == 'Previsão' or txt ==
                              '' else 'Iniciado' if txt.isdigit() else txt)

        # Home Team processing
        data["Home"].append(jogo.find('td', {'class': 'team-a'}).text.strip())

        # Away Team processing
        data["Away"].append(
            jogo.find('td', {'class': 'team-b'}).text.strip() or '')

        # Score processing
        score = jogo.find('td', {'class': 'score'})
        data["Home Score"].append(score.find(
            'span', {'class': 'fs_A'}).text.strip())
        data["Away Score"].append(score.find(
            'span', {'class': 'fs_B'}).text.strip())

    return data


def hello(event, context):
    games_data = fetch_games()
    response = {
        "statusCode": 200,
        "body": json.dumps(games_data),
        "headers": {
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': True,
        }
    }
    return response
