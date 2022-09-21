import csv
import json


def csvtojson(csvfilepath, outputjsonfilepath):

    csvReader = csv.DictReader(csvfilepath)