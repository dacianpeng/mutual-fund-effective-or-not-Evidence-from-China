import pickle

fees = pickle.load(open('data/TwoStepData/fees.pkl', 'rb'))
fees = fees.unstack().T.resample('M').last().ffill().stack().swaplevel()
fees.name = 'fees'