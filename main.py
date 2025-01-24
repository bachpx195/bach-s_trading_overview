import streamlit as st
import numpy as np
from apps.services.custom.get_month_data_service import GetMonthDataService
from apps.services.get_data_service import GetDataService
from apps.components.full_chart_month_component import FullChartMonthComponent
from apps.components.chart_week_component import ChartWeekComponent
from apps.components.custom.chart_month_daily_component import ChartMonthDailyComponent
from apps.helpers.datetime_helper import to_date, next_day, previous_day, to_str
from apps.helpers.constants import LIST_MONTH, LIST_MERCHANDISE
from apps.helpers.draw_chart import draw_month_return_heatmap
from apps.services.log_services import log

MENU_LAYOUT = [1, 1, 1, 7, 2]
CONFIG = {'displayModeBar': False, 'responsive': False}
MERCHANDISE = "LTC"
OTHER_MERCHANDISES = ["DOT"]
SHOW_OTHER_MERCHANDISES = False

def run():
  st.set_page_config(layout="wide")
  st.write(
      '<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
  st.write(
      '<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
 
  layout()
  

def layout():
  merchandise = st.radio(
          "Chọn coin: ", LIST_MERCHANDISE, index=1, horizontal=True)
  
  month_return = GetDataService(f"{merchandise}USDT",None, None,None, None).get_month_return()
    
  c1, c2 = st.columns([2, 2])
  with c1:
    st.pyplot(draw_month_return_heatmap(month_return, 'return_hl'))
  with c2:
    st.pyplot(draw_month_return_heatmap(month_return, 'return_oc'))
  
  month = st.radio(
          "Chọn tháng: ", LIST_MONTH, index=1, horizontal=True)

  try:
    month_prices, month_with_previous_month_prices, day_prices = GetMonthDataService(
      f"{merchandise}USDT", month).run()
    c1, c2 = st.columns([2, 2])
    with c1:
      st.bar_chart(month_prices, x="year", y=["return_oc"])
    with c2:
      st.bar_chart(month_prices, x="year", y=["return_hl"])
      
    week_prices = GetDataService(f"{merchandise}USDT",None, None,None, None, month).get_week_in_month_data()
    year_list = -np.sort(-np.unique(week_prices['year'].values))
    for year in year_list:
      st.write(year)
      if month == 2:
        month_in_year_prices = month_with_previous_month_prices[(month_with_previous_month_prices['year'] == year) & (month_with_previous_month_prices['month'] == month) | (month_with_previous_month_prices['year'] == year) & (month_with_previous_month_prices['month'] == 1) | (month_with_previous_month_prices['year'] == (year - 1)) & (month_with_previous_month_prices['month'] == 12)]
        previous_month_prices = month_in_year_prices[(month_in_year_prices['year'] == year) & (month_in_year_prices['month'] == (month -1))]
      elif month == 1:
        month_in_year_prices = month_with_previous_month_prices[(month_with_previous_month_prices['year'] == year) & (month_with_previous_month_prices['month'] == month) | (month_with_previous_month_prices['year'] == (year-1)) & (month_with_previous_month_prices['month'] == 11) | (month_with_previous_month_prices['year'] == (year - 1)) & (month_with_previous_month_prices['month'] == 12)]
        previous_month_prices = month_in_year_prices[(month_with_previous_month_prices['year'] == (year-1)) & (month_with_previous_month_prices['month'] == 12)]
      else:
        month_in_year_prices = month_with_previous_month_prices[(month_with_previous_month_prices['year'] == year) & (month_with_previous_month_prices['month'] == month)]
        previous_month_prices = month_in_year_prices[(month_in_year_prices['year'] == year) & (month_in_year_prices['month'] == (month -1))]
      week_in_month_prices = week_prices[(week_prices['year'] == year) & ((week_prices['month'] == month) | (week_prices['overlap_month'] == month))]
      day_in_month_prices = day_prices[day_prices.index.year == year]
      c1, c2 = st.columns([1, 2])
      with c1:
        FullChartMonthComponent(month_in_year_prices).run()
      with c2:
        ChartWeekComponent(previous_month_prices, week_in_month_prices).run()
        ChartMonthDailyComponent(previous_month_prices, day_in_month_prices).run()
    # btc_week_prices, btc_day_prices, btc_hour_prices = GetDataService(
    #   'BTCUSDT', 1000, START_DATE, END_DATE, None).run()
    # other_price_data = None
    # if SHOW_OTHER_MERCHANDISES:
    #   other_price_data = {}
    #   for om in OTHER_MERCHANDISES:
    #     om_week_prices, om_day_prices, om_hour_prices = GetDataService(
    #         f"{om}USDT", 1000, START_DATE, END_DATE, None).run()
    #     other_price_data[om] = {
    #         'week_prices': om_week_prices,
    #         'day_prices': om_day_prices,
    #         'hour_prices': om_hour_prices
    #     }

    # for date in day_prices.day.to_list():
    #     if to_str(date) in LIST_DATE:
    #         ChartOverviewComponent(
    #             MERCHANDISE,
    #             week_prices,
    #             day_prices,
    #             hour_prices,
    #             date,
    #             True,
    #             btc_week_prices,
    #             btc_day_prices,
    #             btc_hour_prices,
    #             SHOW_OTHER_MERCHANDISES,
    #             other_price_data
    #         ).run()
  except Exception as e:
    log(str(e), 'Exception')

if __name__ == "__main__":
    run()
