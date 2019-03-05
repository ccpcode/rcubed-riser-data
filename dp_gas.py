"""
Compare PDIT700 differential pressure in R-cubed riser for different process gas
conditions. Requires the results files generated from `dp_cat.py` to be in the
`results-hydro` folder.
"""

import matplotlib.pyplot as plt
import pandas as pd
from utils import config

# Plot
# ----------------------------------------------------------------------------

gasflow = [320, 400, 480]

df_low = pd.read_csv('results-hydro/pdit700_low.csv', index_col=0)
df_mid = pd.read_csv('results-hydro/pdit700_mid.csv', index_col=0)
df_high = pd.read_csv('results-hydro/pdit700_high.csv', index_col=0)

df_comp = pd.DataFrame(columns=['catflow', 'gas_low', 'gas_mid', 'gas_high'])
for i in range(len(df_low)):
    if i < 3:
        catflow = 'none'
    if 3 <= i < 6:
        catflow = 'low'
    if 6 <= i < 9:
        catflow = 'mid'
    if 9 <= i:
        catflow = 'high'
    gaslow = df_low.iloc[i]['mean']
    gasmid = df_mid.iloc[i]['mean']
    gashigh = df_high.iloc[i]['mean']
    df_comp.loc[i] = [catflow, gaslow, gasmid, gashigh]

# Plot
# ----------------------------------------------------------------------------

plt.close()

fig, ax = plt.subplots()
ax.plot(gasflow, df_comp.iloc[0][1:], 'C0', marker='.', label='none')
ax.plot(gasflow, df_comp.iloc[1][1:], 'C0', marker='.', label='_nolegend_')
ax.plot(gasflow, df_comp.iloc[2][1:], 'C0', marker='.', label='_nolegend_')
ax.plot(gasflow, df_comp.iloc[3][1:], 'C1', marker='.', label='low')
ax.plot(gasflow, df_comp.iloc[4][1:], 'C1', marker='.', label='_nolegend_')
ax.plot(gasflow, df_comp.iloc[5][1:], 'C1', marker='.', label='_nolegend_')
ax.plot(gasflow, df_comp.iloc[6][1:], 'C2', marker='.', label='mid')
ax.plot(gasflow, df_comp.iloc[7][1:], 'C2', marker='.', label='_nolegend_')
ax.plot(gasflow, df_comp.iloc[8][1:], 'C2', marker='.', label='_nolegend_')
ax.plot(gasflow, df_comp.iloc[9][1:], 'C3', marker='.', label='high')
ax.plot(gasflow, df_comp.iloc[10][1:], 'C3', marker='.', label='_nolegend_')
ax.plot(gasflow, df_comp.iloc[11][1:], 'C3', marker='.', label='_nolegend_')
config(ax, 'Gas flow [SLM]', 'Differential pressure [kPa]')
ax.legend(loc='lower left', bbox_to_anchor=(0.0, 1.01), ncol=4, frameon=False)

plt.show()
