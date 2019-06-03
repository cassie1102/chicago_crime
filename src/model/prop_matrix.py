# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:56:07 2019

@author: andyj
"""

import os 
import pandas as pd
import numpy as np


# setwd
os.chdir('E:/projects/chi_crime/src/etl/')

###########
# imports #
###########
#m prop_table
prop_table = pd.read_csv('../../data/processed/prop_table_edit.csv', index_col = 0)

# predictions
preds = pd.read_csv('../../data/processed/arima_2_preds.csv', header = None)
preds = preds[1]

# test forecast
test_forecast = pd.read_csv('../../data/processed/test_forecasted.csv', header = None) 
test_forecast = test_forecast[1]

# test actuals
test_actuals = pd.read_csv('../../data/processed/test_actuals.csv', header = None)
test_actuals = test_actuals[1]

# check all element equal 100
prop_table.sum().sum() # .99998 is close enough


###############
# form tables #
###############

# actual table
actual_table = prop_table
def set_actual(prop_table, i):
    actual_table = prop_table
    actual_table *= test_actuals[i]
    prop_table = pd.read_csv('../../data/processed/prop_table_edit.csv', index_col = 0) #reset prop
    return actual_table, prop_table
    
# forecast table
forecast_table = prop_table
def set_forecast(prop_table, i):
    forecast_table = prop_table
    forecast_table *= test_forecast[i]
    prop_table = pd.read_csv('../../data/processed/prop_table_edit.csv', index_col = 0) #reset prop
    return forecast_table, prop_table

############
# evaluate #
############

def check_error(matrix_forecast, matrix_actual, sse_total):
    error_matrix = matrix_forecast.sub(matrix_actual)
    error_matrix = np.square(error_matrix)
    sse = error_matrix.sum().sum()
    print('Sum of Square Errors in Prediction Matrix: %.2f' %(sse))
    sse_total += sse
    return sse_total
    
# check against actual
sse_total = 0
for i in range(0, len(test_actuals) - 1):
    forecast_table, prop_table = set_forecast(prop_table, i)
    actual_table, prop_table = set_actual(prop_table, i)
    
    sse_total = check_error(forecast_table, actual_table, sse_total)

# print out average error
#avg_error = np.sqrt(sse_total/len(test_actuals)-1)
#print('Average Weekly Error Rate: %.2f' %(avg_error))
 
# example error
error_matrix = forecast_table.sub(actual_table)
avg_error_intersect = error_matrix.sum().sum()/(77*21)
print('Example Error Rate per intersect: %.2f' %(avg_error_intersect))



##############
# FINAL PRED #
##############
# next week predictions 
pred_table = prop_table
pred_table *= preds[1]
prop_table = pd.read_csv('../../data/processed/prop_table_edit.csv', index_col = 0) #reset prop

# check element equal total for week
pred_table.sum().sum()
preds[1]


# create heatmap of pred_table
