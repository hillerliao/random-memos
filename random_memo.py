import sqlite3
import requests
from  config import *


db = f'{DB_PATH}/memos_prod.db'

def get_random_memo(db='', filter=FILTER): 
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Get the number of rows in the table
    c.execute('SELECT COUNT(*) FROM memo')
    count = c.fetchone()[0]

    # Select a random row
    q = 'SELECT * FROM memo ORDER BY RANDOM() LIMIT 1;'

    while True:
        c.execute(q)
        row = c.fetchone()

        # exclude memo cotaining certain characters.
        #if filter not in row[5]:
        if 'https://' in row[5]:
            msg = row[5]

            if len(msg) <= 500:
                msg = msg
            else:
                msg = msg[0:500] + '...'

            link = f'https://{DOMAIN}/m/{row[7]}'
            msg = msg  + ' ' + link
            break
    conn.close()
    return msg


def push_msg(channel='telegram'):
    channel= channel.lower()
    msg = get_random_memo(db, filter=FILTER)
    if channel== 'telegram':
        if not TG_BOT_TOKEN or not CHAT_ID:
            print('TG_BOT_TOKEN or CHAT_ID is not set.')
            return
        url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
        params = {'chat_id': CHAT_ID, 'text': msg}
        response = requests.post(url, params=params)
    elif channel == 'n8n':
        N8N_WEBHOOK_URL = N8N_WEBHOOK_URL.strip()
        if not N8N_WEBHOOK_URL:
            print('N8N_WEBHOOK_URL is not set.')
            return
        headers = {'token': N8N_WEBHOOK_TOKEN, 'Content-Type': 'application/json'}
        response = requests.post(N8N_WEBHOOK_URL, json={'content': msg}, headers=headers)
    if response.status_code == 200:
        print('Message sent.')
    else:
        print('Message sending failed.')

if __name__ == '__main__':
    push_msg(channel='n8n')
