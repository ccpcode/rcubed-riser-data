"""
Helper functions for analyzing the experimental data.
"""

import pandas as pd


def df_experiment(colname, items, files):
    """
    Create a dataframe for a group of three experiments.

    Parameters
    ----------
    colname : str
        Column name from experimental data given as pdit700 or te770 etc.
    items : tuple
        Item numbers for three experiments.
    files : list
        Data files from riser experiments.

    Note
    ----
    `item_files` are names of CSV data files which are named according to item
    number in the experiment matrix spreadsheet.
    """
    item_files = sorted([f for f in files if f.startswith(items)])
    df_items = [pd.read_csv(f'processed-hydro/{f}', usecols=['DateTime', colname]) for f in item_files]
    df = pd.concat(df_items, axis=1)
    df.columns = [f'DateTime{items[0]}', items[0], f'DateTime{items[1]}', items[1], f'DateTime{items[2]}', items[2]]
    return df


def stats(catflow, df, item):
    """
    Determine mean, standard deviation, max, and min for column in the
    dataframe.
    """
    start = df['DateTime' + item].iloc[0]
    stop_idx = df['DateTime' + item].last_valid_index()
    stop = df['DateTime' + item].iloc[stop_idx]
    dp_mean = df[item].mean()
    dp_std = df[item].std()
    dp_max = df[item].max()
    dp_min = df[item].min()
    return [start, stop, catflow, dp_mean, dp_std, dp_max, dp_min]


def config(ax, xlabel, ylabel):
    """
    Custom styles for plot in a figure. Also set x-label and y-label of figure.
    """
    ax.grid(True, color='0.9')
    ax.legend(loc='best')
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')


def config_subplot(ax, title, xlabel='', ylabel=''):
    """
    Custom styles for axes in a subplot figure. Also set the title, x-label, and
    y-label of the subplot figure.
    """
    ax.grid(True, color='0.9')
    ax.legend(loc='lower right')
    ax.set_frame_on(False)
    ax.set_title(title)
    ax.tick_params(color='0.9')
    if xlabel is not '':
        ax.set_xlabel(xlabel)
    if ylabel is not '':
        ax.set_ylabel(ylabel)
