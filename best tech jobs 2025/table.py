import pandas as pd
import sys

def MakeTable():
    df = pd.read_csv('tech_jobs_2025.csv')
    print(df)