import streamlit as st
import plotly.graph_objects as go
from apps.helpers.datetime_helper import previous_day
from apps.helpers.constants import CHART_CONFIG


class ChartDailyComponent:
  def __init__(self, dataframe, date):
    self.df = dataframe[(dataframe['day'] == date) | (dataframe['day'] == previous_day(
        date)) | (dataframe['day'] == previous_day(previous_day(date)))]

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    candlestick_data = go.Candlestick(
      x=self.df.index.tolist(),
      open=self.df['open'].tolist(),
      high=self.df['high'].tolist(),
      low=self.df['low'].tolist(),
      close=self.df['close'].tolist(),
      hovertext=self.df['return_oc']
    )

    fig = go.Figure()
    fig.add_trace(candlestick_data)

    fig.update_layout(xaxis_rangeslider_visible=False, xaxis=dict(
        showgrid=False), yaxis=dict(showgrid=False))

    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
