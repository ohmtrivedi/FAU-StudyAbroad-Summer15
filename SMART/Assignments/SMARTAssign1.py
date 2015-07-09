# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 11:18:06 2015

@author: Ohm
"""
from xml.etree.ElementTree import parse
from pandas import DataFrame, Series

doc = parse('generated-data\patient-613876.fhir-bundle.xml')

root = doc.getroot()

"""for item in doc.iterfind('feed/'):
    title = item.findtext('title')
    print title
    print doc
"""
#found = [element for element in doc.iter() if element.text == 'A']
#encounters = doc.findall('{http://hl7.org/fhir}Encounter')
#print encounters

encounter_dates = []
for encounter in doc.findall('.//{http://hl7.org/fhir}Encounter'):
    period = encounter.find('{http://hl7.org/fhir}period')
    start_date = period.find('{http://hl7.org/fhir}start')
    encounter_dates.append(start_date.get('value'))

#print len(encounter_dates)

enc_dates = DataFrame(encounter_dates, columns= ['date'])
enc_dates.date = enc_dates.date.astype("datetime64")
print enc_dates

enc_dates.groupby([enc_dates.date.dt.week, enc_dates.date.dt.year]).count().plot(kind="barh")
