import streamlit as st

from apps.models.candlestick import Candlestick
from apps.models.merchandise_rate import MerchandiseRate
from apps.models.analytic_month import AnalyticMonth
from apps.services.ochl_dataframe import *
from apps.helpers.datetime_helper import previous_day, get_start_of_week, to_date


class GetDataService:
  def __init__(self, merchandise_rate, record_limit, start_date, end_date, list_day, month=None, context=None):
    self.merchandise_rate = MerchandiseRate().find_by_slug(merchandise_rate)
    self.record_limit = record_limit
    self.start_date = start_date
    self.end_date = end_date
    self.month = month
    self.context = context
    if list_day:
      self.list_day = self.set_list_day(list_day)
    else:
      self.list_day = None

  def run(self):
    day_prices = load_day_data(self.merchandise_rate,
        self.record_limit, self.start_date, self.end_date, self.list_day)
    week_prices = load_week_data(
        self.merchandise_rate,self.start_date, self.end_date)
    hour_prices = load_hour_data(self.merchandise_rate,
        self.record_limit*24, self.start_date, self.end_date, self.list_day)
        
    return week_prices, day_prices, hour_prices
  
  def get_month_return(self):
    month_return = load_month_return_data(self.merchandise_rate)
    
    return month_return
  
  def get_week_in_month_data(self):
    week_prices = load_week_data(self.merchandise_rate, month=self.month)
    
    return week_prices
  
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
def load_month_return_data(merchandise_rate):
  analytic_month = AnalyticMonth(merchandise_rate)
  month_return = analytic_month.to_df()
  
  return month_return

@st.cache_data
def load_day_data(merchandise_rate, record_limit, start_date, end_date, list_day):
  candlestick = Candlestick(merchandise_rate, 'day', limit=record_limit,
                            sort="DESC", start_date=start_date, end_date=end_date, list_day=list_day)

  prices = candlestick.to_df()
  first_date = prices.iloc[-1].name
  end_date = prices.iloc[0].name.replace(tzinfo=None)

  start_date = get_start_of_week(first_date)
  candlestick = Candlestick(merchandise_rate, 'day', limit=record_limit,
                            sort="DESC", start_date=start_date, end_date=end_date, list_day=list_day)
  prices = candlestick.to_df()
  prices = add_return_column(prices)
  prices = add_day_column(prices)
  prices = add_day_name_column(prices)

  return prices


@st.cache_data
def load_week_data(merchandise_rate,first_date=None,end_date=None, month=None):
  if first_date:
    start_date = get_start_of_week(to_date(first_date))
    candlestick = Candlestick(merchandise_rate, 'week',
                              sort="DESC", limit=100, start_date=start_date, end_date=end_date)
  else:
    candlestick = Candlestick(merchandise_rate, 'week', month=month)

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

