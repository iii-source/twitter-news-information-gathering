import yaml

with open('../common/db/sql/sql_id.yaml', 'r') as read_yml:
    sql_id_yaml = yaml.load(read_yml, Loader=yaml.SafeLoader)
