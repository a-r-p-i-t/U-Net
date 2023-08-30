# Person Face Classification using U-Net Architecture

## Overview

This repository contains the code for a person face classification task using the U-Net architecture. The goal of this project is to classify different categories of person faces using annotated images, where the annotations have been divided into 7 categories. The project includes data preprocessing, annotation conversion, model training, and inference.

## Table of Contents

- [Dataset](#dataset)
- [Annotations](#annotations)
- [Data Preprocessing](#data-preprocessing)
- [Model Architecture](#model-architecture)
- [Training](#training)
- [Usage](#usage)
- [License](#license)

## Dataset

The dataset used for this project consists of person face images with associated annotations. The annotations are divided into 7 categories, each representing a different aspect of the face.

## Annotations

The original annotations were provided in JSON format. To convert these annotations into mask images, the `json_to_masks.py` script was created. The script reads the JSON annotations and generates corresponding mask images in PNG format.

## Data Preprocessing

The `data_preprocess.py` script handles the data preprocessing steps. It prepares the dataset, processes the images, and generates the required input data for model training.

## Model Architecture

The core architecture of the project is based on the U-Net model. The U-Net architecture is a convolutional neural network designed for image segmentation tasks.

## Training

The training script (`train.py`) utilizes the U-Net architecture to train a custom model on the preprocessed dataset. The model is optimized for the person face classification task using appropriate loss functions and optimizers.

## Usage

To use this project, follow these steps:

1. Clone the repository: `git clone https://github.com/yourusername/your-repo.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Preprocess the data: Run `data_preprocess.py` to prepare the dataset and generate masks.
  ![Person3](https://github.com/a-r-p-i-t/U-Net/assets/99071325/fab3f5c3-e132-43bd-87d1-8865ba5702d2)
4. Convert annotations: Run `json_to_masks.py` to convert JSON annotations to mask images.
  ![Person3_mask](https://github.com/a-r-p-i-t/U-Net/assets/99071325/7a8e65ac-eb72-48fa-856f-d64094100cef)
5. Train the model: Execute `train.py` to train the U-Net model on the preprocessed data.


