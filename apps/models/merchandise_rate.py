import pandas as pd
from myenv.database.pymysql_conn import DataBase

db = DataBase()
INTERVAL_HASH = {"day": 1, "week": 2}
SQL = "SELECT * FROM DailyTradingJournal_development.merchandise_rates;"


class MerchandiseRate:
    def __init__(self):
        self.sql = SQL

    def to_df(self):
        db.cur.execute(self.sql)
        columns = ['date', 'open', 'high', 'close', 'low']
        datas = list(db.cur.fetchall())
        data = [(da[8], da[3], da[4], da[5], da[6])
                for da in datas]
        df = pd.DataFrame(columns=columns, data=data)
        df.set_index('date', inplace=True)
        return df

    def find_by_slug(self, slug):
        query_sql = f"SELECT  * FROM DailyTradingJournal_development.merchandise_rates WHERE merchandise_rates.slug = '{slug}' LIMIT 1"
        db.cur.execute(query_sql)
        datas = list(db.cur.fetchall())
        return datas[0][0]
