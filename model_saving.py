import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from catboost import CatBoostClassifier
from sklearn.neural_network import MLPClassifier
import pickle

data = pd.read_csv('data/balanced_diabetes_data.csv', encoding='utf-8', delimiter=',')
data.drop(['Unnamed: 0'], axis=1, inplace=True)

bX = data.drop('Diabetes_012', axis=1)
by = data['Diabetes_012']

X_ho_train, X_ho_test, y_ho_train, y_ho_test = train_test_split(bX, by, test_size=0.2, random_state=42, stratify=by)

# knn = KNeighborsClassifier(n_neighbors=14, metric='manhattan')
# knn.fit(X_ho_train, y_ho_train)
#
# with open('models/knn_model.pkl', 'wb') as file:
#     pickle.dump(knn, file)
#
# ctree = DecisionTreeClassifier(max_depth=None)
# c_bagging_model = BaggingClassifier(ctree, n_estimators=9, max_samples=1.0, bootstrap=True, random_state=42)
#
# c_bagging_model.fit(X_ho_train, y_ho_train)
#
# with open('models/bagging_model.pkl', 'wb') as file:
#     pickle.dump(c_bagging_model, file)
#
# gbc = GradientBoostingClassifier(n_estimators=12,
#                                  learning_rate=0.05,
#                                  random_state=100,
#                                  max_features=5,
#                                  min_samples_split=4,
#                                  min_samples_leaf=4,
#                                  max_depth=10,
#                                  loss='log_loss')
#
# gbc.fit(X_ho_train, y_ho_train)
#
# with open('models/boosting_model.pkl', 'wb') as file:
#     pickle.dump(gbc, file)
#
# pred_y = gbc.predict(X_ho_test)
#
# acc = accuracy_score(y_ho_test, pred_y)
# print("Gradient Boosting Classifier accuracy is : {:.2f}".format(acc))
#
# base_models = [
#     ('knn1', KNeighborsClassifier(n_neighbors=4)),
#     ('dt', DecisionTreeClassifier(max_depth=3)),
#     ('knn2', KNeighborsClassifier(n_neighbors=2))
# ]
#
# stacking_model = StackingClassifier(estimators=base_models, final_estimator=LogisticRegression())
# stacking_model.fit(X_ho_train[:10000], y_ho_train[:10000])
#
# with open('models/stacking_model.pkl', 'wb') as file:
#     pickle.dump(stacking_model, file)
#
# y_pred_stacking = stacking_model.predict(X_ho_test)
#
# accuracy_stacking = accuracy_score(y_ho_test, y_pred_stacking)
# print(f'Stacking Test Accuracy: {accuracy_stacking:.2f}')

cat_model = CatBoostClassifier(verbose=0)
cat_model.fit(X_ho_train, y_ho_train)
cat_model.save_model("models/catboost_model.cbm")

# mlp = MLPClassifier(hidden_layer_sizes=(50, 25), activation='relu', solver='adam', max_iter=100, random_state=42)
#
# mlp.fit(X_ho_train[:50000], y_ho_train[:50000])
#
# with open('models/fcnn_model.pkl', 'wb') as file:
#     pickle.dump(mlp, file)