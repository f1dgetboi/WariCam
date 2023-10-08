import pandas as pd


def read_menu(file):
    df = pd.read_excel(file)
    dict = df.to_dict()
    return dict,len(df)
def read_foods(file):
    df = pd.read_excel(file)
    dict = df.to_dict()
    return dict,len(df)

