import os
import json
import subprocess
import requests
import time
import math
import sys

from datetime import datetime
from collections import namedtuple

import numpy as np

from piksi_tools import time_utils
from sbp.gnss import GPSTimeNano
from sbp.navigation import MsgAssistance

GPSTime = namedtuple('GPSTime', ['wn', 'tow', 'ns'])
CoarseLocation = namedtuple('CoarseLocation', ['lat', 'lon', 'accuracy'])

def get_current_location():
  api_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key='
  api_key =  os.environ['GOOGLE_WIFI_API_KEY']

  cmd = ["/System/Library/PrivateFrameworks/Apple80211."
          "framework/Versions/Current/Resources/airport "
          "-s | grep -io '[0-9a-f:]\{17\}\ \-[0-9]\{2\}'"]

  mac_ids = subprocess.check_output(cmd, shell=True)

  access_points = []
  for l in mac_ids.split('\n'):
    split = l.split()
    if len(split) == 2:
      access_points.append({
        'macAddress': split[0],
        'signalStrength': int(split[1])
        })

  print "Scanned %s Wi-Fi access points, determining location..." % len(access_points)
  r = requests.post(api_url + api_key, json={'wifiAccessPoints': access_points})
  if r.status_code == 200:
    rj = r.json()
  else:
    raise ValueError("Bad response from Google Wi-Fi API.")
  cl = CoarseLocation(rj['location']['lat'], rj['location']['lng'], rj['accuracy'])
  print "Coarse location: %s" % (cl,)
  return cl

def get_current_gps_time():
  utc_now = np.datetime64(datetime.utcnow())
  gps_now = time_utils.utc_to_gpst(utc_now)
  tow_ms = time_utils.seconds_to_ms(gps_now['tow'])
  tow_ms_floor = int(round(tow_ms))
  ns = int(round((tow_ms - tow_ms_floor) * 1.e6))
  gt = GPSTime(gps_now['wn'], tow_ms_floor, ns)
  print "Coarse time: %s" % (gt,)
  return gt

def get_assistance_data():
  print "Getting a coarse Wi-Fi based location..."
  loc = get_current_location()
  print "Getting a coarse time..."
  time = get_current_gps_time()
  return loc, time

def make_sbp_message(loc, time):
  t = GPSTimeNano(wn=time.wn, tow=time.tow, ns=time.ns)
  msg = MsgAssistance(time=t, lat=loc.lat, lon=loc.lon, alt=0, accuracy=loc.accuracy)
  return msg

def get_data_make_msg():
  loc, time = get_assistance_data()
  return make_sbp_message(loc, time)

def get_ephemeris():
  header = {'Accept': 'application/vnd.swiftnav.broker.v1+sbp2'}
  url = 'http://ephemeris.testing.skylark.swiftnav.com'
  print "Downloading ephemeris data from Skylark..."
  r = requests.get(url, headers=header)
  return r.content
