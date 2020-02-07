import pandas as pd
import MySQLdb as mdb

if __name__ == "__main__":
    # Connect to the MySQL instance
    DB_HOST = 'localhost'
    DB_USER = 'sec_user'
    DB_PASS = 'password'
    DB_NAME = 'securities_master'
    con = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    
    # Select all of the historic Google adjusted close data
    sql = "SELECT dp.price_date, dp.close_price, dp.adj_factor FROM symbol AS sym INNER JOIN daily_price AS dp ON dp.symbol_id = sym.id WHERE sym.ticker = '601988' ORDER BY dp.price_date ASC;"

    # Create a pandas dataframe from the SQL query
    ZGYH = pd.read_sql_query(sql, con=con, index_col='price_date')
    # Output the dataframe tail
    print(ZGYH.tail())
