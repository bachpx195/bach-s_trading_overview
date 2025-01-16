import streamlit as st
from apps.services.custom.get_month_data_service import GetMonthDataService
from apps.components.chart_overview_component import ChartOverviewComponent
from apps.helpers.datetime_helper import to_date, next_day, previous_day, to_str
from apps.helpers.constants import LIST_MONTH, LIST_MERCHANDISE

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
  month = st.radio(
          "Chọn tháng: ", LIST_MONTH, index=1, horizontal=True)

  try:
    month_prices = GetMonthDataService(
      f"{merchandise}USDT", month).run()
    st.bar_chart(month_prices, x="year", y=["return_oc", "return_hl"])
    # btc_week_prices, btc_day_prices, btc_hour_prices = GetDataService(
    #   'BTCUSDT', 1000, START_DATE, END_DATE, None).run()
    other_price_data = None
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
  except IndexError:
    st.write(
      f"Ngay chua co data.")

if __name__ == "__main__":
    run()
