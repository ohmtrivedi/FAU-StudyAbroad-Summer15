# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 18:52:46 2015

@author: Ohm
"""
from xml.etree.ElementTree import parse
from pandas import DataFrame
import matplotlib.pyplot as plt
import plotly.plotly as py
import os

path = "C:\Users\Ohm\Documents\Python Scripts\XML Parsing\generated-data"
dirs = os.listdir(path)

#patient_list = ['613876','621799','644201','665677','736230','765583','880378','897185','935270','967332']
mean_bp = []
count = 0

for patient in dirs:
    #filename = 'generated-data\patient-' + patient + '.fhir-bundle.xml' 
    filename = 'generated-data\\' + patient
    #print filename
    doc = parse(filename)

    encounter_dates = []
    
    for encounter in doc.findall('.//{http://hl7.org/fhir}Encounter'):
        period = encounter.find('{http://hl7.org/fhir}period')
        start_date = period.find('{http://hl7.org/fhir}start')
        encounter_dates.append(start_date.get('value'))
    
    if not encounter_dates:
        #print "No Encounter Dates"
        continue
    
    systolic_bps = []
    diastolic_bps = []
    
    for observation in doc.findall('.//{http://hl7.org/fhir}Observation'):
        text_ele = observation.find('{http://hl7.org/fhir}text')
        div = text_ele.find('{http://www.w3.org/1999/xhtml}div')
        if div.text.find('Systolic') != -1:
            value_quant = observation.find('{http://hl7.org/fhir}valueQuantity')
            value = value_quant.find('{http://hl7.org/fhir}value')
            systolic_bps.append(value.get('value'))
        if div.text.find('Diastolic') != -1:
            value_quant = observation.find('{http://hl7.org/fhir}valueQuantity')
            value = value_quant.find('{http://hl7.org/fhir}value')
            diastolic_bps.append(value.get('value'))
    
    if (not systolic_bps) & (not diastolic_bps):
        #print "No Systolic/Diastolic BP"
        continue
    
    enc_dict = {}
    enc_dict['encounter_date'] = encounter_dates
    enc_dict['systolic_bp'] = systolic_bps
    enc_dict['diastolic_bp'] = diastolic_bps
    
    encounters = DataFrame(enc_dict, columns=['encounter_date', 'diastolic_bp', 'systolic_bp'])
    encounters = encounters.convert_objects(convert_dates='coerce', convert_numeric=True)
    #print encounters
    enc_period = encounters[(encounters.encounter_date.dt.year >= 2004) & (encounters.encounter_date.dt.year <= 2006)]
    if enc_period.empty:
        #print "No data between given period"
        continue
    #print encounters0406
    
    enc_period['mean_bp'] = enc_period['diastolic_bp'] + ((enc_period['systolic_bp']-enc_period['diastolic_bp'])/3)
    mbp = enc_period['mean_bp'].mean()
    mean_bp.append(mbp)
    count = count + 1
    #print encounters0406
    #print mbp
    #print
    
print mean_bp
print count
plt.hist(mean_bp, stacked=True)
plt.title("Gaussian Histogram")
plt.xlabel("Mean Blood Pressure")
plt.ylabel("Frequency")

fig = plt.gcf()

#plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')