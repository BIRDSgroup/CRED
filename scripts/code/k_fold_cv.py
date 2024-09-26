# Code to apply 4-crossfold cross-validation

from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import numpy as np
import pandas as pd

def k_fold(train_df, test_df, get_specific_token_embeddings):
    # Combine train_df and test_df
    combined_df = pd.concat([train_df, test_df], axis=0).reset_index(drop=True)
    combined_df=combined_df.rename({"index":"PMID"}, axis=1)


    # Create embeddings for the combined dataframe
    combined_embeddings = np.vstack([get_specific_token_embeddings(sentence) for sentence in combined_df['sentence']])

    # Get unique IDs
    unique_ids = combined_df['PMID'].unique()

    # Apply 4-fold cross-validation on unique IDs
    kf = KFold(n_splits=4, shuffle=True, random_state=42)

    file_name = "cross_val_classification_report_new.txt"

    # Placeholder for storing probabilities and true labels
    all_probabilities = []
    all_true_labels = []
    count=1
    for train_ids, test_ids in kf.split(unique_ids):
        train_ids = [unique_ids[i] for i in train_ids]
        test_ids = [unique_ids[i] for i in test_ids]

        train_idx = combined_df[combined_df['PMID'].isin(train_ids)].index
        test_idx = combined_df[combined_df['PMID'].isin(test_ids)].index

        X_train_fold = combined_embeddings[train_idx]
        #print(X_train_fold)
        y_train_fold = combined_df['label'].iloc[train_idx].tolist()

        X_test_fold = combined_embeddings[test_idx]
        y_test_fold = combined_df['label'].iloc[test_idx].tolist()

        clf = SVC(kernel='poly', degree=20, probability=True, class_weight={0:1, 1:30})
        clf.fit(X_train_fold, y_train_fold)

        # Predict and Evaluate
        y_pred = clf.predict(X_test_fold)

        # Get probabilities
        y_prob = clf.predict_proba(X_test_fold)

        # Append to placeholder lists
        all_probabilities.extend(y_prob)
        all_true_labels.extend(y_test_fold)

        # Print classification report for the current fold
        print(f"Classification report for fold {count}:\n")
        clf_report = classification_report(y_test_fold, y_pred)


        # Writing the report to the file
        with open(file_name, 'a') as file:
            file.write(clf_report)

        print(clf_report)
        count+=1

    # Convert to a DataFrame and save probabilities
    df = pd.DataFrame(all_probabilities, columns=['Probability_Class_0', 'Probability_Class_1'])
    df.to_csv('biobert_svm_probabilities_cv.csv', index=False)
