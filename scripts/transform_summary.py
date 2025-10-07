import pandas as pd

def transform_summary_data(cleaned_csv, summary_csv):
    #Read cleaned CSV
    df = pd.read_csv(cleaned_csv)
    
    #Group by Region, Fuel_Type, Year and aggregate
    df_summary = (
        df.groupby(['Region', 'Fuel_Type', 'Year']).agg(
            Total_Sales_Volume = ('Sales_Volume', 'sum'),
            Total_Revenue_Billion_USD = ('Revenue', 'sum'),
            Average_Price_USD = ('Price_USD', 'mean')
        ).reset_index()).round(2)
    
    #Adjust Total_Revenue to Billion USD and add Summary_ID, Car_ID
    df_summary['Total_Revenue_Billion_USD'] = (df_summary['Total_Revenue_Billion_USD'] / 1e9).round(2)
    df_summary.insert(0, 'Summary_ID', df_summary.index + 1)
    df_summary.insert(1, 'Car_ID', df_summary.index + 1)
    
    #To csv
    df_summary.to_csv(summary_csv, index=False)