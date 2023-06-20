import requests
import base64
from cryptography.fernet import Fernet
from django.utils.timezone import make_aware
import datetime


# URL path perma's to request
LATEST = 'new'
MOST_LIKED = 'top'
POPULAR = 'hot'


"""
Login Reddit account

@param username: Reddit username
@param password: Reddit password
@param cli_id: Reddit API personal use script
@param secret: Reddit API secret token
@param encoding: Encoding to be used in files
@return: Headers to make requests
@raise ValueError: No cli_id, secret specified
"""
def login(username: str = None, password: str = None, cli_id: str = None, secret: str = None, encoding: str = 'utf-8') -> dict:

    # Add to environment list if not alreadt set
    try:
        with open('.env', 'r+') as env_f:
            if not username or not password:
                username = env_f.readline().strip()
                password = env_f.readline().strip()
    except FileNotFoundError:
        with open(".env", "w+") as env_f:
            env_f.write(username + "\n" + password)

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


"""
Get posts from subreddit

@param subreddit: Subreddit name
@param type: Type of request
@param limit: No of posts to get
@param header: Headers to authorize
@return: List of posts as dict
"""
def get(subreddit: str, type: str = LATEST, limit: int = 10, headers: dict = None) -> list:

    # URL to make request
    request_url = f"https://oauth.reddit.com/r/{subreddit}/{type}.json?limit={limit}"

    # Request without authorization if headers not set
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
            'URL': post['data']['url'],
            'created': make_aware(datetime.datetime.utcfromtimestamp(post['data']['created'])),
        })

    return results


"""
Add subreddit name to listening list

@param subreddit: Subreddit name
"""
def add_subreddit(subreddit: str) -> None:

    # Do nothing if already listening
    if subreddit in get_subreddit_list():
        return

    # If file is not already created, create one
    try:
        with open('.gedditlisten', 'a+') as sub_list_f:
            sub_list_f.write(subreddit + '\n')
    except FileNotFoundError:
        with open('.gedditlisten', 'w+') as sub_list_f:
            sub_list_f.write(subreddit + '\n')


"""
Get subreddit names in listening list

@return: List of subreddit names
"""
def get_subreddit_list() -> list:
    sub_list = list()

    # Return empty list if there is no list
    try:
        with open('.gedditlisten', 'r+') as sub_list_f:
            sub_list = sub_list_f.read().split('\n')[:-1]
    except FileNotFoundError:
        sub_list = []
    return sub_list

