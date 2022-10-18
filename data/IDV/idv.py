import pickle

idv = pickle.load(open('data/IDV/IDV.pkl', 'rb')).sort_values('TRADE_DT')