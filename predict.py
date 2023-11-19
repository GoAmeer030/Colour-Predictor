from joblib import load

model = load('model.joblib')

value_to_predict = input('Enter a value to predict: ')

print(model.predict([[value_to_predict]]))