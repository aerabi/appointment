import json
from plyer import notification
import requests
import time


def slot_notifier(branch='AM', persons=1, initial_slot=None):
    while True:
        try:
            url = 'https://portal.ind.nl/oap/api/desks/%s/slots/?productKey=DOC&persons=%d' % (branch, persons)
            r = requests.get(url)
            time_slots = json.loads(r.content[5:])
            soonest_slot = time_slots['data'][0]
            soonest_date = soonest_slot['date']
            start_time = soonest_slot['startTime']
            end_time = soonest_slot['endTime']
            print(r.status_code, soonest_date, start_time, '-', end_time)
            if initial_slot is None:
                initial_slot = soonest_date
            if soonest_date < initial_slot:
                # send desktop notification
                notification_message = '%s %s %s-%s' % (branch, soonest_date, start_time, end_time)
                notification.notify(
                    title='Time Slot Found',
                    message=notification_message,
                    app_name='IND Slot Finder',
                    app_icon='./calendar.png')
        except Exception as e:
            print(e)
        time.sleep(30)
