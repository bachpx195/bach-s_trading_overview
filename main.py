import streamlit as st
from apps.services.get_data_service import GetDataService
from apps.components.chart_overview_component import ChartOverviewComponent
from apps.helpers.datetime_helper import to_date, next_day, previous_day, to_str


MENU_LAYOUT = [1, 1, 1, 7, 2]
CONFIG = {'displayModeBar': False, 'responsive': False}

# Them *** voi cac ngay phu hop
# LIST_DATE = (
#     "2024-08-08",
#     "2023-10-12",
#     "2023-09-13",
#     "2023-08-10",
#     "2024-07-11",
#     "2024-06-12",
#     "2024-05-15",
# )

def run():
  st.set_page_config(layout="wide")
  st.write(
      '<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
  st.write(
      '<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
  
#   date_select = st.radio(
#       "Chọn ngày: ", LIST_DATE)
#   date_select = date_select.replace("*", "")
  

  date_select = st.date_input(label='Chọn ngày')


  START_DATE = previous_day(to_str(date_select))
  END_DATE = next_day(to_str(date_select))

  week_prices, day_prices, hour_prices = GetDataService(
      'LTCUSDT',100, START_DATE, END_DATE, None).run()
  btc_week_prices, btc_day_prices, btc_hour_prices = GetDataService(
      'BTCUSDT', 100, START_DATE, END_DATE, None).run()
  abtc_week_prices, abtc_day_prices, abtc_hour_prices = GetDataService(
      'LTCBTC', 100, START_DATE, END_DATE, None).run()

  for date in day_prices.day.to_list():
    if date == to_str(date_select):
      ChartOverviewComponent(
          week_prices,
          day_prices,
          hour_prices,
          date,
          True,
          btc_week_prices,
          btc_day_prices,
          btc_hour_prices,
          abtc_week_prices,
          abtc_day_prices,
          abtc_hour_prices,
      ).run()

if __name__ == "__main__":
    run()
