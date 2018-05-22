# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:12:50 2018

@author: PIYUSH
"""

import pandas as pd

import plotly
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.dashboard_objs as dashboard

import numpy as np

import IPython.display
from IPython.display import Image

import re

#Setting plotly user
'''
username = 'varpiyush'
api_key='MIuUtZ4batoJ9OouNmAM'
'''
username = 'maybhat'
api_key = 'Bef2UsFGii7RqHBzjYpr' 
plotly.tools.set_credentials_file(username=username, api_key=api_key)

#Map FileId and ShareKey Generators
def fileId_from_url(url):
    """Return fileId from a url."""
    raw_fileId = re.findall("~[A-z]+/[0-9]+", url)[0][1: ]
    return raw_fileId.replace('/', ':')

def sharekey_from_url(url):
    """Return the sharekey from a url."""
    if 'share_key=' not in url:
        return "This url is not 'sercret'. It does not have a secret key."
    return url[url.find('share_key=') + len('share_key='):]

#Map Integration
def mapInteg():
    mapbox_access_token = 'pk.eyJ1IjoidmFycGl5dXNoIiwiYSI6ImNqZ3c2dXRlbTAzMjEyd253aWN5aWJyc3oifQ.1KH3xPnBcyepYyyKiMrNMA'
    
    df = pd.read_csv('C:/Users/PIYUSH/Downloads/neempins.csv')
    site_lat = df.lat
    site_lon=df.lon
    locations_name = df.text
    
    data = Data([
        Scattermapbox(
            lat=site_lat,
            lon=site_lon,
            mode='markers',
            marker=Marker(
                size=17,
                color='rgb(10, 255, 10)',
                opacity=0.7
            ),
            text=locations_name,
            hoverinfo='text'
        ),
        Scattermapbox(
            lat=site_lat,
            lon=site_lon,
            mode='markers',
            marker=Marker(
                size=8,
                color='green',
                opacity=0.7
            ),
            hoverinfo='none'
        )]
    )
    
    layout = Layout(
        title='Location of Smart Meter Deployments',
        autosize=False,
        width=450,
        height=450,
        margin=go.Margin(
            l=5,
            r=5,
            b=5,
            t=100,
            pad=4
    ),
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=23,
                lon=80
            ),
            pitch=0,
            zoom=3,
            style='light'
        ),
    )
    
    fig_map = dict(data=data, layout=layout)
    url_map=py.plot(fig_map, filename='NeemMap',sharing='public',validate=False)
    return (url_map)

def timeserInteg():
    ds_ts = pd.read_csv('C:/Users/PIYUSH/Downloads/dailyelecunits.csv')
    ds_ts_DepUnique=ds_ts.DEP.unique()
    ds_ts_final={}
    LenDepUnique=len(ds_ts_DepUnique)

    #looping through Deployment Ids
    for i in range (0,LenDepUnique):
        ds_ts_temp=[] #resets temp for everytime
        ds_ts_filter=ds_ts_DepUnique[i] #Sets the Deployment id (say SHM-4B-2 | Clasp-192)as filter
        ds_ts_temp=ds_ts[(ds_ts.DEP)==ds_ts_filter] # Checks across DEP column for Deployment id and assigns array to a temp variable 
        ds_ts_final.update({ds_ts_filter:[ds_ts_temp]})
    
    ds_ts_filter='AHM-1B-1 | Clasp-74'
    ds_ts_temp=ds_ts[(ds_ts.DEP)==ds_ts_filter]
    x=ds_ts_temp.DATE
    y=ds_ts_temp.KWH
    '''
    data=[]
    data.append(x)
    data.append(y)
    '''
    trace=go.Scatter(x=x,y=y)
    data=[trace]       
    layout=dict(title='Time Series Data: Hourly Energy Use',
                autosize=False,
                width=600,
                height=450,
                margin=go.Margin(
                    l=5,
                    r=5,
                    b=5,
                    t=100,
                    pad=4),
                xaxis=dict(
                        rangeselector=dict(
                                buttons=list([
                                        dict(count=1,
                                             label='1m',
                                             step='month',
                                             stepmode='backward'),
                                        dict(count=6,
                                             label='6m',
                                             step='month',
                                             stepmode='backward'),
                                        dict(count=1,
                                             label='YTD',
                                             step='year',
                                             stepmode='todate'),
                                        dict(count=1,
                                             label='1y',
                                             step='year',
                                             stepmode='backward'),
                                        dict(step='all')                                             
                                             ])
                                        ),
                                        rangeslider=dict(),
                                        type='date')
                                        )
    #plot scatter chart
    fig_ts=dict(data=data,layout=layout)
    url_plot=py.plot(fig_ts, filename='NeemLine',sharing='public',validate=False)
                                        
    return (url_plot)

# Main Dashboard Function

##Accessing map for the dashboard
url_map=mapInteg()
fileId_map = fileId_from_url(url_map)
sharekey_map=sharekey_from_url(url_map)

##Accessing TimeSeries Plot for the dashboard
url_plot=timeserInteg()
fileId_plot=fileId_from_url(url_plot)
sharekey_plot=sharekey_from_url(url_plot)

##Assigning boxes to Plots/figures
###Map
box_map = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_map,
    'title': 'Neemboriyan',
}
###TimeSeries
box_plot= {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_plot,
    'title': 'Neem Branches',
}

##Creating Dashboard 
NeemDash=dashboard.Dashboard()
#NeemDash=['layout']['size'] = 3000

### Insert box in dashboard 
NeemDash.insert(box_plot)
NeemDash.insert(box_map, 'left', 1, fill_percent=40)

###Styling Dashboard
NeemDash['settings']['title'] = 'National Energy End-use Monitoring Dashboard'
NeemDash['settings']['logoUrl'] = 'http://edsglobal.com/images/homepagetext/basetext/EDS.png'
NeemDash['settings']['links'] = []
NeemDash['settings']['links'].append({'title': 'Environmental Design Solutions', 'url': 'http://www.edsglobal.com/'})
NeemDash['settings']['links'].append({'title': 'Zenatix', 'url': 'https://zenatix.com/'})
NeemDash['settings']['links'].append({'title': 'CLASP', 'url': 'https://clasp.ngo/'})
NeemDash['settings']['foregroundColor'] = '#000000'
NeemDash['settings']['backgroundColor'] = '#adcaea'
NeemDash['settings']['headerForegroundColor'] = '#ffffff'
NeemDash['settings']['headerBackgroundColor'] = '#9ad845'
NeemDash['settings']['boxBackgroundColor'] = '#ffffff'
NeemDash['settings']['boxBorderColor'] = '#000000'
NeemDash['settings']['boxHeaderBackgroundColor'] = '#ffffff'

py.dashboard_ops.upload(NeemDash, 'NEEM')
