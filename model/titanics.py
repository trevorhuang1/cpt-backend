from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import seaborn as sns
import numpy as np

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

    def initTitanic(self):
        titanic_data = sns.load_dataset('titanic')
        self.td = titanic_data
        self.td.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
        self.td.dropna(inplace=True) # drop rows with at least one missing value, after dropping unuseful columns
        self.td['sex'] = self.td['sex'].apply(lambda x: 1 if x == 'male' else 0)
        self.td['alone'] = self.td['alone'].apply(lambda x: 1 if x == True else 0)

        # Encode categorical variables
        self.enc = OneHotEncoder(handle_unknown='ignore')
        self.enc.fit(self.td[['embarked']])
        self.onehot = self.enc.transform(self.td[['embarked']]).toarray()
        cols = ['embarked_' + val for val in self.enc.categories_[0]]
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

    def runLogisticRegression(self):
        # more code here
        self.logreg = LogisticRegression()
        self.logreg.fit(self.X_train, self.y_train)

def initTitanic():
    global titanic_regression
    titanic_regression = TitanicRegression()
    titanic_regression.initTitanic()

# From API
def predictSurvival(self,passenger):
    new_passenger = passenger.copy()
    # Preprocess the new passenger data
    new_passenger['sex'] = new_passenger['sex'].apply(lambda x: 1 if x == 'male' else 0)
    new_passenger['alone'] = new_passenger['alone'].apply(lambda x: 1 if x == True else 0)

    # Encode 'embarked' variable
    self.onehot = self.enc.transform(new_passenger[['embarked']]).toarray()
    cols = ['embarked_' + val for val in self.enc.categories_[0]]
    new_passenger[cols] = pd.DataFrame(self.onehot, index=new_passenger.index)
    new_passenger.drop(['name'], axis=1, inplace=True)
    new_passenger.drop(['embarked'], axis=1, inplace=True)
    aliveProb = np.squeeze(self.logreg.predict_proba(new_passenger))

    # more code here
    # interact with 
    return aliveProb
# Sample usage without API
if __name__ == "__main__":
    # Initialize the Titanic model
    initTitanic()