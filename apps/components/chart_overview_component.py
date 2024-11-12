import streamlit as st
import plotly.graph_objects as go
from apps.helpers.datetime_helper import date_with_name
from apps.components.chart_daily_component import ChartDailyComponent
from apps.components.chart_hour_component import ChartHourComponent


class ChartOverviewComponent:
  def __init__(self, merchandise, week_prices, day_prices, hour_prices, date, diff_with_btc, btc_week_prices=None, btc_day_prices=None, btc_hour_prices=None, show_other_merchandise=False, other_price_data=None):
    self.merchandise = merchandise
    self.date = date
    self.week_prices = week_prices
    self.day_prices = day_prices
    self.hour_prices = hour_prices
    self.diff_with_btc = diff_with_btc
    self.btc_week_prices = btc_week_prices
    self.btc_day_prices = btc_day_prices
    self.btc_hour_prices = btc_hour_prices
    self.show_other_merchandise = show_other_merchandise
    self.other_price_data = other_price_data

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    st.write(self.chart_title())

    self.render_chart("BTC", self.btc_week_prices,
                      self.btc_day_prices, self.btc_hour_prices)
    
    self.render_chart(self.merchandise, self.week_prices,
                      self.day_prices, self.hour_prices)

    if self.show_other_merchandise:
      for key in self.other_price_data.keys():
        price_data = self.other_price_data[key]
        self.render_chart(key, price_data['week_prices'],
                          price_data['day_prices'], price_data['hour_prices'])

    st.write('_________________________________________________')

    # chart_hour_object.show_detail_chart()

  def chart_title(self):
    return f"{date_with_name(self.date)}"
  
  def render_chart(self, merchandise, week_prices, day_prices, hour_prices):
    chart_container = st.container()
    with chart_container:
      chart_container.write(merchandise)
      c1, c2 = chart_container.columns([1, 3])
      chart_hour_object = ChartHourComponent(hour_prices, day_prices, self.date)
      with c1:
        ChartDailyComponent(week_prices, day_prices, self.date).run()
      with c2:
        chart_hour_object.run()

    return chart_hour_object

