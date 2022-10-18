
from data.CSMAR.daily_nav import csmar_nav_daily

csmar_nav_monthly = csmar_nav_daily.groupby('Symbol').apply(lambda x: x.set_index('Date').resample('M').last()).NAV
csmar_nav_monthly = csmar_nav_monthly.unstack(level=0)
csmar_nav_monthly.index = csmar_nav_monthly.index.to_period('M')
csmar_nav_monthly.columns = csmar_nav_monthly.columns.astype(str).str.zfill(6)

csmar_nav_monthly.to_pickle(open('data/TwoStepData/csmar_nav_monthly.pkl', 'wb'))
