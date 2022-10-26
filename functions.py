from io import StringIO
import pandas
import asyncio


def failsafe(df):
    if 'user_country' not in df:
        df['user_country'] = "Not initialized"
    if 'CIME_geolocation_string' not in df:
        df['CIME_geolocation_string'] = "Not Initialized"


def get_or_setandget(mydict, key, default):
    if key not in mydict:
        mydict[key] = default
    return mydict[key]


def checkmap(csv_contents):
    lastid = len(csv_contents) - 1  # only last id
    try:
        df = csv_contents[lastid]
        tmp = StringIO(df)
        df = pandas.read_csv(tmp)
    except Exception:
        return False, None

    if 'CIME_geolocation_centre' in df:
        return True, df

    return False, None


def check_user_loc(csv_contents):
    lastid = len(csv_contents) - 1  # only last id
    try:
        df = csv_contents[lastid]
        tmp = StringIO(df)
        df = pandas.read_csv(tmp)
    except Exception:
        return False
    if 'GeotextAugmenter' in df:
        return True
    return False


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


# For tracking GA without waiting for response (otherwise is locking awaiting possible events fired afterward)
def fire_and_forget(f):
    def wrapped(*args, **kwargs):
        loop = get_or_create_eventloop()
        return loop.run_in_executor(None, f, *args, *kwargs)

    return wrapped
