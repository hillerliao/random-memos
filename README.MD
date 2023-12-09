Send a Random Memo from Memos to Telegram

Applicable for  [memos](https://github.com/usememos/memos)  database using SQLite.

## Set Up Config File

Modify the `config.py` with your own secret things.

## Install Required Packages

`pip install -r requirements.txt`

## Set Up Scheduled Task

`* 7,11,17,21 * * * python  /path-of-the-script/random_memo.py`