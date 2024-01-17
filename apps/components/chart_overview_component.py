import streamlit as st
from apps.helpers.datetime_helper import date_with_name
from apps.components.chart_daily_component import ChartDailyComponent
from apps.components.chart_hour_component import ChartHourComponent


class ChartOverviewComponent:
  def __init__(self, week_prices, day_prices, hour_prices, date, diff_with_btc, btc_week_prices=None, btc_day_prices=None, btc_hour_prices=None):
    self.date = date
    self.week_prices = week_prices
    self.day_prices = day_prices
    self.hour_prices = hour_prices
    self.diff_with_btc = diff_with_btc
    self.btc_week_prices = btc_week_prices
    self.btc_day_prices = btc_day_prices
    self.btc_hour_prices = btc_hour_prices

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    st.write(date_with_name(self.date))
    c1, c2 = st.columns([1, 3])

    with c1:
      ChartDailyComponent(self.week_prices, self.day_prices, self.date).run()
    with c2:
      ChartHourComponent(self.hour_prices, self.day_prices, self.date).run()

    if self.diff_with_btc:
      with c1:
        ChartDailyComponent(
            self.btc_week_prices, self.btc_day_prices, self.date).run()
      with c2:
        ChartHourComponent(self.btc_hour_prices,
                          self.btc_day_prices, self.date).run()

    st.write('_________________________________________________')

