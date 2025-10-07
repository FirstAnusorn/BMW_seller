import pandas as pd

def extract_features(csv_raw_data):
    df = pd.read_csv(csv_raw_data)

    print('Original Data')
    print(df.head(),'\n')
    print('-' * 30)

    print('Number of structure')
    print(df.shape), '\n'
    print('-' * 30)

    print('Information for data')
    print(df.info(), '\n')
    print('-' * 30)

    print('Number missing values')
    df_missing = df.isnull().sum()
    print(df_missing, '\n')
    print('-' * 30)

    df_duplicate = df.duplicated().sum()
    print(f'Number duplicate column is : {df_duplicate}')
    print('-' * 30)

    print('Data type :')
    print(df.dtypes)