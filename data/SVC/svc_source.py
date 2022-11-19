import pickle
import pandas as pd

# svc_source = pickle.load(open('data/SVC/CH3_Monthly.pkl', 'rb'))
# svc_source['Date'] = pd.to_datetime(svc_source[['year', 'month']].assign(day=1)).dt.to_period('M')
# svc_source = svc_source.set_index('Date')

svc_source = pickle.load(open('data/SVC/SVC_SOURCE.pkl', 'rb'))
