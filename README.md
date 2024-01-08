# Earthquake Magnitude Prediction

## Overview

This repository contains code for predicting earthquake magnitudes using a Histogram Gradient Boosting Regressor. The project is structured with each file representing a standalone section in the report.

## How to Run the Code

1. Clone the repository.
2. Install the required dependencies listed in the `requirements.txt` file.
3. Follow the instructions provided in each file to execute the code.

## Dataset

The dataset for this project is sourced from the ANSS Comprehensive Earthquake Catalog, updated daily. We backfilled earthquake data from the start of 2022 and run a daily feature extraction pipeline using GitHub Actions.

### Feature Extraction

We filtered irrelevant features and added the following to the feature group:

- `id`: Primary key (not used in training)
- `time`: Event timestamp (not used in training)
- `latitude` and `longitude`: Location of the earthquake
- `depth` and `depthError`: Depth where the earthquake begins to rupture
- `rms`: Root-mean-square travel time residual
- `reviewed`: Whether the event has been reviewed by a human
- `mag`: Target variable (magnitude)

We filtered out non-earthquake events, resulting in 130,683 rows for training.

## Training

The train-test split is 80-20, and the model used is a Histogram Gradient Boosting Regressor. We performed a random hyperparameter search with 5-fold cross-validation to find optimal values. The best configuration is as follows:

- Learning_rate = 1e-3 (default)
- L2_regularization = 1e-5
- Max_iter = 200
- Max_leaf_nodes = 51
- Min_samples_leaf = 15

The model can be retrained by rerunning the training pipeline. The mean squared error of the best model on the test set is 0.1362.

## Gradio UI / Online Inference Pipeline

A Gradio app on Hugging Face Space allows users to interact with the model. Instructions:

1. Enter earthquake parameters: latitude, longitude, depth, depth_error, rms, and whether the earthquake was reviewed.
2. View the output containing a world map with the marked earthquake location, magnitude, and description according to the magnitude scale.

## Gradio Monitor UI / Batch Inference Pipeline

For batch inference, a daily pipeline on GitHub Actions predicts magnitudes for the most recent 100 records. The last 5 predictions and model error comparisons are available in the monitor UI. This helps detect covariate shifts and trigger retraining if needed.
