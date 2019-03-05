"""
Process the original hydrodynamics data and write to a CSV file for model
development. CSV files are written to the `processed-hydro` directory.
"""

import pandas as pd

# Parameters
# ----------------------------------------------------------------------------

# each tuple in `condition` represents
# (item number in exp. matrix, file name, start time, stop time)
condition = (
    (1, 'rd181211', '16:38', '16:54'),
    (2, 'rd181211', '22:04', '22:17'),
    (3, 'rd181211', '22:54', '23:06'),
    (4, 'rd181211', '23:45', '23:56'),
    (5, 'rd181219', '9:39', '9:55'),
    (6, 'rd181219', '14:51', '15:06'),
    (7, 'rd181219', '16:36', '16:51'),
    (8, 'rd181219', '15:58', '16:13'),
    (9, 'rd181210', '18:39', '18:57'),
    (10, 'rd181210', '23:16', '23:31'),
    (11, 'rd181210', '22:23', '22:38'),
    (12, 'rd181210', '21:47', '22:02'),
    (13, 'rd181218', '10:02', '10:15'),
    (14, 'rd181218', '14:21', '14:36'),
    (15, 'rd181218', '13:33', '13:45'),
    (16, 'rd181218', '13:03', '13:16'),
    (17, 'rd181217', '12:32', '12:47'),
    (18, 'rd181217', '20:00', '20:12'),
    (19, 'rd181217', '17:53', '18:05'),
    (20, 'rd181217', '18:39', '18:51'),
    (21, 'rd181218', '15:51', '16:05'),
    (22, 'rd181218', '19:10', '19:24'),
    (23, 'rd181218', '20:29', '20:41'),
    (24, 'rd181218', '19:59', '20:12'),
    (25, 'rd181210', '11:46', '11:58'),
    (26, 'rd181210', '14:43', '15:00'),
    (27, 'rd181210', '14:14', '14:30'),
    (28, 'rd181210', '15:25', '15:40'),
    (29, 'rd181212', '10:43', '10:59'),
    (30, 'rd181213', '12:23', '12:39'),
    (31, 'rd181213', '13:36', '13:54'),
    (32, 'rd181213', '11:22', '11:37'),
    (33, 'rd181213', '19:25', '19:40'),
    (34, 'rd181214', '15:37', '15:47'),
    (35, 'rd181214', '16:28', '16:40'),
    (36, 'rd181214', '18:31', '18:43'),
    (101, 'rd181219', '17:10', '17:20'),
    (102, 'rd181219', '17:58', '18:07'),
    (103, 'rd181219', '18:12', '18:21'),
    (105, 'rd181219', '18:28', '18:33'),
    (201, 'rd181220', '11:26', '11:36'),
    (202, 'rd181220', '11:46', '11:56')
)

# Process Data
# ----------------------------------------------------------------------------

print('Save CSV files to processed-hydro directory')

for i in range(len(condition)):
    item = condition[i][0]
    f00 = f'{condition[i][1]}_h00.csv'
    f0m = f'{condition[i][1]}_h0m.csv'
    f19 = f'{condition[i][1]}_h19.csv'
    t0 = condition[i][2]
    t1 = condition[i][3]

    print(f'Process h00, h0m, and h19 files for item {item} ... ', end='')

    # h00 -------------

    c00 = [0, 6, 7, 8]
    n00 = ['DateTime', 'PDIT705', 'PDIT706', 'PDIT707']
    df_h00 = pd.read_csv(f'original-hydro/{f00}', names=n00, skiprows=2, usecols=c00)

    df_h00 = df_h00.dropna()
    df_h00['DateTime'] = pd.to_datetime(df_h00['DateTime'], format='%m/%d/%Y %H:%M:%S.%f')
    df_h00 = df_h00.set_index(['DateTime']).between_time(t0, t1)

    df_h00.to_csv(f'processed-hydro/{item:03g}_{f00}')

    # h0m -------------

    c0m = [0] + list(range(13, 23))
    n0m = ['DateTime', 'FIT600', 'FT702', 'FT750', 'PIT700', 'PIT780', 'PDIT700', 'PDIT704', 'PDIT780', 'ZC742', 'ZC762']
    df_h0m = pd.read_csv(f'original-hydro/{f0m}', names=n0m, skiprows=2, usecols=c0m)

    df_h0m = df_h0m.dropna()
    df_h0m['DateTime'] = pd.to_datetime(df_h0m['DateTime'], format='%m/%d/%Y %H:%M:%S')
    df_h0m = df_h0m.set_index(['DateTime']).between_time(t0, t1)

    df_h0m.to_csv(f'processed-hydro/{item:03g}_{f0m}')

    # h19 -------------

    c19 = [0] + list(range(3, 26))
    n19 = ['DateTime', 'TE629', 'TE701', 'TE705', 'TE706A_1', 'TE706A_2', 'TE706B_1', 'TE706B_2', 'TE706C_1', 'TE706C_2', 'TE707A', 'TE707B', 'TE707C', 'TE708A_1', 'TE708A_2', 'TE708B_1', 'TE708B_2', 'TE708C_1', 'TE708C_2', 'TE709A', 'TE709B', 'TE709C', 'TE741A', 'TE743']
    df_h19 = pd.read_csv(f'original-hydro/{f19}', names=n19, skiprows=2, usecols=c19)

    df_h19 = df_h19.dropna()
    df_h19['DateTime'] = pd.to_datetime(df_h19['DateTime'])
    df_h19 = df_h19.set_index(['DateTime']).between_time(t0, t1)

    df_h19.to_csv(f'processed-hydro/{item:03g}_{f19}')

    print('Complete.')

print('Done.')
