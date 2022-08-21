import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


plt.style.use('fivethirtyeight')
pd.set_option('display.max_columns', 500)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]

from fredapi import Fred

fred_key = 'ENTER_YOUR_KEY_HERE'

# 1. Create the Fred Object
fred = Fred(api_key=fred_key)

# 2. Search for economic data!
sp_search = fred.search('S&P', order_by='popularity')
sp_search.head()

# 3. Pull Raw Data
sp500 = fred.get_series(series_id='SP500')

sp500.plot(figsize=(10, 5), title='S&P 500', lw=2)

# 4. Pull and Join Multiple Data Series
nc_metrics_results_df = fred.search('unemployment NC', filter=('frequency','Monthly'), order_by='popularity')
nc_metrics_results_df = nc_metrics_results_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')
nc_metrics_results_df = nc_metrics_results_df.loc[nc_metrics_results_df['title'].str.contains('Rate')]


# 5. Loop through and concatenate the data
all_results = []

for myid in nc_metrics_results_df.index:
    results = fred.get_series(series_id=myid)
    results = results.to_frame(name=myid)
    all_results.append(results)
nc_metric_results = pd.concat(all_results, axis=1)
nc_metric_results = nc_metric_results.dropna()

# 6. Plot NC Labor Force Participation and Unemployment Rates
px.line(nc_metric_results)

nc_metric_results.loc[nc_metric_results.index == '2020-04-01']

nc_unemp_rate = fred.get_series(series_id='NCUR')
nc_unemp_rate.plot(figsize=(10, 5), title='NC Unemployment Rate', lw=2)

nc_labor_force_rate = fred.get_series(series_id='LBSSA37')
nc_labor_force_rate.plot(figsize=(10, 5), title='NC Labor Force Rate', lw=2)
