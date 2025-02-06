import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from apps.helpers.datetime_helper import get_list_day_of_week, get_start_of_week, to_date, previous_week, FORMAT_DATE_YEAR
from apps.helpers.constants import CHART_CONFIG, CHART_HEIGHT


class FullChartDailyComponent:
  def __init__(self, week_dataframe, dataframe):
    self.day_df = dataframe
    self.week_df = week_dataframe if week_dataframe else None
    
  def set_week_dataframe(self, week_dataframe, date):
    week_df = week_dataframe[week_dataframe.index.strftime(
        FORMAT_DATE_YEAR) == get_start_of_week(previous_week(date))]
    return week_df

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    df = self.day_df
    df.sort_index(inplace=True) 

    tickvals =[k*0.5 for k in range(len(df))]
    ticktext = list(
        (f"{date.to_pydatetime().strftime('%m-%d')} {round(df.loc[date].return_oc, 2)}" for date in df.index))

    fig = go.Figure(data=[go.Candlestick(x=tickvals,
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'], hovertext=list(
        (f"{date.to_pydatetime().strftime('%d')} {round(df.loc[date].return_oc, 2)}" for date in df.index)))])
    

    fig.add_vline(x=0.3, line_width=2, line_dash="dash", line_color="green")
    fig.add_vline(x=3.9, line_width=2, line_dash="dash", line_color="green")
    fig.update_xaxes(showticklabels=False)

    fig.update_layout(xaxis_rangeslider_visible=False, height=350, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), margin={"l":0,"r":0,"t":0,"b":0})

    st.plotly_chart(fig)
