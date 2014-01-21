#!/usr/bin/env python

from datetime import datetime

def from_unix(unixtime):
    return datetime.fromtimestamp(float(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
