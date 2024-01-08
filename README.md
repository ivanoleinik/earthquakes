# Earthquake Magnitude Prediction

## Table of Contents

- [Overview](#overview)
- [How to Run the Code](#how-to-run-the-code)
- [Dataset](#dataset)
  - [Feature Extraction](#feature-extraction)
- [Training](#training)
- [Gradio UI / Online Inference Pipeline](#gradio-ui--online-inference-pipeline)
- [Gradio Monitor UI / Batch Inference Pipeline](#gradio-monitor-ui--batch-inference-pipeline)


## Overview

This repository contains code for predicting earthquake magnitudes using a Histogram Gradient Boosting Regressor.

## How to Run the Code

We have divided this report such that each file in the submitted code is a standalone section in the report. 

## Dataset

The dataset for this project was sourced from [ANSS Comprehensive Earthquake Catalog](https://earthquake.usgs.gov/fdsnws/event/1/), which is updated daily. 

We backfilled with all earthquakes from the start of 2022 onwards and run a daily feature extraction pipeline using GitHub Actions, adding data to the same feature group. 

### Feature Extraction

There were several features that we deemed irrelevant including: 

- `place`, `locationSource`, `magSourse` – the information about the location is covered by latitude and longitude features.
- `nst`, `gap`, `dmin`, etc. – too many missing values

The features we added to the feature group: 
- `id` – to use as a primary key (not use in training)
- `time` – to sort the events (not used in training)
- `latitude` and `longitude` – the location of the earthquake
- `depth` and `depthError` – the depth where the earthquake begins to rupture
- `rms` – the root-mean-square travel time residual This parameter provides a measure of the fit of the observed arrival times to the predicted arrival times for this location.
- `reviewed` – whether the event has been reviewed by a human or not
- `mag` – the magnitude we are aiming to predict (target)

Additionally, we filtered out the ~2% of events which were not typed as ‘Earthquake’. This resulted in 130683 rows being kept out for training.

For the daily feature pipeline (run automatically) we copied these transformations. 

## Training

The train-test split we chose was 80-20. The model we used was Histogram Gradient Boosting Regressor. Due to our choice of model, we did not perform any statistical data transformations as they do not change the result. 
We performed a random hyperparameter search with 5-fold cross validation to find optimal values for the model parameters, finding the following configuration to be perform the best: 

- Learning_rate = 1e-3 (the default)
- L2_regularization = 1e-5
- Max_iter = 200
- Max_leaf_nodes = 51
- Min_samples_leaf = 15

The model can be retrained on demand by rerunning the training pipeline and is only reliant on feature groups. The mean squared error of the best model on the test set is 0.1362

## Gradio UI / Online Inference Pipeline

Our deployed model with which the user can interact and receive online inference results is a Gradio app on Hugging Face Space. The usage instructions are as follows:

- The user is asked to enter earthquake parameters (inputs): latitude, longitude, depth, depth_error, rms, and whether the earthquake was reviewed by a human
- The output contains the world map with the marked location of the earthquake, its magnitude, and the description according to the magnitude scale.

## Gradio Monitor UI / Batch Inference Pipeline

For inference of our model, we run a daily inference pipeline on GitHub Actions triggered by the completion of the daily feature pipeline. We take the most recent 100 records from the feature view and predict the magnitudes using our model. The outcomes of the last 5 predictions can be found in the monitor UI. 

In addition, we compare the mean squared error of the model for the recent predictions with the error of the model received during evaluation on the test set in the training pipeline. This can help to detect covariate shifts and retrain the model if needed. 
