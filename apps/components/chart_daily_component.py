import streamlit as st
import plotly.graph_objects as go
from apps.helpers.datetime_helper import get_list_day_of_week, get_start_of_week, to_date, FORMAT_DATE_YEAR
from apps.helpers.constants import CHART_CONFIG


class ChartDailyComponent:
  def __init__(self, week_dataframe, dataframe, date):
    list_day_of_week = get_list_day_of_week(to_date(date))
    print(list_day_of_week)
    self.df = dataframe[dataframe['day'].isin(
        list_day_of_week)].sort_index()
    self.week_df = week_dataframe[week_dataframe.index.strftime(
        FORMAT_DATE_YEAR) == get_start_of_week(to_date(date))]

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    ticktext = list(
        (f"{date.to_pydatetime().strftime('%m-%d')} {round(self.df.loc[date].return_oc, 2)}" for date in self.df.index))

    candlestick_data = go.Candlestick(
      x=ticktext,
      open=self.df['open'].tolist(),
      high=self.df['high'].tolist(),
      low=self.df['low'].tolist(),
      close=self.df['close'].tolist(),
      hovertext=self.df['return_oc']
    )

    fig = go.Figure()
    fig.add_trace(candlestick_data)

    fig.update_layout(xaxis_rangeslider_visible=False, xaxis_ticktext=ticktext, xaxis=dict(
        showgrid=False), yaxis=dict(showgrid=False))

    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
