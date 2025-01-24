import streamlit as st

from apps.models.candlestick import Candlestick
from apps.models.merchandise_rate import MerchandiseRate
from apps.services.ochl_dataframe import *
from apps.helpers.datetime_helper import previous_day, get_start_of_week, to_date


class GetMonthDataService:
  def __init__(self, merchandise_rate, month):
    self.merchandise_rate = MerchandiseRate().find_by_slug(merchandise_rate)
    self.month = month

  def run(self):
    month_with_previous_month_prices = load_month_data(self.merchandise_rate, self.month)
    month_prices = month_with_previous_month_prices[month_with_previous_month_prices["month"] == self.month]
    day_prices =  load_day_data(self.merchandise_rate, self.month)
    return month_prices, month_with_previous_month_prices, day_prices


@st.cache_data
def load_day_data(merchandise_rate, month):
  candlestick = Candlestick(merchandise_rate, 'day', sort="DESC", month=month)
  prices = candlestick.to_df()
  prices = add_return_column(prices)

  return prices


@st.cache_data
def load_week_data(merchandise_rate,first_date,end_date):
  start_date = get_start_of_week(to_date(first_date))
  candlestick = Candlestick(merchandise_rate, 'week',
                            sort="DESC", start_date=start_date, end_date=end_date)

  prices = candlestick.to_df()
  prices = add_return_column(prices)

  return prices

@st.cache_data
def load_hour_data(merchandise_rate, record_limit, start_date, end_date, list_day):
  candlestick = Candlestick(merchandise_rate, 'hour', limit=record_limit*24,
                            sort="DESC", start_date=start_date, end_date=end_date, list_day=list_day)

  prices = candlestick.to_df()
  prices = add_day_name_with_binance_column(prices)

  return prices

@st.cache_data
def load_month_data(merchandise_rate, month):
  month_list = f"{month - 2 if month - 2 > 0 else 12 +  month - 2 },{month - 1 if month - 1 > 0 else 12 +  month - 1 },{month}"
  candlestick = Candlestick(merchandise_rate, 'month', month=month_list)

  prices = candlestick.to_df()

  return prices
  
  