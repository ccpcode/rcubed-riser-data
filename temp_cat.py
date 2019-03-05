"""
Compare temperature readings in the R-cubed riser for different catalyst flow
rates. Run this program for each low, mid, and high process gas flow.

Examples
--------

First argument denoted as low, mid, or high for process gas flow. Second
argument for temperature as te709c, te709b, te709a, te707c, te707b, te707a,
te705, or te701.

>>> python temp_cat.py low te709c
>>> python temp_cat.py mid te709c
>>> python temp_cat.py high te705
"""

import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd
from utils import df_experiment, stats, config, config_subplot

# Command line argument
# ----------------------------------------------------------------------------

# input low, mid, or high for process gas experiments
parser = argparse.ArgumentParser()
parser.add_argument('pg', help='process gas group as low, mid, high')
parser.add_argument('col', help='column name as TE709C, TE705 etc.')
args = parser.parse_args()
n = ('low', 'mid', 'high').index(args.pg)
col = args.col.upper()

# Parameters for process gas flow experiments
# ----------------------------------------------------------------------------

# experiments are referred to as the item numbers in the experimental matrix
# each experiment was repeated three times
# items = | low gas flow | mid gas flow | high gas flow |
nocat_items = ('001', '005', '009'), ('013', '017', '021'), ('025', '029', '033')
lowcat_items = ('002', '006', '010'), ('014', '018', '022'), ('026', '030', '034')
midcat_items = ('003', '007', '011'), ('015', '019', '023'), ('027', '031', '035')
hicat_items = ('004', '008', '012'), ('016', '020', '024'), ('028', '032', '036')

# catalyst flow rates as reported for each experiment [kg/hr]
# cat. flows for third experiment in mid gas were not reported so assume values
# items = | low gas flow | mid gas flow | high gas flow |
lowcat = (46.8, 49.5, 44.3), (45.8, 45.1, 47.3), (53.2, 46.9, 56.5)
midcat = (91.3, 95.3, 91.6), (89.2, 95.1, 94.6), (102.2, 98.4, 97.1)
hicat = (137.6, 136.5, 141.7), (131.8, 138.2, 141.3), (140.1, 140.9, 144.8)

# Analyze process gas flow data from thermocouple TE709C
# ----------------------------------------------------------------------------

h19_files = [f for f in os.listdir('processed-hydro') if f.endswith('h19.csv')]

df_nocat = df_experiment(col, nocat_items[n], h19_files)
df_lowcat = df_experiment(col, lowcat_items[n], h19_files)
df_midcat = df_experiment(col, midcat_items[n], h19_files)
df_hicat = df_experiment(col, hicat_items[n], h19_files)

# stats from experimental data
df_stats = pd.DataFrame(columns=['start', 'stop', 'catflow', 'mean', 'std', 'max', 'min'])

for i in nocat_items[n]:
    row = stats(0, df_nocat, i)
    df_stats.loc[i] = row

for idx, i in enumerate(lowcat_items[n]):
    row = stats(lowcat[n][idx], df_lowcat, i)
    df_stats.loc[i] = row

for idx, i in enumerate(midcat_items[n]):
    row = stats(midcat[n][idx], df_midcat, i)
    df_stats.loc[i] = row

for idx, i in enumerate(hicat_items[n]):
    row = stats(hicat[n][idx], df_hicat, i)
    df_stats.loc[i] = row

df_stats['catflow'] = df_stats['catflow'].apply(pd.to_numeric)

# Plot
# ----------------------------------------------------------------------------

plt.close('all')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(9.4, 4.8), sharex='col')

for i in nocat_items[n]:
    ax1.plot(df_nocat[i].dropna(), label=f'{i}')
config_subplot(ax1, 'No catalyst', ylabel='Temperature [K]')

for i in lowcat_items[n]:
    ax2.plot(df_lowcat[i].dropna(), label=f'{i}')
config_subplot(ax2, 'Low catalyst flow')

for i in midcat_items[n]:
    ax3.plot(df_midcat[i].dropna(), label=f'{i}')
config_subplot(ax3, 'Mid catalyst flow', xlabel='Measurement [-]', ylabel='Temperature [K]')

for i in hicat_items[n]:
    ax4.plot(df_hicat[i].dropna(), label=f'{i}')
config_subplot(ax4, 'High catalyst flow', xlabel='Measurement [-]')
plt.tight_layout()

fig, ax = plt.subplots(tight_layout=True)
ax.plot(df_stats.loc[nocat_items[n], 'catflow'], df_stats.loc[nocat_items[n], 'mean'], 'oC0', label='mean')
ax.plot(df_stats.loc[lowcat_items[n], 'catflow'], df_stats.loc[lowcat_items[n], 'mean'], 'oC0', label='_nolegend_')
ax.plot(df_stats.loc[midcat_items[n], 'catflow'], df_stats.loc[midcat_items[n], 'mean'], 'oC0', label='_nolegend_')
ax.plot(df_stats.loc[hicat_items[n], 'catflow'], df_stats.loc[hicat_items[n], 'mean'], 'oC0', label='_nolegend_')
ax.plot(df_stats.loc[nocat_items[n], 'catflow'], df_stats.loc[nocat_items[n], 'max'], '.C1', label='max')
ax.plot(df_stats.loc[lowcat_items[n], 'catflow'], df_stats.loc[lowcat_items[n], 'max'], '.C1', label='_nolegend_')
ax.plot(df_stats.loc[midcat_items[n], 'catflow'], df_stats.loc[midcat_items[n], 'max'], '.C1', label='_nolegend_')
ax.plot(df_stats.loc[hicat_items[n], 'catflow'], df_stats.loc[hicat_items[n], 'max'], '.C1', label='_nolegend_')
ax.plot(df_stats.loc[nocat_items[n], 'catflow'], df_stats.loc[nocat_items[n], 'min'], '.C2', label='min')
ax.plot(df_stats.loc[lowcat_items[n], 'catflow'], df_stats.loc[lowcat_items[n], 'min'], '.C2', label='_nolegend_')
ax.plot(df_stats.loc[midcat_items[n], 'catflow'], df_stats.loc[midcat_items[n], 'min'], '.C2', label='_nolegend_')
ax.plot(df_stats.loc[hicat_items[n], 'catflow'], df_stats.loc[hicat_items[n], 'min'], '.C2', label='_nolegend_')
ax.xaxis.set_ticks([0, 45, 91, 136])
ax.fill_between(df_stats['catflow'][::3], df_stats['min'][::3], df_stats['max'][::3], alpha=0.5, facecolor='lightgrey')
ax.fill_between(df_stats['catflow'][1::3], df_stats['min'][1::3], df_stats['max'][1::3], alpha=0.5, facecolor='lightgrey')
ax.fill_between(df_stats['catflow'][2::3], df_stats['min'][2::3], df_stats['max'][2::3], alpha=0.5, facecolor='lightgrey')
config(ax, 'Catalyst flow [kg/hr]', 'Temperature [K]')

plt.show()
