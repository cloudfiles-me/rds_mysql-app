'''Importing all modules we need'''
import time, mysql.connector
from mysql.connector import errorcode

INSERT_STMT = "INSERT INTO failover_test (test_name, failover_date) VALUES (%s, %s)"

# CONFIG = {
#     'user': 'username',
#     'password': 'pass',
#     'host': 'server',
#     'database': 'db',
# }

CONFIG = {
    'raise_on_warnings': True,
    'connection_timeout': 5,
    'failover': [{
        'user': 'username',
        'password': 'pass',
        'host': 'server',
        'port': 3306,
        'database': 'db',
        }, {
            'user': 'user',
            'password': 'pass',
            'host': 'server',
            'port': 3306,
            'database': 'db',
        }]
}

SEC = 0
while True:
    try:
        CNX = mysql.connector.connect(**CONFIG)
        CURSOR = CNX.cursor()
        print("Connection OK")
        try:
            INSERT_DATA = ("jorge", time.strftime('%Y-%m-%d %H:%M:%S'))
            CURSOR.execute(INSERT_STMT, INSERT_DATA)
            # You can use CNX.autocommit = True
            CNX.commit()
            SEC += 1
            print("Data inserted :: Secuence:: " + str(SEC))
            CURSOR.close()
            CNX.close()
            time.sleep(1)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            print("Closing Connection")
            CNX.close()
