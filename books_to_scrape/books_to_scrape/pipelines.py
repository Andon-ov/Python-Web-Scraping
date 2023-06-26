# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import psycopg2

# class BooksToScrapePipeline:
#     def __init__(self):
#         ## Connection Details
#         hostname = 'localhost'
#         username = 'postgres'
#         password = 'mysecretpassword' # your password
#         database = 'books'

#         ## Create/Connect to database
#         self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

#         ## Create cursor, used to execute commands
#         self.cur = self.connection.cursor()

#         ## Create quotes table if none exists
#         self.cur.execute("""
#         CREATE TABLE IF NOT EXISTS quotes(
#             id serial PRIMARY KEY,
#             content text,
#             tags text,
#             author VARCHAR(255)
#         )
#         """)

#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)

#         # Strip all whitespaces from strings
#         field_names = adapter.field_names()
#         for field_name in field_names:
#             if field_name != 'description':
#                 value = adapter.get(field_name)
#                 adapter[field_name] = value.strip()

#         # Category & Product Type --> switch to lowercase
#         lowercase_keys = ['category', 'product_type']
#         for lowercase_key in lowercase_keys:
#             value = adapter.get(lowercase_key)
#             adapter[lowercase_key] = value.lower()

#         # Price keys --> remove pound sign and convert to float
#         price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
#         for price_key in price_keys:
#             value = adapter.get(price_key)
#             value = value.replace('£', '')
#             adapter[price_key] = float(value)

#         # Availability --> extract number of books in stock
#         availability_string = adapter.get('availability')
#         split_string_array = availability_string.split('(')
#         if len(split_string_array) < 2:
#             adapter['availability'] = 0
#         else:
#             availability_array = split_string_array[1].split(' ')
#             adapter['availability'] = int(availability_array[0])

#         # Reviews --> convert string to number
#         num_reviews_string = adapter.get('num_reviews')
#         adapter['num_reviews'] = int(num_reviews_string)

#         # Stars --> convert text to number
#         stars_string = adapter.get('stars')
#         split_stars_array = stars_string.split(' ')
#         stars_text_value = split_stars_array[1].lower()
#         if stars_text_value == "zero":
#             adapter['stars'] = 0
#         elif stars_text_value == "one":
#             adapter['stars'] = 1
#         elif stars_text_value == "two":
#             adapter['stars'] = 2
#         elif stars_text_value == "three":
#             adapter['stars'] = 3
#         elif stars_text_value == "four":
#             adapter['stars'] = 4
#         elif stars_text_value == "five":
#             adapter['stars'] = 5


#         return item



# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BooksToScrapePipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()


        ## Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()



        ## Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)


        ## Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])



        ## Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)


        ## Stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5


        return item




# class SaveToMySQLPipeline:

# pipelines.py

import psycopg2

class SaveToPostgresPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'mysecretpassword', #add your password here if you have one set 
        database = 'books'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into books (
            url, 
            title, 
            upc, 
            product_type, 
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
            str(item["description"][0])
        ))

        # ## Execute insert of data into database
        self.connection.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
