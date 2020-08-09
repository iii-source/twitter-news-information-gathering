import yaml

LOGGING_PATH = '../common/log/logger.log'
LOGGING_PATH_CURRENT = '../log/logger.log'
API_DOCUMENTS = 'https://iii-source.github.io/public/swagger_ui/tweet_news/docs/dist/'

with open('../common/db/sql/sql.yaml', 'r') as read_yml:
    sql_yaml = yaml.load(read_yml, Loader=yaml.SafeLoader)
