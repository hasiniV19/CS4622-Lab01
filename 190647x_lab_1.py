# -*- coding: utf-8 -*-
"""190647X_Lab_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dGKCOvNXgg6dURpkqYTa9evzM4kcUR3A

# Load data set and initialize variables
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

train_file_path = "/content/drive/MyDrive/Machine Learning Lab 1/train.csv"
valid_file_path = "/content/drive/MyDrive/Machine Learning Lab 1/valid.csv"
test_file_path = "/content/drive/MyDrive/Machine Learning Lab 1/test.csv"

train = pd.read_csv(train_file_path)
valid = pd.read_csv(valid_file_path)
test = pd.read_csv(test_file_path)

LABELS = ["label_1", "label_2", "label_3", "label_4"]
FEATURES = [column for column in train.columns if column not in LABELS]

"""# Standardization"""

from sklearn.preprocessing import StandardScaler

X_train = {}
X_valid = {}
y_train = {}
y_valid = {}
X_test = {}

for label in LABELS:
  train_df = train[train['label_2'].notna()] if label == 'label_2' else train
  valid_df = valid[valid['label_2'].notna()] if label == 'label_2' else valid
  test_df = test

  scaler = StandardScaler()
  X_train[label] = pd.DataFrame(scaler.fit_transform(train_df.drop(LABELS, axis=1)), columns=FEATURES)
  y_train[label] = train_df[label]
  X_valid[label] = pd.DataFrame(scaler.transform(valid_df.drop(LABELS, axis=1)), columns=FEATURES)
  y_valid[label] = valid_df[label]
  X_test[label]  = pd.DataFrame(scaler.transform(test_df.drop(LABELS, axis=1)), columns=FEATURES)

y_pred_before = {}
y_pred_after = {}

"""# Label 1

## Model before feature engineering
"""

from sklearn import svm

classifier = svm.SVC(kernel='linear')
classifier.fit(X_train["label_1"], y_train["label_1"])

from sklearn import metrics

y_pred = classifier.predict(X_valid["label_1"])
y_pred_before["label_1"] = classifier.predict(X_test["label_1"])

print(metrics.confusion_matrix(y_valid["label_1"], y_pred))

print("Accuracy score: ", metrics.accuracy_score(y_valid["label_1"], y_pred))
print("Precision score: ", metrics.precision_score(y_valid["label_1"], y_pred, average='weighted'))
print("Recall score: ", metrics.recall_score(y_valid["label_1"], y_pred, average='weighted'))

"""# Correlation"""

from sklearn.feature_selection import VarianceThreshold

train_removed_corr = {}
valid_removed_corr = {}
test_removed_corr = {}

for label in LABELS:

  num_colums = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
  numerical_columns = list(X_train[label].select_dtypes(include=num_colums).columns)
  X_train_numeric = X_train[label][numerical_columns] # only numeric data

  X_train_numeric.shape

  correlated_features = set()
  correlation_matrix = X_train_numeric.corr()

  for i in range(len(correlation_matrix.columns)):
      for j in range(i):
          if abs(correlation_matrix.iloc[i, j]) > 0.5:
              colname = correlation_matrix.columns[i]
              correlated_features.add(colname)

  train_removed_corr[label] = X_train[label].drop(columns=list(correlated_features))
  valid_removed_corr[label] = X_valid[label].drop(columns=list(correlated_features))
  test_removed_corr[label] = X_test[label].drop(columns=list(correlated_features))

"""# PCA"""

from sklearn.decomposition import PCA

X_train_df = {}
X_valid_df = {}
X_test_df = {}

for label in LABELS:
  pca = PCA(n_components=0.95, svd_solver='full')
  pca.fit(train_removed_corr[label])
  X_train_df[label] = pd.DataFrame(pca.transform(train_removed_corr[label]))
  X_valid_df[label] = pd.DataFrame(pca.transform(valid_removed_corr[label]))
  X_test_df[label] = pd.DataFrame(pca.transform(test_removed_corr[label]))
  print("Shape after PCA: ", X_train_df[label].shape)

"""# Plot variance"""

explained_variance = pca.explained_variance_ratio_

len_retained_features = len(explained_variance)
print(len_retained_features, " of components for training data")

import matplotlib.pyplot as plt
import numpy as np

plt.bar(range(1, len(explained_variance)+1), explained_variance)

plt.plot(range(1, len(explained_variance)+1), np.cumsum(explained_variance),
         c='red', label='Cumulative Explained Variance')

plt.legend(loc='upper left')
plt.xlabel('Number of componenets')
plt.ylabel('Explained Variance')
plt.title('Plot')

plt.show()

"""# Label 1

## K Neighbors Classification
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(np.array(X_train_df["label_1"]), y_train["label_1"])

y_pred = knn.predict(np.array(X_valid_df["label_1"]))

accuracy = accuracy_score(y_valid["label_1"], y_pred)
print("Accuracy score: ", accuracy)

y_pred_after["label_1"] = knn.predict(np.array(X_test_df["label_1"]))

"""# Label 2

## Model before feature engineering
"""

from sklearn import svm
from sklearn import metrics


classifier = svm.SVC(kernel='linear')
classifier.fit(X_train["label_2"], y_train["label_2"])


y_pred = classifier.predict(X_valid["label_2"])
y_pred_before["label_2"] = classifier.predict(X_test["label_2"])

print(metrics.confusion_matrix(y_valid["label_2"], y_pred))
print("Accuracy score: ", metrics.accuracy_score(y_valid["label_2"], y_pred))
print("Precision score: ", metrics.precision_score(y_valid["label_2"], y_pred, average='weighted'))
print("Recall score: ", metrics.recall_score(y_valid["label_2"], y_pred, average='weighted'))

"""## K Neighbors Classification"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(np.array(X_train_df["label_2"]), y_train["label_2"])

y_pred = knn.predict(np.array(X_valid_df["label_2"]))

accuracy = accuracy_score(y_valid["label_2"], y_pred)
print("Accuracy score: ", accuracy)

y_pred_after["label_2"] = knn.predict(np.array(X_test_df["label_2"]))

"""# Label 3

## Model before feature engineering
"""

from sklearn import svm
from sklearn import metrics


classifier = svm.SVC(kernel='linear')
classifier.fit(X_train["label_3"], y_train["label_3"])


y_pred = classifier.predict(X_valid["label_3"])
y_pred_before["label_3"] = classifier.predict(X_test["label_3"])
print(metrics.confusion_matrix(y_valid["label_3"], y_pred))
print("Accuracy score: ", metrics.accuracy_score(y_valid["label_3"], y_pred))
print("Precision score: ", metrics.precision_score(y_valid["label_3"], y_pred, average='weighted'))
print("Recall score: ", metrics.recall_score(y_valid["label_3"], y_pred, average='weighted'))

"""## K Neighbors Classification"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(np.array(X_train_df["label_3"]), y_train["label_3"])

y_pred = knn.predict(np.array(X_valid_df["label_3"]))

accuracy = accuracy_score(y_valid["label_3"], y_pred)
print("Accuracy score: ", accuracy)

y_pred_after["label_3"] = knn.predict(np.array(X_test_df["label_3"]))

"""# Label 4

## Model before feature engineering
"""

from sklearn import svm
from sklearn import metrics


classifier = svm.SVC(kernel='linear')
classifier.fit(X_train["label_4"], y_train["label_4"])


y_pred = classifier.predict(X_valid["label_4"])
y_pred_before["label_4"] = classifier.predict(X_test["label_4"])
print(metrics.confusion_matrix(y_valid["label_4"], y_pred))
print("Accuracy score: ", metrics.accuracy_score(y_valid["label_4"], y_pred))
print("Precision score: ", metrics.precision_score(y_valid["label_4"], y_pred, average='weighted'))
print("Recall score: ", metrics.recall_score(y_valid["label_4"], y_pred, average='weighted'))

"""## K Neighbors Classification"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(np.array(X_train_df["label_4"]), y_train["label_4"])

y_pred = knn.predict(np.array(X_valid_df["label_4"]))

accuracy = accuracy_score(y_valid["label_4"], y_pred)
print("Accuracy score: ", accuracy)

y_pred_after["label_4"] = knn.predict(np.array(X_test_df["label_4"]))

print(X_train_df["label_4"])

"""# Write to CSV files"""

path = "/content/drive/MyDrive/Machine Learning Lab 1/190647X_"

for label in LABELS:
  csv_file_path = path + label + ".csv"
  num_features = len(X_train_df[label].columns)
  num_rows = len(X_test_df[label])
  no_features_arr = [num_features]*num_rows

  data = {
      "Predicted labels before feature engineering": y_pred_before[label],
      "Predicted labels after feature engineering": y_pred_after[label],
      "No of new features": no_features_arr
  }

  print(len(y_pred_before[label]))
  print(len(y_pred_after[label]))
  print(len(no_features_arr))
  for i in range(num_features):
    column_name = "new_feature_" + str(i+1)
    data[column_name] = X_test_df[label][i]


  data_df = pd.DataFrame.from_dict(data)

  for i in range(data_df['No of new features'][0], 256):
    data_df[f'new_feature_{i+1}'] = [""] * (data_df.shape[0])

  data_df.to_csv(csv_file_path, index=False)