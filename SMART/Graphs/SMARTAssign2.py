# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 11:57:21 2015

@author: Ohm
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 11:18:06 2015

@author: Ohm
"""
from xml.etree.ElementTree import parse
from pandas import DataFrame, Series

doc = parse('generated-data\patient-613876.fhir-bundle.xml')

#root = doc.getroot()

encounter_dates = []

for encounter in doc.findall('.//{http://hl7.org/fhir}Encounter'):
    period = encounter.find('{http://hl7.org/fhir}period')
    start_date = period.find('{http://hl7.org/fhir}start')
    encounter_dates.append(start_date.get('value'))
    
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

"""for sys_bp in systolic_bps:
    print sys_bp

print

for dias_bp in diastolic_bps:
    print dias_bp
"""
enc_dict = {}
enc_dict['encounter_date'] = encounter_dates
enc_dict['systolic_bp'] = systolic_bps
enc_dict['diastolic_bp'] = diastolic_bps

encounters = DataFrame(enc_dict, columns=['encounter_date', 'diastolic_bp', 'systolic_bp'])
encounters = encounters.convert_objects(convert_dates='coerce', convert_numeric=True)
#encounters.encounter_date = encounters.encounter_date.astype("datetime64")
#encounters.diastolic_bp = encounters.diastolic_bp.astype(int)
print encounters

encounters.set_index(['encounter_date'],inplace=True)
encounters.plot(x_compat=True,marker='o')
#encounters.groupby([encounters.encounter_date.dt.week, encounters.encounter_date.dt.year]).count().plot(kind='barh')