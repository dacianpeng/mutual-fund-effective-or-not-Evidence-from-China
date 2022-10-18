
import pandas as pd



wind_validate_share_nav = pd.read_excel('data/Wind/wind_validate_share_nav.xlsx', sheet_name='Sheet1')
wind_fund_classification = wind_validate_share_nav[['证券代码', '投资类型(一级分类)']]
wind_validate_share_nav = pd.DataFrame(data=wind_validate_share_nav.iloc[:, 3:].values, index=wind_validate_share_nav.证券代码.values, \
    columns = pd.MultiIndex.from_tuples(list(map(lambda x: (x[:4], pd.to_datetime(x[12:22])), wind_validate_share_nav.columns[3:])))).T.sort_index()
wind_validate_share_nav.index = wind_validate_share_nav.index.set_levels(wind_validate_share_nav.index.levels[1].to_period('M'), level=1)