"""
data_processing.py
------------------
Reads and validates the BIS WS_OTC_DERIV2 CSV data file and extracts
the key time series used in the paper.

Usage:
    python src/data_processing.py

Requirements:
    data/WS_OTC_DERIV2_csv_col.csv must be present (see data/README.md).

Output:
    Prints summary statistics and validates series coverage.
    Returns a dict of extracted series for use by figures.py if imported.
"""

import os
import sys
import numpy as np

try:
    import pandas as pd
except ImportError:
    print('pandas is required. Install with: pip install pandas')
    sys.exit(1)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
BIS_FILE = os.path.join(DATA_DIR, 'WS_OTC_DERIV2_csv_col.csv')


def load_bis_data():
    """Load the BIS OTC derivatives CSV and return as a DataFrame."""
    if not os.path.exists(BIS_FILE):
        raise FileNotFoundError(
            f'BIS data file not found: {BIS_FILE}\n'
            'See data/README.md for download instructions.'
        )
    df = pd.read_csv(BIS_FILE)
    print(f'Loaded BIS data: {len(df)} rows, {len(df.columns)} columns')
    return df


def extract_global_aggregate(df, der_type):
    """
    Extract the global aggregate series for a given DER_TYPE.

    Parameters
    ----------
    df : pd.DataFrame
        Full BIS WS_OTC_DERIV2 DataFrame.
    der_type : str
        'A' = notional outstanding
        'D' = gross market value
        'H' = gross credit exposure

    Returns
    -------
    dict mapping period (e.g. '2008-S2') to value in USD trillions.
    """
    labels = {'A': 'Notional', 'D': 'Gross Market Value', 'H': 'Gross Credit Exposure'}

    row = df[
        (df['DER_TYPE'] == der_type) &
        (df['DER_SECTOR_CPY'] == 'A') &      # all counterparty sectors
        (df['DER_INSTR'] == 'A') &            # all instruments
        (df['Reporting country'] == 'All countries') &
        (df['Risk category'] == 'Total (all risk categories)')
    ]

    if len(row) == 0:
        raise ValueError(f'No rows found for DER_TYPE={der_type} with all-country, all-instrument filter.')

    # Identify semiannual time columns
    time_cols = [c for c in df.columns if '-S' in str(c)]
    series = {}
    for col in time_cols:
        val = pd.to_numeric(row[col].values[0], errors='coerce')
        if not np.isnan(val):
            # Convert from USD millions to USD trillions
            series[col] = val / 1e6

    print(f'  {labels.get(der_type, der_type)}: {len(series)} periods from '
          f'{min(series.keys())} to {max(series.keys())}')
    return series


def compute_gmv_notional_ratio(notional, gmv):
    """
    Compute the GMV-to-notional ratio for periods present in both series.

    Returns a dict of {period: ratio_pct}.
    """
    ratio = {}
    for period in gmv:
        if period in notional and notional[period] > 0:
            ratio[period] = (gmv[period] / notional[period]) * 100
    return ratio


def print_key_statistics(ratio):
    """Print the key statistics cited in the paper."""
    values = list(ratio.values())
    print('\nKey statistics from BIS GMV/Notional ratio:')
    print(f'  Sample mean:  {np.mean(values):.2f}%')
    print(f'  Sample std:   {np.std(values):.2f}%')
    print(f'  Sample min:   {min(values):.2f}% ({min(ratio, key=ratio.get)})')
    print(f'  Sample max:   {max(values):.2f}% ({max(ratio, key=ratio.get)})')
    print(f'  Observations: {len(values)} semiannual periods')

    # Key periods cited in the paper
    key_periods = {
        '1998-S2': 'Pre-crisis baseline',
        '2008-S2': 'GFC peak',
        '2019-S2': 'Post-reform trough',
        '2022-S2': 'Rate-hike spike',
        '2025-S1': 'Most recent observation',
    }
    print('\n  Key periods:')
    for period, label in key_periods.items():
        if period in ratio:
            print(f'    {period} ({label}): {ratio[period]:.2f}%')


def main():
    print('=== BIS OTC Derivatives Data Validation ===\n')

    df = load_bis_data()

    print('\nExtracting global aggregate series...')
    notional = extract_global_aggregate(df, 'A')
    gmv      = extract_global_aggregate(df, 'D')
    gce      = extract_global_aggregate(df, 'H')

    ratio = compute_gmv_notional_ratio(notional, gmv)
    print_key_statistics(ratio)

    # Validate netting benefit proxy: GCE / GMV
    print('\nGross Credit Exposure / GMV ratio (netting benefit proxy):')
    gce_gmv_periods = ['2008-S2', '2019-S2', '2022-S2', '2025-S1']
    for p in gce_gmv_periods:
        if p in gce and p in gmv and gmv[p] > 0:
            nb = (1 - gce[p] / gmv[p]) * 100
            print(f'  {p}: netting benefit = {nb:.1f}%')

    print('\nValidation complete.')

    return {
        'notional': notional,
        'gmv': gmv,
        'gce': gce,
        'gmv_notional_ratio': ratio,
    }


if __name__ == '__main__':
    main()
