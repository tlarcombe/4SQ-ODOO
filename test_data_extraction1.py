import xmlrpc.client
import pandas as pd
from sqlalchemy import create_engine
import schedule
import time

def connect_to_odoo(url, db, username, password):
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    return uid, models

def extract_data(models, db, uid, password, model, fields):
    data = models.execute_kw(db, uid, password, model, 'search_read', [[]], {'fields': fields})
    return pd.DataFrame(data)

def store_data(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists='replace', index=False)

def main():
    # Odoo connection details
    url = 'https://coach1st.odoo.com/odoo'
    db = 'coach1st'
    username = 't*******combe'
    password = '*************'

    # Local database details
    local_db_url = 'sqlite:///odoo_data.db'  # Using SQLite for simplicity - move to the lab LAMP stack eventually

    uid, models = connect_to_odoo(url, db, username, password)
    engine = create_engine(local_db_url)

    # Define data to extract
    extraction_config = [
        {'model': 'sale.order', 'fields': ['name', 'date_order', 'partner_id', 'amount_total'], 'table': 'sales'},
        {'model': 'res.partner', 'fields': ['name', 'email', 'phone'], 'table': 'customers'},
        {'model': 'product.product', 'fields': ['name', 'list_price', 'qty_available'], 'table': 'products'},
        {'model': 'mrp.production', 'fields': ['name', 'date_planned_start', 'product_id', 'product_qty'], 'table': 'production_orders'},
    ]

    for config in extraction_config:
        df = extract_data(models, db, uid, password, config['model'], config['fields'])
        store_data(df, config['table'], engine)

    print("Data extraction and storage complete.")

if __name__ == "__main__":
    schedule.every().day.at("01:00").do(main)  # Run daily at 1 AM

    while True:
        schedule.run_pending()
        time.sleep(60)
