import streamlit as st
from hydralit_custom import HydraHeadApp
from apps.components.raw_data import RawData
from apps.services.get_data_service import GetDataService
from apps.components.search_option import SearchOption
from apps.components.chart_overview_component import ChartOverviewComponent

MENU_LAYOUT = [1,1,1,7,2]
CONFIG = {'displayModeBar': False, 'responsive': False}

class HomeApp(HydraHeadApp):
   def __init__(self, title = 'Hydralit Explorer', **kwargs):
      self.__dict__.update(kwargs)
      self.title = title

   def run(self):
      st.write('HI, IM A TRADER!')

      merchandise_rate, record_limit, start_date, end_date, list_day = SearchOption().run()
      day_prices, hour_prices = GetDataService(
         merchandise_rate, record_limit, start_date, end_date, list_day).run()

      RawData(day_prices, "Hiển thị data ngày").run()
      RawData(hour_prices, "Hiển thị data giờ").run()

      list_day = day_prices.day.to_list()

      for date in list_day:
        ChartOverviewComponent(day_prices, hour_prices, date).run()

