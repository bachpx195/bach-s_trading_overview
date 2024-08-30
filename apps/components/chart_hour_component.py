import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from apps.helpers.datetime_helper import previous_day
from apps.helpers.constants import CHART_CONFIG, CHART_HEIGHT
from apps.helpers.draw_chart import draw_candlestick

class ChartHourComponent:
  def __init__(self, hour_prices, day_prices, date):
    self.hour_prices = self.set_hour_dataframe(hour_prices, date)
    self.day_prices = self.set_day_dataframe(day_prices, date)
    self.date = date

  def set_day_dataframe(self, day_prices, date):
    day_ohlc = day_prices[(
        day_prices['day'] == previous_day(date))]

    return day_ohlc
  
  def set_hour_dataframe(self, hour_prices, date):
    return hour_prices[hour_prices['date_with_binane'] == pd.to_datetime(date).date()]

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    df = pd.concat([self.day_prices, self.hour_prices])
    df.sort_index(inplace=True) 

    tickvals =[k*0.5 for k in range(len(df))]
    ticktext = list(
        (f"{date.to_pydatetime().strftime('%Hh')} {round(df.loc[date].return_oc, 2)}" for date in df.index))

    fig = go.Figure(data=[go.Candlestick(x=tickvals,
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'], hovertext=df['return_oc'])])
        
    if self.day_prices['low'].size != 0 and self.day_prices['high'].size != 0 and self.day_prices['close'].size != 0:
      fig.add_hline(y=self.day_prices['low'].values[0], line_width=1, line_color="pink")
      fig.add_hline(y=self.day_prices['high'].values[0], line_width=1, line_color="green")
      fig.add_hline(y=self.day_prices['close'].values[0], line_width=1, line_color="red")
      fig.add_vline(x=0.3, line_width=2, line_dash="dash", line_color="green")
      fig.add_vline(x=4.2, line_width=2, line_dash="dash", line_color="green")
      fig.add_vline(x=8.8, line_width=2, line_dash="dash", line_color="green")
      fig.update_layout(xaxis_rangeslider_visible=False, height=CHART_HEIGHT, xaxis_tickvals=tickvals,
                        xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

  def show_detail_chart(self):
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    df = self.hour_prices
    df = df.iloc[::-1]

    tickvals = [k*0.5 for k in range(len(df))]
    ticktext = list(
        (f"{date.to_pydatetime().strftime('%Hh')}" for date in df.index))

    fig = go.Figure(data=[go.Candlestick(x=tickvals,
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'], hovertext=df['return_oc'])])

    fig.add_vline(x=3.7, line_width=2, line_dash="dash", line_color="green")
    fig.add_vline(x=8.2, line_width=2, line_dash="dash", line_color="green")
    fig.update_layout(xaxis_rangeslider_visible=False, height=CHART_HEIGHT, xaxis_tickvals=tickvals,
                      xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
