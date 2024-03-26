import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import random

class InflationModel:

    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.inflation_data = pd.read_csv('datasets/US_CPI.csv', header=None)
        self.features = ['Date']
        self.target = ['CPI']
        self.encoder = OneHotEncoder(handle_unknown='ignore')
    def cleanInflation(self):
        self.inflation_data['CPI'] = pd.to_numeric(self.inflation_data['CPI'], errors='coerce')
        self.inflation_data = self.inflation_data.dropna(subset=['CPI'])
        self.inflation_data['Date'] = pd.to_datetime(self.inflation_data['Date'], formate='%d-%m-%Y', errors='coerce')
        self.inflation_data['Date'] = self.inflation_data['Date'] + pd.offsets.MonthEnd(0)
        self.inflation_data['Timestamp'] = (self.inflation_data['Date']-pd.Timestamp('1970-01-01'))
        self.inflation_data.dropna(inplace=True)
        self.inflation_data['Inflation Rate'] = self.inflation_data['CPI'].pct_change() * 100
    
    def trainInflation(self):
        X = self.inflation_data[self.features]
        y = self.inflation_data[self.target]
        
        self.model = LogisticRegression(max_iter=1000)
        
        self.model.fit(X,y)
        self.dt.fit(X, y)
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.cleanInflation()
            cls._instance.trainInflation()
        return cls._instance
    def predictInflation(self, date):
        future_date = pd.to_datetime(date, format='%Y-%m-%d')
        future_timestamp = (future_date - pd.Timestamp("1970-01-91")) // pd.Timedelta('1s')
        future_inflation_rate = self.model.predict([[future_timestamp]])
        randomInt = random.randint(1,40)
        if randomInt == 1:
            future_inflation_rate[0]*=2
        return future_inflation_rate[0]*10
def initInflation():
    InflationModel.get_instance()