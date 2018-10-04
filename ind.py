import json
import requests
import subprocess
import time


def slot_notifier(branch='AM', persons=1, initial_slot=None):
    while True:
        try:
            url = 'https://portal.ind.nl/oap/api/desks/%s/slots/?productKey=DOC&persons=%d' % (branch, persons)
            r = requests.get(url)
            time_slots = json.loads(r.content[5:])
            soonest_date = time_slots['data'][0]['date']
            print(r.status_code, soonest_date)
            if initial_slot is None:
                initial_slot = soonest_date
            if soonest_date < initial_slot:
                # send desktop notification
                subprocess.call(['notify-send', 'Time Slot Found', '%s %s' % (branch, soonest_date)])
        except Exception as e:
            print(e)
        time.sleep(30)
