import streamlit as st
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from datetime import datetime

st.header("Bank Loan Prediction")
st.image('https://miro.medium.com/max/640/1*UC0sy0bENl-DLPy3jmXNag.jpeg')


@st.cache
def get_data():
    X = pd.read_csv("trainDataset.csv")
    X.drop('Loan_ID', axis = 1, inplace = True)

    Y = X['Loan_Status']
    X = X.drop('Loan_Status', axis=1)

    # Data Cleaning
    X['Dependents'].replace({'3+': 5}, inplace = True)
    X['Dependents'] = pd.to_numeric(X['Dependents'])
    Y = np.where(Y == 'Y', 1, 0)
    return X, Y

X, Y = get_data()

coltrans = ColumnTransformer([
      ('imputer-mod_onehot', Pipeline([
                                ('imputer-mod', SimpleImputer(strategy='most_frequent')),
                                ('onehot', OneHotEncoder(drop='first')),
                              ]), ['Gender', 'Married', 'Self_Employed']),
      ('imputer-mod', SimpleImputer(strategy='most_frequent'), ['Credit_History']),
      ('imputer-mean_scaling', Pipeline([
                                ('imputer-mean', SimpleImputer(strategy='mean')),
                                ('scaling', StandardScaler()),
                              ]), ['Dependents', 'LoanAmount', 'Loan_Amount_Term']),
      ('onehot', OneHotEncoder(drop='first'), ['Education', ]),
      ('scaling', StandardScaler(), ['ApplicantIncome', 'CoapplicantIncome', ]),
])

X = coltrans.fit_transform(X)

@st.cache
def train_model():
    model = LogisticRegression().fit(X, Y)
    return model

model = train_model()

data = {}

data['Gender'] = st.selectbox('Gender', ('Male', 'Female'))

data['Married'] = st.selectbox('Married', ('Yes', 'No'))

data['Dependents'] = st.number_input('How many people dependents on you', min_value=0)
if data['Dependents'] > 3:
    data['Dependents'] = 5

data['Education'] = st.selectbox('Are you Graduated', ('Graduate', 'Not Graduate'))
data['Self_Employed'] = st.selectbox('Bussiness', ('Yes', 'No'))
data['ApplicantIncome'] = st.number_input("Your Income", min_value=0)
data['CoapplicantIncome'] = st.number_input("Coapplicant Income", min_value=0)
data['LoanAmount'] = st.number_input("Loan Amount", min_value=0)

data['Loan_Amount_Term'] = st.number_input('Loan_Amount_Term', min_value=0)
data['Property_Area'] = st.selectbox('Property_Area', ['Rural', 'Urban', 'Semiurban'])


data['Credit_History'] = st.selectbox('Transaction Frequency', ['Good', 'Average']) # format_func
if data['Credit_History'] == 'Good':
    data['Credit_History'] = 1
else:
    data['Credit_History'] = 0


features = pd.DataFrame(data, index=[0])
st.write(features)

features = coltrans.transform(features)

pred = model.predict(features)

if pred[0] == 1:
    st.write('Congrats you will get loan')
else:
    st.write('You have very less chance of getting loan')    

