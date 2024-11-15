import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import json

data = pd.read_json('./data/history.json')
data['datetime_utc'] = pd.to_datetime(data['datetime_utc'], unit='ms')  # Convert milliseconds to datetime

data = data.sort_values('datetime_utc').reset_index(drop=True)

# Calculate the time difference in days between consecutive events
data['diff_days'] = data['datetime_utc'].diff().dt.total_seconds() / (24 * 3600)

diff_series = data['diff_days'].dropna()
diff_series.index = pd.date_range(start=data['datetime_utc'].iloc[1], periods=len(diff_series), freq='D')

arima_model = ARIMA(diff_series, order=(1, 1, 1))  # ARIMA with order that should handle slight trend and randomness
fitted_model = arima_model.fit()

forecast_intervals = fitted_model.forecast(steps=10)

last_event_date = data['datetime_utc'].iloc[-1]
predicted_dates = [last_event_date + pd.Timedelta(days=interval) for interval in forecast_intervals.cumsum()]

predicted_data = [
    {"datetime_utc": int(predicted_date.timestamp() * 1000), "predicted": True} 
    for predicted_date in predicted_dates
]

with open('./data/predicted.json', 'w') as f:
    json.dump(predicted_data, f, indent=4)

print("Predicted dates saved to /data/predicted.json")
