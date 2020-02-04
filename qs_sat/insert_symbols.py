"""
sudo apt-get install libmysqlclient-dev
pip install mysqlclient # Take the place of MySQLdb below since it does not support Python3
pip install requests
pip install beautifulsoup4
"""
import datetime
from math import ceil
import bs4
import MySQLdb as mdb
import requests


def obtain_parse_wiki_snp500():
    """ Download and parse the Wikipedia list of S&P500 constituents using requests and BeautifulSoup.
    Returns a list of tuples for to add to MySQL.
    """
    # Stores the current time, for the created_at record 
    now = datetime.datetime.utcnow()
    # Use requests and BeautifulSoup to download the list of S&P500 companies and obtain the symbol table 
    response = requests.get( "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs4.BeautifulSoup(response.text)
    # This selects the first table, using CSS Selector syntax and then ignores the header row ([1:])
    symbolslist = soup.select('table')[0].select('tr')[1:]
    # Obtain the symbol information for each row in the S&P500 constituent table
    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(
            (
            tds[0].select('a')[0].text, # Ticker 
            'stock', 
            tds[1].select('a')[0].text, # Name
            tds[3].text, # Sector
            'USD', now, now
            ))
    return symbols

def insert_snp500_symbols(symbols):
    """
    Insert the S&P500 symbols into the MySQL database.
    """
    # Connect to the MySQL instance
    db_host = 'localhost'
    db_user = 'sec_user'
    db_pass = 'Your_Password_Here'
    db_name = 'securities_master'
    con = mdb.connect( host=db_host, user=db_user, passwd=db_pass, db=db_name)
    # Create the insert strings
    column_str = ( "name, instrument, ticker, sector, "
        "currency, created_date, last_updated_date")
    insert_str = ("%s, " * 7)[:-2]
    final_str = "INSERT INTO symbol (%s) VALUES (%s)" % (column_str, insert_str)
    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    cur = con.cursor()
    cur.executemany(final_str, symbols)
    con.commit()


if __name__ == '__main__':
    symbols = obtain_parse_wiki_snp500()
    insert_snp500_symbols(symbols)
    print('%s symbols were successfully added.' % len(symbols))
