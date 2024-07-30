from urllib import parse

sql = "postgresql"
main = {
    "id": 2,
    "name": 'Main',
    "dev_profile": "Python"
}
user = "main"
password = parse.quote_plus('Taste81')
host = "localhost"
port = "5432"
dbName = "Project Main"
