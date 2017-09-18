import pandas
import csv
import urllib
import requests
import time
from datetime import date
from datetime import datetime
from datetime import timedelta

from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd
import requests

class EventBriteConcerts:
    def __init__(self, end):
        self.base_url=    "https://www.eventbriteapi.com/v3/events/search/?token=GJMNDMWASHYCSZEIR42S&location.address=california&categories=103&start_date.keyword=today&start_date.range_end="+ end
        self.dataKeys=["artist", "venue", "date", "image url", "ticket url", "coordinates", "genre", "featured"]
        self.end=end

    # def make_request(self):
    #     response = requests.get(
    #         self.base_url,
    #         headers = {
    #             "Authorization": "Bearer GJMNDMWASHYCSZEIR42S",
    #         },
    #         verify = True,  # Verify SSL certificate
    #     )
    #     base = response.json()
    #     return base

    def parse_api(self):
        data = json.loads(requests.get(self.base_url).text)
        response = data['events']
        return response

    def get_data(self):
        event_dict = []
        for event in self.parse_api():
            artist_name = event['name']['text']
            venue = event['venue_id']
            date_time = event['start']['local']
            date = date_time[:10]

            ticket_url = event['url']
            featured="false"
            if event['logo'] is not None:
                artist_image_url = event['logo']['url']
            else:
                artist_image_url = 'None'
            #make a method
            if event['venue_id'] is not None:
                venue_id = event['venue_id']
                venue_response = requests.get(
                    "https://www.eventbriteapi.com/v3/venues/"+ venue_id,
                    headers = {
                        "Authorization": "Bearer GJMNDMWASHYCSZEIR42S",
                    },
                    verify = True,  # Verify SSL certificate
                )
                venue_base = venue_response.json()
                venue_name = venue_base['name']
            else:
                venue_name = "Unknown"
            coordinates = {'latitude':venue_base['address']['latitude'], 'longitude':venue_base['address']['longitude']}
            #make a method
            subcat_id = event["subcategory_id"]
            if subcat_id is not None:
                subcat_response = requests.get(
                    "https://www.eventbriteapi.com/v3/subcategories/"+ subcat_id,
                    headers = {
                        "Authorization": "Bearer GJMNDMWASHYCSZEIR42S",
                    },
                    verify = True,  # Verify SSL certificate
                )
                genre = subcat_response.json()['name']
            else:
                genre = "Other"
            info_list = [artist_name, venue_name, date, artist_image_url, ticket_url, coordinates, genre, featured]
            event_dict.append(info_list)
        return event_dict

    def data_dic(self):
        events = []
        for event in self.get_data():
            zipped=dict(zip(self.dataKeys, event))
            events.append(zipped)
        return events


#get end date

def get_end():
    today = date.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    if len(day) == 1:
        day = "0"+ day
    if len(month) == 1:
        month = "0" + month
    tendays = datetime.now() + timedelta(days=10)
    endday = str(tendays.day)
    end = year + "-" + month + "-" + endday
    end = end + "T02%3A00%3A00Z"
    return end

# events_instance=EventBriteConcerts(get_end())
# print(type(events_instance.parse_api()))




# data = pd.DataFrame.from_dict(df, orient='index')




# print(len(events_instance.data_dic()))




# response = requests.get(
#     "https://www.eventbriteapi.com/v3/events/search/?location.address=california&categories=103&start_date.keyword=today&start_date.range_end=" + end,
#     headers = {
#         "Authorization": "Bearer GJMNDMWASHYCSZEIR42S",
#     },
#     verify = True,  # Verify SSL certificate
# )
#
#
# #put take page count from pagination and for that many times add param page = i and increase until i=page count
# base = response.json()['events']
#
#
#
# event_dict = []
# for event in base:
#     artist_name = event['name']['text']
#     venue = event['venue_id']
#     date_time = event['start']['local']
#     date = date_time[:10]
#
#     ticket_url = event['url']
#     featured="false"
#
#
#
#     if event['logo'] is not None:
#         artist_image_url = event['logo']['url']
#     else:
#         artist_image_url = 'None'
#     #make a method
#     venue_id = event['venue_id']
#     venue_response = requests.get(
#         "https://www.eventbriteapi.com/v3/venues/"+ venue_id,
#         headers = {
#             "Authorization": "Bearer GJMNDMWASHYCSZEIR42S",
#         },
#         verify = True,  # Verify SSL certificate
#     )
#     venue_base = venue_response.json()
#     venue_name = venue_base['name']
#     coordinates = {'lat':venue_base['address']['latitude'], 'lon':venue_base['address']['longitude']}
#
#
#     #make a method
#     subcat_id = event["subcategory_id"]
#     if subcat_id is not None:
#         subcat_response = requests.get(
#             "https://www.eventbriteapi.com/v3/subcategories/"+ subcat_id,
#             headers = {
#                 "Authorization": "Bearer GJMNDMWASHYCSZEIR42S",
#             },
#             verify = True,  # Verify SSL certificate
#         )
#         genre = subcat_response.json()['name']
#     else:
#         genre = "Other"
#     info_list = [artist_name, venue_name, date, artist_image_url, ticket_url, coordinates, genre, featured]
#     event_dict.append(info_list)
#
# dataKeys=["artist", "venue", "date", "image url", "ticket url", "coordinates", "genre", "featured"]
# events = []
# for event in event_dict:
#     zipped=dict(zip(dataKeys, event))
#     events.append(zipped)
#
# print(len(events))
