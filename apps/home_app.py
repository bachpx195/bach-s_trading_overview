import streamlit as st
from hydralit_custom import HydraHeadApp
from apps.components.raw_data import RawData
from apps.services.get_data_service import GetDataService
from apps.components.search_option import SearchOption
from apps.components.chart_overview_component import ChartOverviewComponent
from apps.helpers.datetime_helper import date_name

MENU_LAYOUT = [1,1,1,7,2]
CONFIG = {'displayModeBar': False, 'responsive': False}

class HomeApp(HydraHeadApp):
   def __init__(self, title = 'Hydralit Explorer', **kwargs):
      self.__dict__.update(kwargs)
      self.title = title

   def run(self):
      st.write('HI, IM A TRADER!')

      # merchandise_rate, record_limit, start_date, end_date, list_day, weekday, diff_with_btc = SearchOption().run()

      # abtc_week_prices, abtc_day_prices, abtc_hour_prices = GetDataService(
      #    'LTCBTC', record_limit, start_date, end_date, list_day).run()
      
      # RawData(abtc_week_prices, "Hiển thị data abtc tuần").run()
      # RawData(abtc_day_prices, "Hiển thị data abtc ngày").run()
      # RawData(abtc_hour_prices, "Hiển thị data abtc giờ").run()

      merchandise_rate, record_limit, start_date, end_date, list_day, weekday, diff_with_btc = SearchOption().run()
      week_prices, day_prices, hour_prices = GetDataService(
         merchandise_rate, record_limit, start_date, end_date, list_day).run()
      
      if diff_with_btc:
         btc_week_prices, btc_day_prices, btc_hour_prices = GetDataService(
            'BTCUSDT', record_limit, start_date, end_date, list_day).run()
         abtc_week_prices, abtc_day_prices, abtc_hour_prices = GetDataService(
             'LTCBTC', record_limit, start_date, end_date, list_day).run()
      else:
         btc_week_prices = None
         btc_day_prices = None
         btc_hour_prices = None
         abtc_week_prices = None
         abtc_day_prices = None
         abtc_hour_prices = None
         

      # RawData(week_prices, "Hiển thị data tuần").run()
      # RawData(day_prices, "Hiển thị data ngày").run()
      # RawData(hour_prices, "Hiển thị data giờ").run()
      # RawData(btc_week_prices, "Hiển thị data btc tuần").run()
      # RawData(btc_day_prices, "Hiển thị data btc ngày").run()
      # RawData(btc_hour_prices, "Hiển thị data btc giờ").run()
      # RawData(abtc_week_prices, "Hiển thị data abtc tuần").run()
      # RawData(abtc_day_prices, "Hiển thị data abtc ngày").run()
      # RawData(abtc_hour_prices, "Hiển thị data abtc giờ").run()
      
      if list_day is None:
         list_day = day_prices.day.to_list()

      for date in day_prices.day.to_list():
         if list_day and str(date) not in list_day:
            continue
         
         if date_name(date) not in weekday:
            continue

         ChartOverviewComponent(
            week_prices, 
            day_prices, 
            hour_prices,
            date,
            diff_with_btc,
            btc_week_prices,
            btc_day_prices, 
            btc_hour_prices, 
            abtc_week_prices,
            abtc_day_prices,
            abtc_hour_prices,
         ).run()

