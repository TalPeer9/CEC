def imports():
    import pandas as pd


def empty_cell():
    # your code here
    print()

def create_df():
    date_df = pd.DataFrame({'month': [1, 4, 7, 10],
                            'year': [2012, 2014, 2013, 2014],
                            'sale': [55, 40, 84, 31]})
    date_df


def define_index():
    month_date_df = date_df.set_index('month')
    month_date_df


def section_1():
    import pandas as pd
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    print(df)


def cell2():
    import numpy as np
    arr = np.array([1, 2, 3])
    print(arr)
