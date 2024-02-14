# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
import psycopg2
import time

import logging
logging.basicConfig(level=logging.DEBUG)

# database created using docker compose up
db_params = {
        'user': 'docker',
        'password': 'docker',
        'host': 'database',
        'port': '5432',
        'database': 'exampledb',
    }

# separate database (used for local testing)
# db_params = {
#         "user" : "myuser",
#         "password" : "mypassword",
#         "host" : "localhost",
#         "port" : "5432",
#         "database" : "mydatabase"
# }

class SeleniumScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        return item

class SavingToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()
    def create_connection(self):
        attempts = 0
        while attempts < 60:
            try:
                self.connection = psycopg2.connect(**db_params)
                self.cur = self.connection.cursor()
                logging.debug("Connected successfully!")
                self.create_table()
                logging.debug("Table created successfully!")
                break
            except psycopg2.Error as e:
                logging.error(f"Attempt number {attempts} failed.")
                logging.error(f"Unable to connect to the database. Error: {e}")
                attempts += 1
                time.sleep(0.5)
        else:
            logging.error(f"Maximum number of attempts exceeded")
    def create_table(self):
        self.cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'sreality')")
        table_exists = self.cur.fetchone()[0]
        if not table_exists:
            self.cur.execute("CREATE TABLE sreality(sreality_number int NOT NULL, sreality_title text, sreality_url text)")
            self.connection.commit()
        else:
            self.cur.execute("TRUNCATE TABLE sreality")
            self.connection.commit()
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    def store_db(self, item):
        try:
            self.cur.execute(""" INSERT INTO sreality(
                        sreality_number,
                        sreality_title,
                        sreality_url
                        ) values (
                            %s,
                            %s,
                            %s
                            )""", (
                item["number"],
                item["title"],
                item["imgurl"]
            ))
        except BaseException as e:
            logging.debug("Exception in storing into the db: ", e)

        self.connection.commit()
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
