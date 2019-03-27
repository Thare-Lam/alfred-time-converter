import sys
import time
import datetime
from workflow import Workflow3, ICON_SYNC


invalid_date = 'Invalid datetime'
hint = 'Click Enter to copy'
now = 'now'


def main(wf):
    if len(wf.args) == 1:
        arg = wf.args[0]
        if arg.isdigit():
            s = long(arg)
            format_timestamp(wf, s)
            if s >= 1000:
                format_timestamp(wf, s/1000)
        elif now == arg:
            format_now(wf)
        else:
            format_date(wf, arg)
    else:
        format_datetime(wf, ' '.join([wf.args[0], wf.args[1]]))
    wf.send_feedback()


def format_timestamp(wf, millisecond):
    result = convert_time(time.localtime(millisecond))
    wf.add_item(valid=True, title=result, subtitle=hint, arg=result)


def convert_time(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', t)


def format_now(wf):
    now_time = time.time()
    now_time_s = round(now_time)
    now_time_ms = round(now_time * 1000)
    now_time_format = convert_time(time.localtime(now_time_s))
    wf.add_item(valid=True, title=now_time_format, subtitle=hint, arg=now_time_format)
    wf.add_item(valid=True, title=now_time_ms, subtitle=hint, arg=now_time_ms)
    wf.add_item(valid=True, title=now_time_s, subtitle=hint, arg=now_time_s)


def format_date(wf, date_str):
    try:
        result = long(time.mktime(datetime.datetime.strptime(date_str, '%Y-%m-%d').timetuple()))
        wf.add_item(valid=True, title=result, subtitle=hint, arg=result)
    except Exception:
        return wf.add_item(title=invalid_date)


def format_datetime(wf, datetime_str):
    try:
        result = long(time.mktime(datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').timetuple()))
        wf.add_item(valid=True, title=result, subtitle=hint, arg=result)
    except Exception:
        return wf.add_item(title=invalid_date)


if __name__ == '__main__':
    wf = Workflow3(help_url='https://github.com/Thare-Lam/alfred-time-converter',
                   update_settings={
                       'github_slug': 'Thare-Lam/alfred-time-converter',
                       'frequency': 1
                   })

    if wf.update_available:
        wf.add_item('New version available', 'Action this item to install the update',
                    autocomplete='workflow:update', icon=ICON_SYNC)

    sys.exit(wf.run(main))