import pandas as pd
import numpy as np

def transform_cleaned_data(csv_data, cleaned_csv):
    
    #Read CSV
    df = pd.read_csv(csv_data)

    #Create Car_ID
    df.insert(0, 'Car_ID', df.index + 1)

    #Transform Mile to Kilometer
    df['Mileage_Mile'] =( df['Mileage_KM'] * 0.621371).round(2)

    #Add column Price_THB 
    df['Price_THB'] = df['Price_USD'] * 35

    #Manage outliers
    def cap_outliers(series):
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        return np.where(series > upper, upper,
                    np.where( series < lower, lower, series))

    df['Mileage_KM'] = cap_outliers(df['Mileage_KM'])
    df['Mileage_Mile'] = cap_outliers(df['Mileage_Mile'])
    df['Price_THB'] = cap_outliers(df['Price_THB'])
    df['Price_USD'] = cap_outliers(df['Price_USD'])
    df['Sales_Volume'] = cap_outliers(df['Sales_Volume'])

    #New features
    #Car Age
    df['Car_Age'] = 2025 - df['Year']

    #Revenue
    df['Revenue'] = df['Price_USD'] * df['Sales_Volume']

    #To csv
    df.to_csv(cleaned_csv, index=False)

