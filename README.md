# CRED
Causal Relation Extraction Dataset on Genes-Diseases based on biomedical literature data

We have organised this repository as: code, data, embeddings, intermediate results, pre_trained_models.

The repo contains the code files and data used in the paper : https://www.biorxiv.org/content/10.1101/2024.09.17.613424v1

The code folder contains :

-> classification_code.ipynb: This file contains the code for generating the embeddings using BioBERT model and generating the predictions. This file imports interpretation_code.py and k_fold_cv.py

-> cls_classification.ipynb: This file contains the code for generating the CLS and CLS with G-D embeddings.

-> data_augmentation.ipynb: This file contains the code for augmenting the data

-> hyperparameter_tuning.ipynb: This file contains the code for tuning the hyper-parameters for all the models

-> interpretation_code.py: This file contains the code for calculating interpretation score.

-> k_fold_cv.py: This file contains the code for 4-cross validation.

-> CRED_application_code.ipynb: This file contains the code related to applications of CRED

The data folder contains :

-> new_train_data: training data (after augmentation)

-> only_augmented_data: augmented abstracts

-> test_data: test data

-> val_data: validation data
All the annotations of the data are done by CRED developers and all the abstracts are taken from Pubtator

Intermediate results folder contains files used for generating various interpretation plots

Pre-trained models folder contains pre-trained SVM and XGBoost models trained on CRED and CDR data

# Installation
See requirements.txt file (in the code folder) for the list of dependencies. All the code is written using python language

# Getting started
After doing all the required installations, run classification_code.ipynb file. It can generate embeddings and can also take input as pre-trained embeddings. It will generate the classification results.

# Reproduction of Results Tables and  Figures
Table 2: Running table1_code.ipynb file

Table 3: Run Inter_annotator_agreement.ipynb file

Table 4: Run classification_code.ipynb

Figure 4: Run cls_classification.ipynb

Figure 5,6,7: Run interpretation_graph_new.ipynb

Figure 8,9: Run CRED_application_code.ipynb

