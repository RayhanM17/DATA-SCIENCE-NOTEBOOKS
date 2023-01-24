import pandas as pd

declarations = pd.read_csv(
    'gatorcain_data/declarations_clean_data.csv'
)
declarations['declarationDate'] = pd.to_datetime(declarations['declarationDate'])

print(declarations.head())
