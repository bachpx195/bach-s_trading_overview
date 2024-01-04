import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from apps.helpers.datetime_helper import previous_day
from apps.helpers.constants import CHART_CONFIG


class ChartHourComponent:
  def __init__(self, hour_prices, day_prices, date):
    self.hour_prices = self.set_hour_dataframe(hour_prices, date)
    self.day_prices = self.set_day_dataframe(day_prices, date)
    self.date = date

  def set_day_dataframe(self, day_prices, date):
    day_ohlc_alt = day_prices[(
        day_prices['day'] == previous_day(date))].values.tolist()[0]
    day_df_alt = pd.DataFrame(
        [day_ohlc_alt], columns=day_prices.columns)
    day_df_alt = day_df_alt.set_index(pd.DatetimeIndex([f"{previous_day(date)} 00:00:00+00:00"]))

    return day_df_alt
  
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
    
    return_hl = (self.day_prices['high'].values[0] - self.day_prices['low'].values[0])*100/self.day_prices['low'].values[0]
    
    if return_hl >= 4:
      height = 500
    elif return_hl > 1 and return_hl < 4:
      height = 400
    else:
      height = 300

    fig.add_hline(y=self.day_prices['low'].values[0], line_width=1, line_color="pink")
    fig.add_hline(y=self.day_prices['high'].values[0], line_width=1, line_color="green")
    fig.add_hline(y=self.day_prices['close'].values[0], line_width=1, line_color="red")
    fig.add_vline(x=0.3, line_width=2, line_dash="dash", line_color="green")
    fig.add_vline(x=4.2, line_width=2, line_dash="dash", line_color="green")
    fig.add_vline(x=8.8, line_width=2, line_dash="dash", line_color="green")
    fig.update_layout(xaxis_rangeslider_visible=False, height=height, xaxis_tickvals=tickvals,
                      xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
