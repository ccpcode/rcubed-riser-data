"""
Compare PDIT700 differential pressure in the R-cubed riser for the max catalyst
flow tests at low process gas flow. Refer to items 101, 102, 103, and 105 in
Excel spreadsheet.

Example
-------
>>> python dp_cat_max.py
"""

import matplotlib.pyplot as plt
import pandas as pd
from utils import config

# Analyze process gas flow data for max catalyst flow tests
# ----------------------------------------------------------------------------

maxcat = (266.0, 356.1, 420.7, 507.4)
df101 = pd.read_csv(f'processed-hydro/101_rd181219_h0m.csv', usecols=['DateTime', 'PDIT700'])
df102 = pd.read_csv(f'processed-hydro/102_rd181219_h0m.csv', usecols=['DateTime', 'PDIT700'])
df103 = pd.read_csv(f'processed-hydro/103_rd181219_h0m.csv', usecols=['DateTime', 'PDIT700'])
df105 = pd.read_csv(f'processed-hydro/105_rd181219_h0m.csv', usecols=['DateTime', 'PDIT700'])

# Plot
# ----------------------------------------------------------------------------

plt.close('all')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(df101['PDIT700'], label=maxcat[0])
ax.plot(df102['PDIT700'], label=maxcat[1])
ax.plot(df103['PDIT700'], label=maxcat[2])
ax.plot(df105['PDIT700'], label=maxcat[3])
config(ax, 'Measurement [-]', 'Differential pressure [kPa]')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(maxcat[0], df101['PDIT700'].mean(), 'oC0', label='mean')
ax.plot(maxcat[0], df101['PDIT700'].max(), '.C1', label='max')
ax.plot(maxcat[0], df101['PDIT700'].min(), '.C2', label='min')
ax.plot(maxcat[1], df102['PDIT700'].mean(), 'oC0', label='_nolegend_')
ax.plot(maxcat[1], df102['PDIT700'].max(), '.C1', label='_nolegend_')
ax.plot(maxcat[1], df102['PDIT700'].min(), '.C2', label='_nolegend_')
ax.plot(maxcat[2], df103['PDIT700'].mean(), 'oC0', label='_nolegend_')
ax.plot(maxcat[2], df103['PDIT700'].max(), '.C1', label='_nolegend_')
ax.plot(maxcat[2], df103['PDIT700'].min(), '.C2', label='_nolegend_')
ax.plot(maxcat[3], df105['PDIT700'].mean(), 'oC0', label='_nolegend_')
ax.plot(maxcat[3], df105['PDIT700'].max(), '.C1', label='_nolegend_')
ax.plot(maxcat[3], df105['PDIT700'].min(), '.C2', label='_nolegend_')
ax.xaxis.set_ticks([maxcat[0], maxcat[1], maxcat[2], maxcat[3]])
ax.fill_between(maxcat, [df101['PDIT700'].min(), df102['PDIT700'].min(), df103['PDIT700'].min(), df105['PDIT700'].min()], [df101['PDIT700'].max(), df102['PDIT700'].max(), df103['PDIT700'].max(), df105['PDIT700'].max()], alpha=0.5, facecolor='lightgrey')
config(ax, 'Catalyst flow [kg/hr]', 'Differential pressure, PDIT700 [kPa]')

plt.show()
