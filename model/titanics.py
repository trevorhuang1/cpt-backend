from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import seaborn as sns
import numpy as np
import pdb
import ast

# Define the TitanicRegression global variable
titanic_regression = None

# Define the TitanicRegression class
class TitanicRegression:
    def __init__(self):
        self.dt = None
        self.logreg = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.encoder = None
        self.initTitanic()  # Call initTitanic in the constructor


    def initTitanic(self):
        titanic_data = sns.load_dataset('titanic')
        self.td = titanic_data
        self.td.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
        self.td.dropna(inplace=True) # drop rows with at least one missing value, after dropping unuseful columns
        self.td['sex'] = self.td['sex'].apply(lambda x: 1 if x == 'male' else 0)
        self.td['alone'] = self.td['alone'].apply(lambda x: 1 if x == True else 0)

        # Encode categorical variables
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.encoder.fit(self.td[['embarked']])
        self.onehot = self.encoder.transform(self.td[['embarked']]).toarray()
        cols = ['embarked_' + val for val in self.encoder.categories_[0]]
        self.td[cols] = pd.DataFrame(self.onehot)
        self.td.drop(['embarked'], axis=1, inplace=True)
        self.td.dropna(inplace=True)
        print(self.td)
        # clean data



    def runDecisionTree(self):
        X = self.td.drop('survived', axis=1) # all except 'survived'
        y = self.td['survived'] # only 'survived'
        self.X_train, X_test, self.y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        dt = DecisionTreeClassifier()
        dt.fit(self.X_train, self.y_train)
        self.dt = dt
        print(export_text(dt, feature_names=X.columns.tolist()))

        # more code here

    def runLogisticRegression(self, X, y):
        # more code here
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        self.logreg = LogisticRegression()
        self.logreg.fit(self.X_train, self.y_train)
        
    def predictSurvival(self, passenger):
        X = self.td.drop('survived', axis=1) # all except 'survived'
        y = self.td['survived'] # only 'survived'
        self.X_train, X_test, self.y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                
        self.logreg = LogisticRegression()
        self.logreg.fit(self.X_train, self.y_train)
        
        passenger = list(passenger.values())
        
        passenger = pd.DataFrame({
            'name': [passenger[0]],
            'pclass': [passenger[1]],
            'sex': [passenger[2]],
            'age': [passenger[3]],
            'sibsp': [passenger[4]],
            'parch': [passenger[5]],
            'fare': [passenger[6]],
            'embarked': [passenger[7]],
            'alone': [passenger[8]]
        })
        
        passenger['sex'] = passenger['sex'].apply(lambda x: 1 if x == 'male' else 0)
        passenger['alone'] = passenger['alone'].apply(lambda x: 1 if x == True else 0)
        onehot = self.encoder.transform(passenger[['embarked']])
        cols = ['embarked_' + val for val in self.encoder.categories_[0]]
        print(passenger)
        passenger[cols] = pd.DataFrame(onehot.toarray(), index=passenger.index)
        passenger.drop(['name'], axis=1, inplace=True)
        passenger.drop(['embarked'], axis=1, inplace=True)
        
        print(passenger)
        # passenger_list = list(passenger["passenger"].values())

        # passenger = np.asarray(passenger_list).reshape(1, -1)
        # #preprocessing
    
        aliveProb = np.squeeze(self.logreg.predict_proba(passenger))
        print(aliveProb)
        aliveProb.tolist()
        deathProb = aliveProb[0]
        aliveProb = aliveProb[1]
        
        return 'Survival probability: {:.2%}'.format(aliveProb),('Death probability: {:.2%}'.format(deathProb))  


def initTitanic():
    global titanic_regression
    titanic_regression = TitanicRegression()
    titanic_regression.initTitanic()
    X = titanic_regression.td.drop('survived', axis=1)
    y = titanic_regression.td['survived']
    titanic_regression.runLogisticRegression(X, y)  #s  # Pass X and y to runLogisticRegression


# From API

# Sample usage without API