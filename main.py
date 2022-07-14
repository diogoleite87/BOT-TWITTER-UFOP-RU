import requests
from bs4 import BeautifulSoup
import tweepy
import re
from datetime import date, datetime
import time

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

current_date = date.today()
current_day = current_date.strftime('%d')
current_date_gmt = current_date.strftime('%d/%m/%Y')

postAlmocoOPMA = False
postJantaOPMA = False
postAlmocoJM = False
postJantaJM = False

def subtraiDataCardapio(url):

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')

    dataCardapio = soup.find_all('span', style="font-size:22px;")
    dataCardapio = soup.find('strong')

    dataCardapioFormatado = dataCardapio.get_text().strip()

    return dataCardapioFormatado


def verificaCardapioAtualizado(dataCardapio, dataHoje):

    if dataCardapio == dataHoje:
        return True
    else:
        return False


def subtraiCardapio(url):

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')

    cardapio = soup.find_all('table')

    cardapioFormatado = []

    for i in range(len(cardapio)):
        cardapioFormatado.append(cardapio[i].get_text().strip())

    cardapioFormatado = cardapioFormatado
    return cardapioFormatado


def montaCardapiosFinal(cardapioFormatado) -> str:

    cardapioOPMA = ''.join(cardapioFormatado[0])
    cardapioJM = ''.join(cardapioFormatado[1])

    cardapioOPMA.strip()
    cardapioJM.strip()

    almocoOPMA = cardapioOPMA.replace('\n', '&')
    almocoOPMA = re.search('Almoço(.+?)Jantar', almocoOPMA).group(1)
    almocoOPMA = almocoOPMA.replace('&', '\n')
    almocoOPMA = 'Ouro Preto e Mariana - Almoço\nData: ' + current_date_gmt + almocoOPMA

    if len(almocoOPMA) > 280:
        aux = len(almocoOPMA) - 280
        almocoOPMA = almocoOPMA[:len(almocoOPMA) - aux]

    jantaOPMA = cardapioOPMA.replace('\n', '&')
    jantaOPMA = jantaOPMA + ' ◝(ᵔᵕᵔ)◜'
    jantaOPMA = re.search('Jantar(.+.)', jantaOPMA).group(1)
    jantaOPMA = jantaOPMA.replace('&', '\n')
    jantaOPMA = 'Ouro Preto e Mariana - Jantar\nData: ' + current_date_gmt + jantaOPMA

    if len(jantaOPMA) > 280:
        aux = len(jantaOPMA) - 280
        jantaOPMA = jantaOPMA[:len(jantaOPMA) - aux]

    almocoJM = cardapioJM.replace('\n', '&')
    almocoJM = re.search('Almoço(.+?)Jantar', almocoJM).group(1)
    almocoJM = almocoJM.replace('&', '\n')
    almocoJM = 'João Monlevade - Almoço\nData: ' + current_date_gmt + almocoJM

    if len(almocoJM) > 280:
        aux = len(almocoJM) - 280
        almocoJM = almocoJM[:len(almocoJM) - aux]

    jantaJM = cardapioJM.replace('\n', '&')
    jantaJM = jantaJM + ' ◝(ᵔᵕᵔ)◜'
    jantaJM = re.search('Jantar(.+.)', jantaJM).group(1)
    jantaJM = jantaJM.replace('&', '\n')
    jantaJM = 'João Monlevade - Jantar\nData: ' + current_date_gmt + jantaJM

    if len(jantaJM) > 280:
        aux = len(jantaJM) - 280
        jantaJM = jantaJM[:len(jantaJM) - aux]

    return almocoOPMA, jantaOPMA, almocoJM, jantaJM


def tweetar(api, tweet):
    try:
        api.update_status(tweet)
    except:
        print('Erro ao Tweetar')


def preTweet(almocoOPMA, jantaOPMA, almocoJM, jantaJM):
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret)

    api = tweepy.API(auth)

    if len(almocoOPMA) > 100:
        tweetar(api, almocoOPMA)
        postAlmocoOPMA = True
    else:
        print('Erro no cardapio Ouro Preto e Mariana - Almoço')

    if len(jantaOPMA) > 100:
        tweetar(api, jantaOPMA)
        postJantaOPMA = True
    else:
        print('Erro no cardapio Ouro Preto e Mariana - Jantar')

    if len(almocoJM) > 100:
        tweetar(api, almocoJM)
        postAlmocoJM = True
    else:
        print('Erro no cardapio João Monlevade - Almoço')

    if len(jantaJM) > 100:
        tweetar(api, jantaJM)
        postJantaJM = True
    else:
        print('Erro no cardapio João Monlevade - Jantar')


def main():

    url = 'https://ufop.br/cardapio-do-ru'

    dataCardapio = subtraiDataCardapio(url)

    if verificaCardapioAtualizado(int(dataCardapio), int(current_day)):

        horaAtual = datetime.today().strftime('%H')

        print("Cardapio atualizado, elaborando postagem...")
        cardapioFormatado = subtraiCardapio(url)

        almocoOPMA, jantaOPMA, almocoJM, jantaJM = montaCardapiosFinal(
            cardapioFormatado)

        preTweet(almocoOPMA, jantaOPMA, almocoJM, jantaJM)

        if ((postAlmocoOPMA == True) and (postJantaOPMA == True) and (postAlmocoJM == True) and (postJantaJM == True)):
            print("Cardapio atualizado com sucesso!")
        elif int(horaAtual) > 17:
            print("Horario de postagem expirou!")
        else:
            time.sleep(1800)
            main()

    else:

        horaAtual = datetime.today().strftime('%H')

        if int(horaAtual) > 17:
            print('Cardapio nao atualizado antes das 18:00hrs, postagem CANCELADA.')
        else:
            print(
                "Cardapio ainda nao foi atualizado, sera feita uma nova busca em 30 minutos...")
            time.sleep(1800)
            main()


main()
