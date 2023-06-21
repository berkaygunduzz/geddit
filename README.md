# geddit
A Python service to wrap Reddit posts

## Installation
- Clone repository
`git clone https://github.com/berkaygunduzz/geddit.git` and
`cd geddit`

- Build Docker image
`docker build -t geddit .`

- Run Docker image
`docker run -it -p 8000:8000 geddit`

- Open http://localhost:8000/api/register to register your credentials (only once)

- Now, you can use via make API calls

## How to use?
- After installation and registiration, to add Subreddit's to be listened with API call
`http://localhost:8000/api/add/<subreddit_name>`

- If you already added a Subreddit to be listened, you can get posts as
`http://localhost:8000/api/get` or
`http://localhost:8000/api/get/<subreddit_name>`

## How it works?
- `src/geddit/core/geddit.py` has methods to login, fetch posts and manage subreddit list
- Django command `./manage.py update_posts` updates database of the Django app with recent posts from the listed subreddits, in `src/geddit/api/management/commands/update_posts.py`
- `api` application helds API calls, database retrivals and register page
- Docker image updates database by calling `./manage.py update_posts` command every minute using `cron`