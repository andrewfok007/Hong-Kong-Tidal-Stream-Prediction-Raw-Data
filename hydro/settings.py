from pytz import timezone


def gen_url(start_date, end_date, mode):
    """
    returns url for Tidal Stream Predictions csv data

    >>> start_date = "2016-03-08 00:00:00"
    >>> end_date = "2016-03-09 00:00:00"
    >>> mode = "Average"
    >>> actual = hydro_url(start_date, end_date, mode)
    >>> expected = ("http://current.hydro.gov.hk/en/download_csv.php?start_dt"
    ... "=2016-03-08 00:00:00&end_dt=2016-03-09 00:00:00&mode=Average")
    >>> expected == actual
    True
    """
    return ("http://current.hydro.gov.hk/en/download_csv.php?"
            "start_dt={}&end_dt={}&mode={}").format(start_date, end_date, mode)

tz = timezone("Hongkong")

# The maximum days forward allowed for csv data retrieveal
max_days_ahead = 6

# The maximum days backward allowed for csv data retrieveal
max_days_behind = 2

# Number of entries within a 15 minutes period
intervals = 1172

# csv data headers
headers = ['Time', 'Knots', 'Degree', 'Latitude(WGS84)', 'Longitude(WGS84)']

# Number of 15 minutes in a day
intervalsInDay = 24 * 4

datetime_format = '%Y-%m-%d%H:%M'

# csv data tidal mode
modes = {"Average": "Average", "Surface": "Surface"}

# celery task message
message = "Saving data from Hong Kong Tidal Stream Prediction website"
