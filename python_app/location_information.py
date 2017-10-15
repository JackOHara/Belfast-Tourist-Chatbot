# -*- coding: utf-8 -*-
import urllib2
import json
import os
import googlemaps
import pandas as pd
from haversine import haversine
from bs4 import BeautifulSoup
import wikipedia

def _get_user_lat_lng(location_name):
    ''' Returns the latitude and longitude of a location using googlemaps API.

    Parameters
    ----------
    location_name : string
        String containing location name.

    Returns
    -------
    lat_lng : tuple of len 2
        tuple  containing latitude and longitude as floats.
    '''
    gmaps = googlemaps.Client(key='AIzaSyA34W9N2eayvZEpD4pTJK7cyfqtyjPjupA')
    geocode_result = gmaps.geocode(location_name)
    lat_lng = geocode_result[0]['geometry']['location']
    lat_lng = (lat_lng['lat'], lat_lng['lng'])
    return lat_lng

def _get_open_data_info(location_name):
    ''' Searches through local datasets and finds the most relevant info.
    Could be improved by linking up to open data ni website directly.

    Parameters
    ----------
    location_name : string
        String containing location name.

    Returns
    -------
    lat_lng : tuple containing latitude and longitude as floats.
    dictionary:  containing relevant dataset info
    '''
    lat_lng = _get_user_lat_lng(location_name)
    open_data_directory = '../open-data-ni-datasets/'
    open_data_file_list = os.listdir(open_data_directory)
    open_data_csvs = []

    for (i, j) in zip(open_data_file_list, range(0, len(open_data_file_list))):
        csv = pd.read_csv(open_data_directory+i)
        open_data_csvs.append(csv)
        open_data_file_list[j] = i.split('.', 1)[0]

    open_data_info = {}
    for (i, j) in zip(open_data_csvs, open_data_file_list):
        open_data_info[j] = __closest_open_data_element(lat_lng, i)

    return open_data_info

def __closest_open_data_element(lat_lng_user, dataset):
    ''' Returns the closest lat lng element in dataset.

    Parameters
    ----------
    location_name : tuple containing lat and long
    dataset: pandas dataset

    Returns
    -------
    dictionary:  containing closest dataset row by distance

    '''
    shortest_distance = 1000000
    shortest_station = 0
    for index, row in dataset.iterrows():
        lat_lng_location = (row['LATITUDE'], row['LONGITUDE'])
        distance = haversine(lat_lng_user, lat_lng_location)
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_station = row.to_json()
    shortest_station = json.loads(shortest_station)
    return shortest_station


def _get_wiki_info(place, user_language):
    ''' Returns wiki info for the desired page if it exists. It will also return it in a specified language if it exists.
    If it doesn't then it will returnt he english version.

    Parameters
    ----------
    place : string containing name of place
    user_langes: string containg user language e.g 'en'

    Returns
    -------
    dictionary:  containing wikipedia info

    '''
    search = wikipedia.search(place)
    page = wikipedia.page(search[0])
    soup = BeautifulSoup(urllib2.urlopen(page.url), 'lxml')
    links = [(el.get('lang'), el.get('title')) for el in soup.select('li.interlanguage-link > a')]

    for language, title in links:
        if user_language == language:
            page_title = title.split(u' – ')[0]
            wikipedia.set_lang(language)
            page = wikipedia.page(page_title)
            wikipedia_summary = {
                'page_title' : page.title,
                'page_summary' : page.summary,
                'page_url' : page.url
            }
            wikipedia_summary = json.dumps(wikipedia_summary)
            return json.loads(wikipedia_summary)

    wikipedia_summary = {
        'page_title' : page.title,
        'page_summary' : page.summary,
        'page_url' : page.url
        }
    wikipedia_summary = json.dumps(wikipedia_summary)
    return json.loads(wikipedia_summary)

def get_all_location_info(location_name, language='en'):
    ''' calls all required methods to return relevant info about location.

    Parameters
    ----------
    location_name : string containing location name
    language: string containg user language e.g 'en'

    Returns
    -------
    dictionary:  containing location relevant wikipedia and opendata info.

    '''
    loc = _get_open_data_info(location_name)
    wiki = _get_wiki_info(location_name, language)
    all_info = {
        'location' : loc,
        'wiki' : wiki
    }
    all_info = json.dumps(all_info)
    # all_info = json.loads(all_info)
    return all_info
