import pandas as pd

def process_csv(file_path):
    data = pd.read_csv(file_path)
    summary_html = data.describe(include='all').to_html(classes='table table-bordered table-striped', border=0)
    return summary_html