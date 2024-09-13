import xmlrpc.client

url = 'http://localhost:8069'
db = 'your_database_name'
username = 'your_username'
password = 'your_password'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Read data from the 'res.partner' model
partners = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[['is_company', '=', True]]],
    {'fields': ['name', 'country_id', 'comment'], 'limit': 5})

for partner in partners:
    print(partner)
