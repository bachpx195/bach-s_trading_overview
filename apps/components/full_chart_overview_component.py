import streamlit as st
import plotly.graph_objects as go
from apps.helpers.datetime_helper import date_with_name
from apps.components.full_chart_daily_component import FullChartDailyComponent
from apps.components.full_chart_hour_component import FullChartHourComponent


class FullChartOverviewComponent:
  def __init__(self, merchandise, week_prices, day_prices, hour_prices, start_date, end_date, diff_with_btc, btc_week_prices=None, btc_day_prices=None, btc_hour_prices=None, show_other_merchandise=False, other_price_data=None, layout=None):
    self.merchandise = merchandise
    self.start_date = start_date
    self.end_date = end_date
    self.week_prices = week_prices
    self.day_prices = day_prices
    self.hour_prices = hour_prices
    self.diff_with_btc = diff_with_btc
    self.btc_week_prices = btc_week_prices
    self.btc_day_prices = btc_day_prices
    self.btc_hour_prices = btc_hour_prices
    self.show_other_merchandise = show_other_merchandise
    self.other_price_data = other_price_data
    self.layout = layout

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    st.write(self.chart_title())

    if self.btc_week_prices:
      self.render_chart('hour', self.btc_day_prices, self.btc_hour_prices)
    
    self.render_chart('hour', self.day_prices, self.hour_prices)

    if self.btc_day_prices:
      self.render_chart('day', self.btc_day_prices, self.btc_hour_prices)
    
    self.render_chart('day', self.day_prices, self.hour_prices)

    # st.write('_________________________________________________')

    # chart_hour_object.show_detail_chart()

  def chart_title(self):
    return f"{date_with_name(self.start_date)} ~ {date_with_name(self.end_date)}"
  
  def render_chart(self, chart_type, day_prices, hour_prices):
    chart_container = st.container()
    with chart_container:
      # chart_container.write(merchandise)
      # c1, c2 = chart_container.columns([1, 3])
      chart_object = None
      if chart_type == 'hour':
        chart_object = FullChartHourComponent(hour_prices, day_prices)
        
      if chart_type == 'day':
        if self.layout == 3:
          chart_object = FullChartDailyComponent(None, day_prices)
        else:
          chart_object = FullChartDailyComponent(hour_prices, day_prices)
      chart_object.run()

    return chart_object

