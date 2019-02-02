import pytz
from datetime import datetime
import pdb

DATE_FORMAT = '%d. %m. %Y %H:%M'


class Night:
    
    def __init__(self, _nid, _tz, _start_time, _end_time, _sched, _duration):
        self.nid = _nid
        self.tz = _tz
        self.start_time = _start_time
        self.end_time = _end_time
        self.start_date = self.start_time.date()
        self.end_date = self.end_time.date()
        # self.sched = _sched
        self.duration = _duration


def read_3_lines_from_csv(lines):
    nid = lines[1][0]
    try:
        tz = pytz.timezone(lines[1][1])
    except pytz.exceptions.UnknownTimeZoneError as e:
        pdb.set_trace()
        print(e)
    start_time = datetime.strptime(lines[1][2], DATE_FORMAT)
    end_time = datetime.strptime(lines[1][3], DATE_FORMAT)
    # sched = datetime.strptime(lines[1][4], DATE_FORMAT)
    sched = None
    hours = float(lines[1][5])

    return Night(nid, tz, start_time, end_time, sched, hours)
