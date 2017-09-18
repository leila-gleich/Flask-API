import logging
import pandas
from state_mmmodule import MusicDatastate
from tm_module import MusicDataCity
import time
from datetime import date
from datetime import datetime
from datetime import timedelta

city1 = "los" + "%" + "angeles"
city2 = "san" + "%" + "diego"
start = "2017-09-15T23:59:59-07:00"
end = "2017-09-25T23:59:59-07:00"

la_events_instance= MusicDataCity(city1, start, end)
sd_events_instance= MusicDataCity(city2, start, end)
state_events_instance= MusicDatastate("CA", start, end)

la_events = la_events_instance.data_dic()
ca_events = state_events_instance.data_dic()
sd_events = sd_events_instance.data_dic()
all_results = la_events + ca_events + sd_events


unique_events = []
for event in all_results:
    if event not in unique_events:
        unique_events.append(event)


print(len(unique_events))
