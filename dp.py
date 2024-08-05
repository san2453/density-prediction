from sklearn.utils.validation import joblib
import pandas as pd

model = joblib.load('../density_prediction.pkl')
features = model.feature_names_in_
data = {key: None for key in features}
df = pd.DataFrame(data, index=[0])

print(df)