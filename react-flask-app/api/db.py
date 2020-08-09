import mariadb

def connect_db():
    return mariadb.connect(
            user='root', 
            password='watermelonpeachmelon',
            host='34.70.46.63',
            database='tweet_data'
    )
