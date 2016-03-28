import datetime
import requests
import random
from pandas import DataFrame
from io import StringIO

from hydro import settings
from hydro.models import Hydro


def get_latest_hydro_data():
    """
    retrieves and saves the latest data from tidal site
    """
    days_ahead = settings.max_days_ahead
    for key in settings.modes.keys():
        df = get_hydro_dataframe(days_ahead, key)
        df_to_db(df, key)


def get_hydro_dataframe(days, mode):
    """
    retrieves csv data based on mode and days ahead of current time (HK),
    convert it to dataframe, check its format to ensure consistency
    """
    if days >= -settings.max_days_behind and\
            days <= settings.max_days_ahead:

        current_time = datetime.datetime.now(settings.tz)

        start_time = current_time + datetime.timedelta(days=days)
        start_date = start_time.strftime("%Y-%m-%d 00:00:00")
        end_date = start_time.strftime("%Y-%m-%d %H:45:00")

        url = settings.gen_url(
            start_date, end_date, settings.modes[mode]
        )
        r = requests.get(url)

        strData = StringIO(r.content.decode('utf-8'))
        df = DataFrame.from_csv(strData, sep=",", parse_dates=False)

        validate_df_format(df)

        return df


def validate_df_format(hydroDf):
    """
    validate csv format, Erros will be raised if csv data retrieved
    from tidal site changes its format
    """
    row_name = list(hydroDf.index)[0]
    sub_hydroDf = hydroDf.ix[[row_name]]
    for quarter in set(hydroDf.Time):
        intervals = sub_hydroDf[sub_hydroDf.Time == quarter].shape[0]
        if intervals != settings.intervals:
            raise ValueError(
                "retrived csv's prediction intervals has changed size"
            )

    headers = list(hydroDf.columns.values)
    if headers != settings.headers:
        raise ValueError(
            "retrived csv's headers does not match default"
        )


def df_to_db(hydroDf, mode):
    """
    saves dataframe row entries to database in bulk
    """
    time, knots, degree, latitude, longitude = settings.headers

    hydroDf["date"] = list(hydroDf.index)

    inte = [i for i in range(1, settings.intervals + 1)]

    intervals = settings.intervalsInDay * inte

    hydro_models = []

    for row in zip(hydroDf["date"], hydroDf[time], intervals,
                   hydroDf[knots], hydroDf[degree], hydroDf[latitude],
                   hydroDf[longitude]):
        hydro_models.append(build_hydro_model(mode, *row))

    Hydro.objects.bulk_create(hydro_models)


def build_hydro_model(mode, date, time, interval, knots, degree, lati, longi):

    """
    building datebase model, the check if data already exists was commented out
    for efficiency performance, making the assumption that it is always new data
    coming from tidal site
    """

    date = datetime.datetime.strptime(date + time, settings.datetime_format)

    # if not Hydro.objects.filter(
    #     mode=mode, date=date, prediction_interval=interval).exists():

    return Hydro(
        mode=mode,
        date=date,
        knots=knots,
        degree=degree,
        latitude=lati,
        longitude=longi,
        prediction_interval=interval
    )
