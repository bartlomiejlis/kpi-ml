# kpi-ml
Company turnover percentage forecast using ARMA, ARIMA and SARIMAX models.

The aim of the project is to train a model to predict the percentage of the company's turnover. The company's turnover percentage is the ratio of subcontractors' costs to the company's net turnover expressed as a percentage.

Three time series models were selected for the project: ARMA, ARIMA and SARIMAX, due to the sequential nature of the data.

The data is located in an Excel file whose sheets have been divided into individual months.

## Table of Contents
* [Features](#features)
* [Authors](#authors)

## Features
- automatic training of many models simultaneously using model_generator function
- saving models with low root mean square error to a file and then removing all models except the one with the best result
- the processing of data used for machine learning has been saved in a separate file, which is imported into the remaining model files

## Authors
Created by Bartłomiej Lis - feel free to contact me at lisu.b117@gmail.com!
