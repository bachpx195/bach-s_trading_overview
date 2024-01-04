import streamlit as st
from apps.helpers.datetime_helper import date_with_name
from apps.components.chart_daily_component import ChartDailyComponent


class ChartOverviewComponent:
  def __init__(self, day_prices, hour_prices, date):
    self.date = date
    self.day_prices = day_prices
    self.hour_prices = hour_prices

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    st.write(date_with_name(self.date))

    ChartDailyComponent(self.day_prices, self.date).run()
    

    
