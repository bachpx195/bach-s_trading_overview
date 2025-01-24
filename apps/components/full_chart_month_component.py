import streamlit as st
import plotly.graph_objects as go
from apps.helpers.constants import CHART_CONFIG, CHART_HEIGHT


class FullChartMonthComponent:
  def __init__(self, dataframe):
    self.df = dataframe

  def run(self):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    df = self.df
    df.sort_index(inplace=True) 

    tickvals =[k*0.5 for k in range(len(df))]
    # ticktext = list(
    #     (f"{date.to_pydatetime().strftime('%m-%d')} {round(df.loc[date].return_oc, 2)}" for date in df.index))

    fig = go.Figure(data=[go.Candlestick(x=tickvals,
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'], hovertext=list(
        (f"{date.to_pydatetime().strftime('%d')} {round(df.loc[date].return_oc, 2)}" for date in df.index)))])
    

    fig.add_vline(x=3.9, line_width=2, line_dash="dash", line_color="green")
    fig.update_xaxes(showticklabels=False)

    fig.update_layout(xaxis_rangeslider_visible=False, height=CHART_HEIGHT, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), margin={"l":0,"r":0,"t":0,"b":0})

    st.plotly_chart(fig)
