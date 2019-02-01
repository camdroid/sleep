import pytz
import pdb


class Night:
    nid = None
    tz = None
    
    def __init__(self, _nid, _tz, _start_time, _end_time, _sched):
        self.nid = _nid
        self.tz = _tz
        self.start_time = _start_time
        self.end_time = _end_time
        self.sched = _sched


def read_3_lines_from_csv(lines):
    nid = lines[1][0]
    try:
        tz = pytz.timezone(lines[1][1])
    except pytz.exceptions.UnknownTimeZoneError as e:
        pdb.set_trace()
        print(e)
    start_time = lines[1][2]
    end_time = lines[1][3]
    sched = lines[1][4]

    return Night(nid, tz, start_time, end_time, sched)
