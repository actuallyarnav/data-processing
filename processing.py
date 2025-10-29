import pandas as pd

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