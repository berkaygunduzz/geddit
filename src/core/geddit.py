import requests
import base64
from cryptography.fernet import Fernet
import datetime


LATEST = 'new'
MOST_LIKED = 'top'
POPULAR = 'hot'


# Login Reddit account, returns headers dict
def login(username: str, password: str, cli_id: str = None, secret: str = None, encoding: str = 'utf-8') -> dict:

    # Encrypt/decrypt class, uses 'username + password' as key
    f = Fernet(base64.urlsafe_b64encode(
        (username + password).ljust(32)[:32].encode(encoding)))

    # Read/write authorization file
    # If authorization file is set, decrypt from
    # Else create encrpyted authorization file
    try:
        # Decrypt authorization tokens from authorization file
        with open('.geddit', 'rb+') as auth_f:
            data = auth_f.read()
            cli_id_encrypted = data[:120]
            secret_encrypted = data[120:]
            cli_id = f.decrypt(cli_id_encrypted.decode(encoding))
            secret = f.decrypt(secret_encrypted.decode(encoding))
    except FileNotFoundError:
        # Encrypt authorization tokens to authorization file
        if not cli_id or not secret:
            raise ValueError('No cli_id or secret token specified')
        cli_id_encrypted = f.encrypt(cli_id.encode(encoding))
        secret_encrypted = f.encrypt(secret.encode(encoding))
        with open('.geddit', 'wb+') as auth_f:
            auth_f.writelines((cli_id_encrypted, secret_encrypted))

    # Authorization request
    auth = requests.auth.HTTPBasicAuth(cli_id, secret)

    # Login method specifications
    data = {'grant_type': 'password',
            'username': username,
            'password': password}

    # Header info file
    headers = {'User-Agent': 'geddit'}

    # Access token
    TOKEN = requests.post('https://www.reddit.com/api/v1/access_token',
                          auth=auth, data=data, headers=headers).json()['access_token']

    # Create full header to acces by login
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    return headers


# Get posts
def get(subreddit: str, type: str = LATEST, limit: int = 10, headers: dict = None) -> dict:

    # URL to make request
    request_url = f"https://oauth.reddit.com/r/{subreddit}/{type}.json?limit={limit}"
    if not headers:
        request_url = f"https://www.reddit.com/r/{subreddit}/{type}.json?limit={limit}"

    # Make request
    result_raw = requests.get(url=request_url, headers=headers)

    # Posts containing
    results = list()

    # Scrap important data
    for post in result_raw.json()['data']['children']:
        results.append({
            'subreddit': subreddit,
            'title': post['data']['title'],
            'author': post['data']['author'],
            'subtext': post['data']['selftext'],
            'permalink': post['data']['permalink'],
            'url': post['data']['url'],
            'created': post['data']['created'],
        })

    return results


# Add Subreddit name to listen
def add_subreddit(subreddit: str) -> None:
    if subreddit in get_subreddit_list():
        return
    try:
        with open('.gedditlisten', 'a+') as sub_list_f:
            sub_list_f.write(subreddit + '\n')
    except FileNotFoundError:
        with open('.gedditlisten', 'w+') as sub_list_f:
            sub_list_f.write(subreddit + '\n')


# Get list of listening Subreddits
def get_subreddit_list() -> list:
    sub_list = list()
    try:
        with open('.gedditlisten', 'r+') as sub_list_f:
            sub_list = sub_list_f.read().split('\n')[:-1]
    except FileNotFoundError:
        sub_list = []
    return sub_list

