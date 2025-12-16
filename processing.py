import pandas as pd
import pandas as pd

def analyze_columns(file_path):
    """
    Reads a CSV file and returns basic metadata about each column.
    """
    df = pd.read_csv(file_path)

    columns = []

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            col_type = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            col_type = "datetime"
        else:
            col_type = "categorical"

        columns.append({
            "name": col,
            "type": col_type,
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isna().sum()),
            "unique": int(df[col].nunique())
        })

    return columns

def process_csv(file_path):
    data = pd.read_csv(file_path)
    summary_html = data.describe(include='all').to_html(classes='table table-bordered table-striped', border=0)
    return summary_html

def readcols(file_path):
    data = pd.read_csv(file_path)
    columns = data.columns.tolist()
    return columns

def summarize(file_path, selected_column):
    data = pd.read_csv(file_path)
    summary = data[selected_column].describe().to_dict()
    return summary

def find_hidden_patterns(file_path):
    return "hello"