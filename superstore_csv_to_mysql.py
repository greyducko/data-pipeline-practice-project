import pandas as pd

def extract(file_path):
    extracted_data = pd.read_csv(file_path)
    return extracted_data

