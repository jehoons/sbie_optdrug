#!/usr/bin/python
import sys 
import pandas as pd 
def df_to_markdown(df, float_format='%.2g'):
    """
    Export a pandas.DataFrame to markdown-formatted text.
    DataFrame should not contain any `|` characters.
    """
    from os import linesep
    return linesep.join([
        '|'.join(df.columns),
        '|'.join(4 * '-' for i in df.columns),
        df.to_csv(sep='|', index=False, header=False, float_format=float_format)
    ]).replace('|', ' | ')

if __name__ == '__main__':
    inputfile = sys.argv[1]
    df = pd.read_csv(inputfile)
    print df_to_markdown(df)

    