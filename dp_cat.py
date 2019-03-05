"""
Compare differential pressure in the R-cubed riser for different catalyst flow
rates. Run this program for each low, mid, and high process gas flow.

Examples
--------

First argument denoted as low, mid, or high for process gas flow. Second
argument for differential pressure for pdit700, pdit704, pdit705, pdit706, or
pdit707. Stats are written to `results-hydro` directory.

>>> python dp_cat.py low pdit700
>>> python dp_cat.py mid pdit700
>>> python dp_cat.py high pdit704
"""

import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd
from utils import df_experiment, stats, config

# Command line argument
# ----------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('pg', help='process gas group as low, mid, high')
parser.add_argument('col', help='column name as pdit700, pdit704 etc.')
args = parser.parse_args()

n = ('low', 'mid', 'high').index(args.pg)
col = args.col.upper()

# Parameters from experimental matrix spreadsheet
# ----------------------------------------------------------------------------

# Experiments are referred to by item number in the experimental matrix
# spreadsheet. Each experiment was repeated three times, hence the three items
# in each tuple. The `*_items` variables contain three tuples which are for low,
# mid, and high process gas flow.

# Catalyst flow rates [kg/hr] for each experiment were obtained from the
# experimental matrix spreadsheet. The `*cat` variable contain three tuples for
# low, mid, and high process gas flow. Each item in the tuple represents a
# single experiment, there are three repeated experiments.

nocat_items = ('001', '005', '009'), ('013', '017', '021'), ('025', '029', '033')
lowcat_items = ('002', '006', '010'), ('014', '018', '022'), ('026', '030', '034')
midcat_items = ('003', '007', '011'), ('015', '019', '023'), ('027', '031', '035')
hicat_items = ('004', '008', '012'), ('016', '020', '024'), ('028', '032', '036')

lowcat = (46.8, 49.5, 44.3), (45.8, 45.1, 47.3), (53.2, 46.9, 56.5)
midcat = (91.3, 95.3, 91.6), (89.2, 95.1, 94.6), (102.2, 98.4, 97.1)
hicat = (137.6, 136.5, 141.7), (131.8, 138.2, 141.3), (140.1, 140.9, 144.8)

# Analyze process gas flow data for differential pressure
# ----------------------------------------------------------------------------

# Dataframes are for no, low, mid, and high catalyst flows. Each dataframe
# contains datetime and diff. pressure for three experiments.

# A statistics dataframe is printed to the console and written to a CSV file
# which is used by the dp_gas.py script.

if col in ('PDIT700', 'PDIT704'):
    h0m_files = [f for f in os.listdir('processed-hydro') if f.endswith('h0m.csv')]
    df_nocat = df_experiment(col, nocat_items[n], h0m_files)
    df_lowcat = df_experiment(col, lowcat_items[n], h0m_files)
    df_midcat = df_experiment(col, midcat_items[n], h0m_files)
    df_hicat = df_experiment(col, hicat_items[n], h0m_files)
elif col in ('PDIT705', 'PDIT706', 'PDIT707'):
    h00_files = [f for f in os.listdir('processed-hydro') if f.endswith('h00.csv')]
    df_nocat = df_experiment(col, nocat_items[n], h00_files)
    df_lowcat = df_experiment(col, lowcat_items[n], h00_files)
    df_midcat = df_experiment(col, midcat_items[n], h00_files)
    df_hicat = df_experiment(col, hicat_items[n], h00_files)
else:
    print('No column available in CSV data file.')

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

desc = 'Low', 'Mid', 'High'
print(f'\n{col} - {desc[n]} process gas experiments')
print(df_stats)

df_stats.to_csv(f'results-hydro/{col.lower()}_{desc[n].lower()}.csv', index_label='item')

# Plot
# ----------------------------------------------------------------------------

plt.close('all')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(9.4, 4.8), sharex='col')

for i in nocat_items[n]:
    ax1.plot(df_nocat[i].dropna(), label=f'{i}')
ax1.set_frame_on(False)
ax1.tick_params(color='0.9')
ax1.grid(True, color='0.9')
ax1.legend(loc='lower right')
ax1.set_ylabel('Differential pressure [kPa]')
ax1.set_title('No catalyst')

for i in lowcat_items[n]:
    ax2.plot(df_lowcat[i].dropna(), label=f'{i}')
ax2.set_frame_on(False)
ax2.tick_params(color='0.9')
ax2.grid(True, color='0.9')
ax2.legend(loc='lower right')
ax2.set_title('Low catalyst flow')

for i in midcat_items[n]:
    ax3.plot(df_midcat[i].dropna(), label=f'{i}')
ax3.set_frame_on(False)
ax3.tick_params(color='0.9')
ax3.grid(True, color='0.9')
ax3.legend(loc='lower right')
ax3.set_xlabel('Measurement [-]')
ax3.set_ylabel('Differential pressure [kPa]')
ax3.set_title('Mid catalyst flow')

for i in hicat_items[n]:
    ax4.plot(df_hicat[i].dropna(), label=f'{i}')
ax4.set_frame_on(False)
ax4.tick_params(color='0.9')
ax4.grid(True, color='0.9')
ax4.legend(loc='lower right')
ax4.set_xlabel('Measurement [-]')
ax4.set_title('High catalyst flow')
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
config(ax, 'Catalyst flow [kg/hr]', 'Differential pressure [kPa]')

plt.show()
