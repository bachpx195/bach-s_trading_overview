import streamlit as st

from apps.models.candlestick import Candlestick
from apps.models.merchandise_rate import MerchandiseRate
from apps.services.ochl_dataframe import *
from apps.helpers.datetime_helper import previous_day


class GetDataService:
  def __init__(self, merchandise_rate, record_limit, start_date, end_date, list_day):
    self.merchandise_rate = MerchandiseRate().find_by_slug(merchandise_rate)
    self.record_limit = record_limit
    self.start_date = start_date
    self.end_date = end_date
    if list_day:
      self.list_day = self.set_list_day(list_day)
    else:
      self.list_day = None

  def run(self):
    day_prices = load_day_data(self.merchandise_rate,
        self.record_limit, self.start_date, self.end_date, self.list_day)
    hour_prices = load_hour_data(self.merchandise_rate,
        self.record_limit*24, self.start_date, self.end_date, self.list_day)
        
    return day_prices, hour_prices
  
  def set_list_day(self, list_day):
    list_custom_day = []

    for date in list_day.split(','):
      date_str = date.strip()
      if date_str not in list_custom_day:
        list_custom_day.append(date_str)
      previous = previous_day(date_str)
      if previous not in list_custom_day:
        list_custom_day.append(previous)
      previous_previous = previous_day(previous)
      if previous_previous not in list_custom_day:
        list_custom_day.append(previous_previous)

    return list_custom_day

@st.cache_data
def load_day_data(merchandise_rate, record_limit, start_date, end_date, list_day):
  candlestick = Candlestick(merchandise_rate, 'day', limit=record_limit,
                            sort="DESC", start_date=start_date, end_date=end_date, list_day=list_day)

  prices = candlestick.to_df()
  prices = add_return_column(prices)
  prices = add_day_volatility_column(prices)
  prices = add_day_name_column(prices)
  prices = add_day_column(prices)

  return prices

@st.cache_data
def load_hour_data(merchandise_rate, record_limit, start_date, end_date, list_day):
  candlestick = Candlestick(merchandise_rate, 'hour', limit=record_limit*24,
                            sort="DESC", start_date=start_date, end_date=end_date, list_day=list_day)

  prices = candlestick.to_df()
  prices = add_day_name_with_binance_column(prices)

  return prices

