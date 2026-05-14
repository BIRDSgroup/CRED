# CRED
Causal Relation Extraction Dataset on Genes-Diseases based on biomedical literature data

We have organised this repository as: code, data, embeddings, intermediate results, pre_trained_models.

The repo contains the code files and data used in the paper: https://www.biorxiv.org/content/10.1101/2024.09.17.613424v1

The code folder contains :

-> classification_code.ipynb: This file contains the code for generating the embeddings using the BioBERT model and generating the predictions. This file imports interpretation_code.py and k_fold_cv.py

-> cls_classification.ipynb: This file contains the code for generating the CLS and CLS with G-D embeddings.

-> data_augmentation.ipynb: This file contains the code for augmenting the data

-> hyperparameter_tuning.ipynb: This file contains the code for tuning the hyperparameters for all the models

-> interpretation_code.py: This file contains the code for calculating the interpretation score.

-> k_fold_cv.py: This file contains the code for 4-fold cross-validation.

-> CRED_application_code.ipynb: This file contains the code related to applications of CRED

The data folder contains :

-> data_description.txt: This file contains the description of rows and columns of all the dataset files

-> new_train_data: training data (after augmentation)

-> only_augmented_data: augmented abstracts

-> test_data: test data

-> val_data: validation data
All the annotations of the data are done by CRED developers, and all the abstracts are taken from Pubtator

The intermediate results folder contains files (importance scores) used for generating various interpretation plots

Pre-trained models folder contains pre-trained SVM and XGBoost models trained on CRED and CDR data

**supplementary_data** folder contains the test data analysis file 

# License Preamble
Copyright 2024 BIRDS Group, IIT Madras

MultiPopPred is a free software: you can redistribute it and modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

MultiPopPred is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Please take a look at the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with MultiPopPred. If not, see https://www.gnu.org/licenses/.


# Installation
See requirements.txt file (in the code folder) for the list of dependencies. All the code is written using python language

# Getting started
After doing all the required installations, run classification_code.ipynb file. It can generate embeddings and can also take input as pre-trained embeddings. It will generate the classification results.

# Reproduction of Results Tables and  Figures
Table 2: Running table1_code.ipynb and auprc.ipynb files

Table 3: Run Inter_annotator_agreement.ipynb file

Table 4: Run classification_code.ipynb

Figure 4: Run cls_classification.ipynb

Figure 5,6,7: Run interpretation_graph_new.ipynb

Figure 8,9: Run CRED_application_code.ipynb

