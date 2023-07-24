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
    allowed_origins = ['http://localhost:3000', 'https://hello-games.vercel.app/']
    origin = event['headers'].get('origin') if 'headers' in event and 'origin' in event['headers'] else 'unknown'
    if origin in allowed_origins:
        cors_origin = origin
    else:
        cors_origin = allowed_origins[0]
    response = {
        "statusCode": 200,
        "body": json.dumps(games_data),
        "headers": {
            'Access-Control-Allow-Origin': cors_origin,
            'Access-Control-Allow-Credentials': True,
        }
    }
    return response
