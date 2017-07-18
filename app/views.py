#!/usr/bin/env python
from flask import Flask, render_template, request, json, jsonify, make_response, url_for, abort, Blueprint, send_file, redirect, send_from_directory
from sqlalchemy import select, join, outerjoin, func, or_, and_
from app import settings
from json import dumps as json_dumps
from datetime import datetime

import csv
import logging, sys
import os
import tempfile
import random
import pickle
import re
import time

import urllib

from datetime import datetime, timedelta, date

from StringIO import StringIO

from app import models, db, app

from dateutil import parser as dateparser

import flask_admin as admin


import quandl
quandl.ApiConfig.api_key = ""

mod = Blueprint('views', __name__)


#http://www.nasdaq.com/symbol/vxus/dividend-history
#http://www.nasdaq.com/symbol/vxus/historical

#So now it appears I need to make a screen scraper
#Maybe I can create a 'bootleg service'.
temp_url = "http://www.google.com/finance/historical?q=YHOO&startdate=May+1%2C+2017&enddate=May+18%2C+2017&output=csv"



OPEN = 0
HIGH = 1
LOW = 2
CLOSE = 3
VOLUME = 4
DIVIDEND = 5
SPLIT = 6

def get_stock_data(series, profile):
    data = quandl.get("EOD/"+series["symbol"],start_date=profile["start_date"], end_date=profile["end_date"])
    data_rows = {}
    for row, value in data.iterrows():
        data_rows[str(row)[0:10]]=value.tolist()
        
    return data_rows
    
class PythonObjectEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

# This function's purpose is to ensure that there is an equal number of dates in each series, and that
# Those dates correspond to the shortest series, typically the custom data entered by the user.

def collate_series(series_list):
    parsed_data = []
    
    shortest_series = []


    for series in series_list:
        if len(json.loads(series["data"]))<len(shortest_series) or len(shortest_series) == 0:
            shortest_series = json.loads(series["data"])
        
    collated_series = []
    #collated_series.append(shortest_series)
    sorted_keys = sorted(shortest_series.keys())
        
    
    for series in series_list:
        collating_series = {}
        if json.loads(series["data"])==shortest_series:
            collated_series.append(series)
            continue
        for entry_date in sorted_keys:
            if entry_date in json.loads(series["data"]):
                collating_series[entry_date] = json.loads(series["data"])[entry_date]
            
        series["data"] = json.dumps(collating_series)
        collated_series.append(series)
        
    return series_list


# This function introduced to be sure there are no gaps between days in the series
# This is important because when collating this series with custom data,
# we need to ensure that non-custom series have corresponding dates with every day in the custom series
# This is necessary because the stock markets aren't open every day, but the user may enter series data for any day
# As such, if there are non stock market days with data we want to be sure they're included in the final, collated data

# Functionality-wise, this just takes date strings, converts them to dates, finds the number of days between them
# And then iterates over the days between the 'entry date' (say, a Monday) and the 'previous date' (say, the previous Friday)
# Then in that loop it just copies in the previous day's data

def infill_dates(parsed_history,before_date,after_date):
    gap_days = abs((datetime.strptime(after_date, "%Y-%m-%d") - datetime.strptime(before_date, "%Y-%m-%d")).days)
    next_day = datetime.strptime(before_date, "%Y-%m-%d")
    for i in xrange(gap_days):
        next_day = next_day + timedelta(days=1)
        day = next_day.strftime('%Y-%m-%d')
        parsed_history[day] = str(float(parsed_history[before_date]))
        

#  This function updates non-custom series with time series data obtained from the EOD dataset from Quandl.
#  It also calculates a special daily adjustment, since the adjustment data from Quandl isn't really what we're looking for (it calculates based on the ending price for the entire series rather than only the specific date requested FWIR).

def crunch_series(series, profile):
    if series["custom"]:
        #if the user enters dates which are not padded, we want to be sure to add padding to them
        padded_data = {}
        decoded_data = json.loads(series["data"])
        date_keys = sorted(decoded_data.keys())
        #This is just to ensure we don't have any dates which are outside of the date range of the profile sneaking in
        for date_key in date_keys:
            if datetime.strptime(date_key,"%Y-%m-%d") < datetime.strptime(profile["start_date"],"%Y-%m-%d") or datetime.strptime(date_key,"%Y-%m-%d") > datetime.strptime(profile["end_date"],"%Y-%m-%d"):
                continue

            padded_date = date_key.split("-")
            padded_date[1] = padded_date[1].zfill(2)
            padded_date[2] = padded_date[2].zfill(2)
            new_date = padded_date[0]+"-"+padded_date[1]+"-"+padded_date[2]
            
            padded_data[new_date] = decoded_data[date_key]
            
            
        return padded_data
        
    
    history = get_stock_data(series, profile)
    #return history
    parsed_history = {}
    prev_date = ""
    sorted_keys = sorted(history.keys())
    for entry_date in sorted_keys:
        current_day = {}
        if prev_date=="":
            current_day["value"] = float(profile["start_amount"])
            current_day["shares"] = float(profile["start_amount"])/history[entry_date][CLOSE]
            parsed_history[entry_date] = current_day["value"]
            prev_date = entry_date
            continue
        
        infill_dates(parsed_history,prev_date,entry_date)
        
        dividend_adjustment = float(history[entry_date][DIVIDEND]) / float(history[entry_date][CLOSE])
        split_adjustment = float(history[entry_date][SPLIT])
        price_adjustment = float(history[entry_date][CLOSE]) / float(history[prev_date][CLOSE]) 
        adjustment = dividend_adjustment + split_adjustment
        
        current_day["value"] = parsed_history[prev_date] * price_adjustment
        current_day["value"] = current_day["value"] * adjustment
        
        #This adds the monthly addition on either the first of the month, or the first day in the series after the first of the month,
        #Determined by whether the new date's day is less than the old date's day
        if datetime.strptime(entry_date,"%Y-%m-%d").day == 1 or datetime.strptime(entry_date, "%Y-%m-%d").day < datetime.strptime(prev_date, "%Y-%m-%d").day:
            current_day["value"] += float(profile["monthly_addition"])            

        parsed_history[entry_date] = current_day["value"]
        prev_date = entry_date
    
    infill_dates(parsed_history,prev_date,profile["end_date"])

    return parsed_history

@mod.route('/crunch_profile', methods=['GET', 'POST'])    
def crunch_profile():
    
    profile = request.get_json()
        
    profile_obj = models.Profile()
    profile_obj.monthly_addition = profile["monthly_addition"]
    profile_obj.start_y = profile["start_y"]
    profile_obj.start_amount = profile["start_amount"]
    profile_obj.start_date = profile["start_date"]
    profile_obj.end_date = profile["end_date"]

    db.session.add(profile_obj)
    db.session.commit()
    
    
    profile["id"] = profile_obj.id
    series_list = []
    for series in profile["series"]:
        series["data"]=json.dumps(crunch_series(series,profile))
        series_list.append(series)
    collated_series = collate_series(series_list)
    for series in collated_series:
        series_obj = models.Series()
        series_obj.name = series["name"]
        series_obj.symbol = series["symbol"]
        series_obj.custom= True if series["custom"] else False
        series_obj.data = series["data"]
        series_obj.profile_id = profile_obj.id
        db.session.add(series_obj)

    db.session.commit()
    
    profile["series"] = collated_series
    return jsonify({"profile":profile})
    



@mod.route('/', methods=['GET', 'POST'])
def index():    
    return redirect("/app")
    
@mod.route('/app', methods=['GET', 'POST'])
def app():
    '''
    series = {}
    profile = {}
    if "profile_id" in request.args.get:
        
        profile = db.session.query(models.Profile).get(request.args.get('profile_id'))
        series = db.session.query(model.Series).filter_by(profile_id=profile.id).all()
    '''
    profile_id=0
    active_panel=1
    if "profile_id" in request.args:
        profile_id=request.args.get("profile_id")
        
    if profile_id!=0:
        active_panel=0

    return render_template("app.html", profile_id=profile_id,active_panel=active_panel)
