import streamlit as st
from apps.services.get_data_service import GetDataService
from apps.components.chart_overview_component import ChartOverviewComponent
from apps.helpers.datetime_helper import to_date, next_day, previous_day, to_str

MENU_LAYOUT = [1, 1, 1, 7, 2]
CONFIG = {'displayModeBar': False, 'responsive': False}
MERCHANDISE = "DOT"
OTHER_MERCHANDISES = ["LTC"]
SHOW_OTHER_MERCHANDISES = False

def run():
  # layout_1()
  layout_2()


def layout_1():
  st.set_page_config(layout="wide")
  st.write(
      '<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
  st.write(
      '<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
  

  # Them *** voi cac ngay phu hop
  LIST_DATE = (
    "2024-11-04",
    "2024-11-05",
    "2024-11-06",
    "2024-11-07",
    "2024-11-08",
    "2024-11-09",
    "2024-11-10",
    "2024-11-11",
    "2024-11-12"
  )
#   date_select = st.radio(
#     "Chọn ngày: ", LIST_DATE)
#   date_select = date_select.replace("*", "")
  
  # date_select = st.date_input(label='Chọn ngày')

  START_DATE = LIST_DATE[0]
  END_DATE = LIST_DATE[-1]

  try:
    week_prices, day_prices, hour_prices = GetDataService(
      f"{MERCHANDISE}USDT", 1000, START_DATE, END_DATE, None).run()
    btc_week_prices, btc_day_prices, btc_hour_prices = GetDataService(
      'BTCUSDT', 1000, START_DATE, END_DATE, None).run()
    other_price_data = None
    if SHOW_OTHER_MERCHANDISES:
      other_price_data = {}
      for om in OTHER_MERCHANDISES:
        om_week_prices, om_day_prices, om_hour_prices = GetDataService(
            f"{om}USDT", 1000, START_DATE, END_DATE, None).run()
        other_price_data[om] = {
            'week_prices': om_week_prices,
            'day_prices': om_day_prices,
            'hour_prices': om_hour_prices
        }

    for date in day_prices.day.to_list():
        if to_str(date) in LIST_DATE:
            ChartOverviewComponent(
                MERCHANDISE,
                week_prices,
                day_prices,
                hour_prices,
                date,
                True,
                btc_week_prices,
                btc_day_prices,
                btc_hour_prices,
                SHOW_OTHER_MERCHANDISES,
                other_price_data
            ).run()
  except IndexError:
    st.write(
      f"Ngay chua co data.")

# Draw danh cac ngay theo khung thoi gian lon
def layout_2():
  from apps.components.full_chart_overview_component import FullChartOverviewComponent


  st.set_page_config(layout="wide")
  st.write(
      '<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
  st.write(
      '<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
  

  # Them *** voi cac ngay phu hop
  LIST_DATE = (
    "2024-11-04",
    "2024-11-05",
    "2024-11-06",
    "2024-11-07",
    "2024-11-08",
    "2024-11-09",
    "2024-11-10",
    "2024-11-11",
    "2024-11-12"
  )
  #   date_select = st.radio(
  #     "Chọn ngày: ", LIST_DATE)
  #   date_select = date_select.replace("*", "")
  
  # date_select = st.date_input(label='Chọn ngày')

  START_DATE = LIST_DATE[0]
  END_DATE = LIST_DATE[-1]

  try:
    week_prices, day_prices, hour_prices = GetDataService(
      f"{MERCHANDISE}USDT", 1000, START_DATE, END_DATE, None).run()
    btc_week_prices, btc_day_prices, btc_hour_prices = GetDataService(
      'BTCUSDT', 1000, START_DATE, END_DATE, None).run()
    other_price_data = None
    if SHOW_OTHER_MERCHANDISES:
      other_price_data = {}
      for om in OTHER_MERCHANDISES:
        om_week_prices, om_day_prices, om_hour_prices = GetDataService(
            f"{om}USDT", 1000, START_DATE, END_DATE, None).run()
        other_price_data[om] = {
            'week_prices': om_week_prices,
            'day_prices': om_day_prices,
            'hour_prices': om_hour_prices
        }


    FullChartOverviewComponent(
      MERCHANDISE,
      week_prices,
      day_prices,
      hour_prices,
      START_DATE,
      END_DATE,
      True,
      btc_week_prices,
      btc_day_prices,
      btc_hour_prices,
      SHOW_OTHER_MERCHANDISES,
      other_price_data
    ).run()
  except IndexError:
    st.write(
      f"Ngay chua co data.")

if __name__ == "__main__":
    run()
