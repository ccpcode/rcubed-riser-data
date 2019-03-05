"""
Plot atmospheric pressure recorded at NREL during the hydrodynamics experiments.
Data is from the PIT000 senser.
"""

import matplotlib.pyplot as plt
import pandas as pd
from utils import config

cols = [0, 1, 2,
        4, 5, 6,
        8, 9, 10,
        12, 13, 14,
        16, 17, 18,
        20, 21, 22,
        24, 25, 26,
        28, 29, 30,
        32, 33, 34]

df = pd.read_csv('original-hydro/pit000_patm.csv', usecols=cols)

print(f"""
{'Date':10} {'Min':10} {'Max':10} {'Mean':10} {'Std':10}
{df['Date'][0]:10} {df['PIT000'].min():<10} {df['PIT000'].max():<10} {df['PIT000'].mean():<10.3f} {df['PIT000'].std():<10.3f}
{df['Date.1'][0]:10} {df['PIT000.1'].min():<10} {df['PIT000.1'].max():<10} {df['PIT000.1'].mean():<10.3f} {df['PIT000.1'].std():<10.3f}
{df['Date.2'][0]:10} {df['PIT000.2'].min():<10} {df['PIT000.2'].max():<10} {df['PIT000.2'].mean():<10.3f} {df['PIT000.2'].std():<10.3f}
{df['Date.3'][0]:10} {df['PIT000.3'].min():<10} {df['PIT000.3'].max():<10} {df['PIT000.3'].mean():<10.3f} {df['PIT000.3'].std():<10.3f}
{df['Date.4'][0]:10} {df['PIT000.4'].min():<10} {df['PIT000.4'].max():<10} {df['PIT000.4'].mean():<10.3f} {df['PIT000.4'].std():<10.3f}
{df['Date.5'][0]:10} {df['PIT000.5'].min():<10} {df['PIT000.5'].max():<10} {df['PIT000.5'].mean():<10.3f} {df['PIT000.5'].std():<10.3f}
{df['Date.6'][0]:10} {df['PIT000.6'].min():<10} {df['PIT000.6'].max():<10} {df['PIT000.6'].mean():<10.3f} {df['PIT000.6'].std():<10.3f}
{df['Date.7'][0]:10} {df['PIT000.7'].min():<10} {df['PIT000.7'].max():<10} {df['PIT000.7'].mean():<10.3f} {df['PIT000.7'].std():<10.3f}
{df['Date.8'][0]:10} {df['PIT000.8'].min():<10} {df['PIT000.8'].max():<10} {df['PIT000.8'].mean():<10.3f} {df['PIT000.8'].std():<10.3f}
""")

fig, ax = plt.subplots(tight_layout=True)
ax.plot(df['PIT000'], label=df['Date'][0])
ax.plot(df['PIT000.1'], label=df['Date.1'][0])
ax.plot(df['PIT000.2'], label=df['Date.2'][0])
ax.plot(df['PIT000.3'], label=df['Date.3'][0])
ax.plot(df['PIT000.4'], label=df['Date.4'][0])
ax.plot(df['PIT000.5'], label=df['Date.5'][0])
ax.plot(df['PIT000.6'], label=df['Date.6'][0])
ax.plot(df['PIT000.7'], label=df['Date.7'][0])
ax.plot(df['PIT000.8'], label=df['Date.8'][0])
config(ax, 'Measurement [-]', 'Atmospheric pressure [kPa]')
ax.legend(loc=2, bbox_to_anchor=(1.05, 1), frameon=False)

plt.show()
