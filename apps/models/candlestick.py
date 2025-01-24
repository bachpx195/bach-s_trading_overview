import pandas as pd
import pytz
from datetime import timezone
from configs.database.pymysql_conn import DataBase
from apps.services.log_services import log

db = DataBase()
INTERVAL_HASH = {"day": 1, "week": 2, "month": 3, "hour": 4, "15m": 5}

class Candlestick:
    def __init__(self, merchandise_rate_id, interval="day", limit=None, sort="ASC", start_date=None, end_date=None, list_day=None, month=None, context=None):
        self.limit = limit if limit else 100000
        self.interval = interval
        self.merchandise_rate_id = merchandise_rate_id
        self.sort = sort
        self.start_date = start_date
        self.end_date = end_date
        self.month = month
        self.context = context
        if interval == 'day':
            self.join_analytic_table = 'day_analytics'
        elif interval == 'hour':
            self.join_analytic_table = 'hour_analytics'
        elif interval == 'month':
            self.join_analytic_table = 'analytic_months'
        else:
            self.join_analytic_table = None
        
        if interval == 'week':
            self.join_master_table = 'week_masters'
        else:
            self.join_master_table = None
            
        self.list_day = list_day

    def to_df(self):
        if self.context:
            log(self.context, 'Context')
        try:
            if self.join_analytic_table:
                sql_query = f"SELECT * FROM DailyTradingJournal_development.candlesticks candlesticks INNER JOIN DailyTradingJournal_development.{self.join_analytic_table} ON candlesticks.id = {self.join_analytic_table}.candlestick_id WHERE "
            elif self.join_master_table:
                sql_query = f"SELECT * FROM DailyTradingJournal_development.candlesticks candlesticks INNER JOIN DailyTradingJournal_development.{self.join_master_table} ON candlesticks.date = {self.join_master_table}.start_date WHERE "
            else:
                sql_query = 'SELECT * FROM DailyTradingJournal_development.candlesticks WHERE '
                
            if self.start_date and self.end_date:
                sql_query = sql_query + \
                    f"(candlesticks.date BETWEEN '{self.start_date} 00:00:00' AND '{self.end_date} 23:23:59') AND "
            if self.list_day:
                if len(self.list_day) == 1:
                    sql_query = sql_query + \
                        f"(candlesticks.date BETWEEN '{self.list_day[0]} 00:00:00' AND '{self.list_day[0]} 23:23:59') AND "
                else:
                    for idx, day in enumerate(self.list_day):
                        if idx == len(self.list_day) - 1:
                            sql_query = sql_query + \
                                f"(candlesticks.date BETWEEN '{day} 00:00:00' AND '{day} 23:23:59')) AND "
                        elif idx == 0:
                            sql_query = sql_query + \
                                f"((candlesticks.date BETWEEN '{day} 00:00:00' AND '{day} 23:23:59') OR "
                        else:
                            sql_query = sql_query + \
                                f"(candlesticks.date BETWEEN '{day} 00:00:00' AND '{day} 23:23:59') OR "
            if self.month:
                if self.join_master_table:
                    sql_query = sql_query + \
                            f"(MONTH(candlesticks.date) = {self.month} OR week_masters.overlap_month = {self.month}) AND "
                else:
                    sql_query = sql_query + \
                            f"MONTH(candlesticks.date) IN ({self.month}) AND "
            if self.interval:
                sql_query = sql_query + \
                    f"candlesticks.time_type = {INTERVAL_HASH[self.interval]} AND "
            if self.merchandise_rate_id:
                sql_query = sql_query + \
                    f"candlesticks.merchandise_rate_id = {self.merchandise_rate_id} "
            if self.sort:
                sql_query = sql_query + f"ORDER BY candlesticks.date {self.sort} "
            if self.limit:
                sql_query = sql_query + f"lIMIT {self.limit}"
            sql_query = sql_query + ';'

            log(sql_query)

            db.cur.execute(sql_query)
            if self.join_analytic_table:
                if self.join_analytic_table == 'hour_analytics':
                    columns = ['date', 'open', 'high', 'close',
                            'low', 'volumn', 'date_database', 'date_with_binane', 'hour', 'return_oc', 'return_hl',
                            'candlestick_type', 'range_type', 'is_highest_hour_return', 'is_reverse_increase_hour', 'is_reverse_decrease_hour',
                            'is_same_btc', 'continue_by_day']
                    datas = list(db.cur.fetchall())
                    data = [(da[8], da[3], da[4], da[5], da[6], da[9], da[16], da[17], da[18], da[19], da[20], da[21], da[22], da[23], da[24], da[25], da[26], da[27])
                        for da in datas]
                if self.join_analytic_table == 'day_analytics':
                    columns = ['date', 'open', 'high', 'close',
                        'low', 'volumn', 'candlestick_type', 'range_type', 'is_inside_day', 'is_same_btc', 'continue_type']
                    datas = list(db.cur.fetchall())
                    data = [(da[8], da[3], da[4], da[5], da[6], da[9], da[18], da[19], da[20], da[26], da[27])
                            for da in datas]
                if self.join_analytic_table == 'analytic_months':
                    columns = ['date', 'open', 'high', 'close', 'low', 'volumn', 'month', 'year', 'return_oc', 'return_hl', 'candlestick_type']
                    datas = list(db.cur.fetchall())
                    data = [(da[8], da[3], da[4], da[5], da[6], da[9], da[16], da[17], da[20], da[21], da[18])
                            for da in datas]
            elif self.join_master_table:
                if self.join_master_table == 'week_masters':
                    columns = ['date', 'open', 'high', 'close', 'low', 'volumn', 'month', 'year', 'overlap_month', 'number_in_month']
                datas = list(db.cur.fetchall())
                data = [(da[8], da[3], da[4], da[5], da[6], da[9], da[15], da[16], da[17], da[18])
                        for da in datas]
            else:
                columns = ['date', 'open', 'high', 'close', 'low', 'volumn']
                datas = list(db.cur.fetchall())
                data = [(da[8], da[3], da[4], da[5], da[6], da[9])
                        for da in datas]
            df = pd.DataFrame(columns=columns, data=data)
            if not df['date'].empty:
                df['date'] = df['date'].dt.tz_localize(timezone.utc)
                my_timezone = pytz.timezone('Asia/Bangkok')
                df['date'] = df['date'].dt.tz_convert(my_timezone)
            else:
                log("**************data frame is null**************")
            df.set_index('date', inplace=True)
            return df
        except Exception as e:
            log(str(e), 'Exception')
