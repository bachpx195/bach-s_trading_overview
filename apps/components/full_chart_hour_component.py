import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from apps.helpers.datetime_helper import previous_day
from apps.helpers.constants import CHART_CONFIG, CHART_HEIGHT

V_LINE_DISTANCE = 4.6

class FullChartHourComponent:
  def __init__(self, hour_prices, day_prices):
    self.hour_prices = hour_prices
    self.day_prices = day_prices

  def set_day_dataframe(self, day_prices, date):
    day_ohlc = day_prices[(
        day_prices['day'] == previous_day(date))]

    return day_ohlc
  
  def set_hour_dataframe(self, hour_prices, date):
    return hour_prices[hour_prices['date_with_binane'] == pd.to_datetime(date).date()]

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    df = self.hour_prices
    df.sort_index(inplace=True) 

    tickvals =[k*0.5 for k in range(len(df))]
    ticktext = list(
        (f"{date.to_pydatetime().strftime('%Hh')} {round(df.loc[date].return_oc, 2)}" for date in df.index))

    fig = go.Figure(data=[go.Candlestick(x=tickvals,
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'], hovertext=list(
        (f"{date.to_pydatetime().strftime('%m-%d %Hh')} {round(df.loc[date].return_oc, 2)}" for date in df.index)))])
        
    v_line_location = 3.8
    for _ in range(self.day_prices['low'].size):
      fig.add_vline(x=v_line_location, line_width=2, line_dash="dash", line_color="green")
      v_line_location = v_line_location + 4.55
      fig.add_vline(x=v_line_location, line_width=2, line_dash="dash", line_color="yellow")
      v_line_location = v_line_location + 3.45
      fig.add_vline(x=v_line_location, line_width=2, line_dash="dash", line_color="red")
      v_line_location = v_line_location + 3.9
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(xaxis_rangeslider_visible=False, height=350, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, width=2000)

  def show_detail_chart(self):
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    df = self.hour_prices
    df = df.iloc[::-1]

    tickvals = [k*0.5 for k in range(len(df))]
    ticktext = list(
        (f"{date.to_pydatetime().strftime('%m-%d %Hh')}" for date in df.index))

    fig = go.Figure(data=[go.Candlestick(x=tickvals,
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'], hovertext=df['return_oc'])])

    fig.add_vline(x=3.7, line_width=2, line_dash="dash", line_color="green")
    fig.add_vline(x=8.2, line_width=2, line_dash="dash", line_color="green")
    fig.update_layout(xaxis_rangeslider_visible=False, height=CHART_HEIGHT, xaxis_tickvals=tickvals,
                      xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
