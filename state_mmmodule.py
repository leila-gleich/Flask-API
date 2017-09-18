import pandas
import csv
import urllib
from datetime import date, timedelta, time, datetime
import sqlite3
from flask import Flask, jsonify

class MusicDatastate:
    def __init__(self, state, start, end):
        self.base_url="https://app.ticketmaster.com/discovery/v2/events.json?apikey=a6U0F5h3AQnINgYGgNMrLn3vxyYsCuyD&keyword=music&segmentName=music&size=200"
        self.dataKeys=["artist", "venue", "date", "image url", "ticket url", "coordinates", "genre", "featured"]
        self.state=state
        self.end=end
        self.start=start

    def add_params(self):
        location_url = self.base_url + "&stateCode=" + self.state
        return location_url

    def set_dates(self):
        return str(self.add_params()) + "&endDateTime=" + self.end + "&startDateTime=" + self.start

    def parse_api(self):
        self.raw_url = self.set_dates()
        # print(self.raw_url)
        url=pandas.read_json(path_or_buf=self.raw_url)
        response = url['_embedded']['events']
        return response

    def find_genre(self):
        data = self.parse_api()
        count = 0
        events = []
        for event in data:
            if 'classifications' in event:
                if 'genre' in event['classifications'][0]:
                    events.append(event)
        return events

    def get_data(self):
        all_events = self.find_genre()
        event_dict = []
        for response in all_events:
            artist_name = response['name']
            venue_name = response['_embedded']['venues'][0]['name']
            date = response['dates']['start']['localDate']
            artist_image_url = response['images'][1]['url']
            ticket_url = response['url']
            if 'location' in  response['_embedded']['venues'][0]:
                coordinates = response['_embedded']['venues'][0]['location']
            else:
                coordinates="Error, no coordinates"
            genre = response['classifications'][0]['genre']['name'].lower()
            featured = 'false'
            info_list = [artist_name, venue_name, date, artist_image_url, ticket_url, coordinates, genre, featured]
            event_dict.append(info_list)
        return event_dict

    def data_dic(self):
        events = []
        for event in self.get_data():
            zipped=dict(zip(self.dataKeys, event))
            events.append(zipped)
        return events

#
# events_instance= MusicDatastate("CA", "2017-08-16T23:59:59-07:00", "2017-09-10T23:59:59-07:00")
# print(type(events_instance.dataKeys))
# data=events_instance.data_dic()

# getdat=events_instance.get_data()

#
# def create_csv(eventDict):
#     headers = ["artist", "venue", "date", "image url", "ticket url", "coordinates", "genre", "featured"]
#     with open('eventdata.csv','w') as f:
#         f_csv = csv.DictWriter(f, headers)
#         f_csv.writeheader()
#         f_csv.writerows(eventDict)
#
# create_csv(data)
