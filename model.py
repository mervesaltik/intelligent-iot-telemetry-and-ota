import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
import pickle

# CSV read
df = pd.read_csv('output22.csv')  # CSV file write

print(df.info())

# Only take good and bad label
df = df[df['label'].isin(['good', 'bad'])]
print(df.head())

# Fill in missing values
df = df.fillna(df.mean(numeric_only=True))
df = df.replace([np.inf, -np.inf], np.nan)
df = df.fillna(df.mean(numeric_only=True))

# Calculate performance differences
df['cpu_diff'] = df['cpu_after'] - df['cpu_before']
df['disk_diff'] = df['disk_after'] - df['disk_before']
df['network_recv_diff'] = df['network_recv_after'] - df['network_recv_before']
df['network_sent_diff'] = df['network_sent_after'] - df['network_sent_before']
df['ram_diff'] = df['ram_after'] - df['ram_before']

# Features and target setting
X = df[['cpu_diff', 'disk_diff', 'network_recv_diff', 'network_sent_diff', 'ram_diff']]
y = df['label']

# Split the dataset into training and test data
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# Use SMOTE to fix data imbalance
smote = SMOTE(random_state=42)
x_train_balanced, y_train_balanced = smote.fit_resample(x_train, y_train)


scaler = StandardScaler()

# Scale training and test sets
x_train_scaled = scaler.fit_transform(x_train_balanced)
x_test_scaled = scaler.transform(x_test)

# Models
# Set parameters for RandomForest
rf_params = {
    "n_estimators": [50, 100, 150],
    "max_depth": [None, 5, 10, 20]
}

grid_rf = GridSearchCV(RandomForestClassifier(random_state=42), rf_params, cv=5, scoring='accuracy')
grid_rf.fit(x_train_scaled, y_train_balanced)
best_rf = grid_rf.best_estimator_

print("RandomForest best parameters:", grid_rf.best_params_)

# Setting parameters for KNN
knn_params = {
    "n_neighbors": [3, 5, 7, 9],
    "weights": ['uniform', 'distance']
}

grid_knn = GridSearchCV(KNeighborsClassifier(), knn_params, cv=5, scoring='accuracy')
grid_knn.fit(x_train_scaled, y_train_balanced)
best_knn = grid_knn.best_estimator_

print("KNN best parameters:", grid_knn.best_params_)

# Creating an ensemble model with soft voting
voting_clf = VotingClassifier(estimators=[("rf", best_rf), ("knn", best_knn)], voting="soft")

# Model train
voting_clf.fit(x_train_scaled, y_train_balanced)

# prediction
y_pred = voting_clf.predict(x_test_scaled)

# results
print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred, labels=['bad', 'good'])
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, labels=['bad', 'good'], target_names=['bad', 'good']))

# result show
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=['bad', 'good'], yticklabels=['bad', 'good'])
plt.title("Confusion Matrix")
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()

# 14. Scatter Plot
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='cpu_diff', y='ram_diff', hue='label', palette='Set1')
plt.title('CPU Difference vs RAM Difference')
plt.xlabel('CPU Difference')
plt.ylabel('RAM Difference')
plt.legend(title='Label')
plt.show()

# Modeli save
with open('model.pkl', 'wb') as f:
    pickle.dump(voting_clf, f)

# prediction function of model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def make_prediction(cpu, disk, network_recv, network_sent, ram):
    data = [[cpu, disk, network_recv, network_sent, ram]]
    prediction = model.predict(data)
    return prediction[0]
