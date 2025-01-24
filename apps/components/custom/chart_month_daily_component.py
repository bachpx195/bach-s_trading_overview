import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from apps.helpers.constants import CHART_CONFIG, CHART_HEIGHT


class ChartMonthDailyComponent:
  def __init__(self, month_dataframe, dataframe):
    self.day_df = dataframe
    self.month_df = month_dataframe
    

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    df = pd.concat([self.month_df, self.day_df])
    df.sort_index(inplace=True) 

    tickvals =[k*0.5 for k in range(len(df))]
    ticktext = list(
        (f"{index.to_pydatetime().strftime('%m-%d')} {round(row.return_oc, 2)}" for index, row in df.iterrows()))

    fig = go.Figure(data=[go.Candlestick(x=tickvals,
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'], hovertext=df['return_oc'])])
    
    if self.month_df['low'].size != 0 and self.month_df['high'].size != 0 and self.month_df['close'].size != 0:
      fig.add_hline(y=self.month_df['low'].values[0], line_width=1, line_color="pink")
      fig.add_hline(y=self.month_df['high'].values[0], line_width=1, line_color="green")
      fig.add_hline(y=self.month_df['close'].values[0], line_width=1, line_color="red")
      fig.add_vline(x=0.3, line_width=2, line_dash="dash", line_color="green")

    fig.update_layout(xaxis_rangeslider_visible=False, height=CHART_HEIGHT, xaxis_tickvals=tickvals,
                      xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), margin={"l":0,"r":0,"t":0,"b":0})

    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
