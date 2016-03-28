from datetime import datetime
from pandas import DataFrame
import os
import json

from django.test import TestCase
from django.test import Client

from hydro.models import Hydro
from hydro.utils import df_to_db, validate_df_format


class HydroTestCase(TestCase):
    """
    A simple test case on Hydro model using sample test data

    run: "manage.py test hydro -v 2" from top directory
    """

    def setUp(self):
        root = os.path.dirname(os.path.dirname(__file__)) + "/hydro/test_data"
        self.path1 = os.path.join(root, "hydro_data_missing_headers.csv")
        self.path2 = os.path.join(root, "hydro_data_missing_intervals.csv")
        self.path3 = os.path.join(root, "hydro_data.csv")

    def test_validate_df(self):
        with open(self.path1, 'rU') as csv1:
            df1 = DataFrame.from_csv(csv1, sep=",", parse_dates=False)
        with open(self.path2, 'rU') as csv2:
            df2 = DataFrame.from_csv(csv2, sep=",", parse_dates=False)
        with open(self.path3, 'rU') as csv3:
            df3 = DataFrame.from_csv(csv3, sep=",", parse_dates=False)

        with self.assertRaises(ValueError):
            validate_df_format(df1)

        with self.assertRaises(ValueError):
            validate_df_format(df2)

        try:
            validate_df_format(df3)
        except ValueError:
            self.fail("validate_df_format() raised ValueError unexpectedly")

    def test_database(self):
        with open(self.path3, 'rU') as csv3:
            df3 = DataFrame.from_csv(csv3, sep=",", parse_dates=False)

        df_to_db(df3, "Average")

        self.assertEqual(len(Hydro.objects.all()), 1172)

        start = datetime.strptime("11-03-2016 00:00:00", "%d-%m-%Y %H:%M:00")
        end = datetime.strptime("11-03-2016 00:15:00", "%d-%m-%Y %H:%M:00")
        data = Hydro.objects.filter(
            mode="Average", date__range=[start, end]).order_by("date")

        self.assertEqual(len(data), 1172)

        r = data[800]

        self.assertEqual(r.mode, "Average")
        self.assertEqual(r.knots, 0.16)
        self.assertEqual(r.degree, 137)
        self.assertEqual(r.latitude, 22.2115316646)
        self.assertEqual(r.longitude, 113.97343155120001)
        self.assertEqual(r.date,
                         datetime.strptime("11-03-2016 00:00:00", "%d-%m-%Y %H:%M:00"))

    def test_hydro_JSON_data_update(self):

        with open(self.path3, 'rU') as csv3:
            df3 = DataFrame.from_csv(csv3, sep=",", parse_dates=False)

        df_to_db(df3, "Average")

        url = "/updateJSON/"
        params = {"start": "11-03-2016 00:00:00",
                  "end": "11-03-2016 00:00:00",
                  "mode": "Average"}
        c = Client()
        response = c.get(url, params)
        data = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(data), 1172)

        r = data[800]

        self.assertEqual(r["mode"], "Average")
        self.assertEqual(r["knots"], 0.16)
        self.assertEqual(r["degree"], 137)
        self.assertEqual(r["latitude"], 22.2115316646)
        self.assertEqual(r["longitude"], 113.97343155120001)
        self.assertEqual(r["date"], "2016-03-11T00:00:00")
