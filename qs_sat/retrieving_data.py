import pandas as pd
import MySQLdb as mdb

if __name__ == "__main__":
    # Connect to the MySQL instance
    DB_HOST = 'localhost'
    DB_USER = 'sec_user'
    DB_PASS = 'Your_Password'
    DB_NAME = 'securities_master'
    con = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    
    sql = """
        SELECT dp.price_date, dp.close_price, dp.adj_factor 
        FROM symbol AS sym 
        INNER JOIN daily_price AS dp 
        ON dp.symbol_id = sym.id 
        WHERE sym.ticker = '601988' 
        ORDER BY dp.price_date ASC;
        """
    sql2 = """
        SELECT sy.ticker, dl.price_date, dl.close_price, dl.adj_factor, dl.volume 
        FROM daily_price AS dl 
        INNER JOIN symbol as sy 
        ON dl.symbol_id = sy.id 
        WHERE sy.ticker='601988' 
        ORDER BY dl.price_date DESC;
        """

    # Create a pandas dataframe from the SQL query
    ZGYH = pd.read_sql_query(sql2, con=con, index_col='price_date')
    # Output the dataframe tail
    print(ZGYH.tail())

    
    
