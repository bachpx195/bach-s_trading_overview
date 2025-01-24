import pandas as pd
from configs.database.pymysql_conn import DataBase
from apps.services.log_services import log

db = DataBase()
INTERVAL_HASH = {"day": 1, "week": 2, "month": 3, "hour": 4, "15m": 5}

class AnalyticMonth:
  def __init__(self, merchandise_rate_id, limit=None, sort="DESC", month=None):
    self.limit = limit if limit else 100000
    self.merchandise_rate_id = merchandise_rate_id
    self.sort = sort

    self.month = month

  def to_df(self):
    try:
      sql_query = 'SELECT * FROM DailyTradingJournal_development.analytic_months WHERE '
      if self.month:
          sql_query = sql_query + \
                  f"MONTH(analytic_months.date) = {self.month} AND "
      if self.merchandise_rate_id:
          sql_query = sql_query + \
              f"analytic_months.merchandise_rate_id = {self.merchandise_rate_id} "
      if self.sort:
          sql_query = sql_query + f"ORDER BY analytic_months.year {self.sort}, analytic_months.month {self.sort} "
      if self.limit:
          sql_query = sql_query + f"lIMIT {self.limit}"
      sql_query = sql_query + ';'

      log(sql_query)

      db.cur.execute(sql_query)
      
      columns = ['month', 'year', 'candlestick_type', 'return_oc', 'return_hl']
      datas = list(db.cur.fetchall())
      data = [(da[3], da[4], da[5], da[7], da[8])
              for da in datas]
      df = pd.DataFrame(columns=columns, data=data)
      return df
    except Exception as e:
      log(str(e), 'Exception')
