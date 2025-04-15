import configparser
import os

from aiohttp.hdrs import USER_AGENT

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

SECRET = parser.get('api_keys', 'reddit_secret_key')
CLIENT_ID = parser.get('api_keys', 'reddit_client_id')
USER_AGENT=parser.get("api_keys",'user_agent')


DATABASE_HOST =  parser.get('database', 'database_host')
DATABASE_NAME =  parser.get('database', 'database_name')
DATABASE_PORT =  parser.get('database', 'database_port')
DATABASE_USER =  parser.get('database', 'database_username')
DATABASE_PASSWORD =  parser.get('database', 'database_password')

ACCOUNT_NAME=parser.get('azure', 'ACCOUNT_NAME')
FILE_SYSTEM_NAME=parser.get('azure', 'FILE_SYSTEM_NAME')
ACCOUNT_KEY=parser.get('azure', 'ACCOUNT_KEY')
ACCOUNT_URL=parser.get('azure', 'ACCOUNT_URL')

INPUT_PATH = parser.get('file_paths', 'input_path')
OUTPUT_PATH = parser.get('file_paths', 'output_path')

POST_FIELDS = (
    'id',
    'subreddit',
    'title',
    'score',
    'num_comments',
    'author',
    'created_utc',
    'upvote_ratio'
)