import pandas as pd

def find_column_ignore_case(df: pd.DataFrame, column_name: str) -> pd.Series:
    """
    Returns a column in a dataframe regardless of case

    Parameters:
        df (pd.DataFrame): dataframe from which to pull column
        column_name (str): name of column to retrun
    
    """
    column = [col for col in [column_name.capitalize(), column_name] if col in df.columns][0]
    return df[column]
