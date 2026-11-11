"""
utils.py
--------
Shared utility functions for data processing and figure generation.
"""

import os
import numpy as np


def ensure_output_dir(path):
    """Create output directory if it does not exist."""
    os.makedirs(path, exist_ok=True)
    return path


def usd_millions_to_trillions(value):
    """Convert a value in USD millions to USD trillions."""
    return value / 1e6


def compute_ratio_pct(numerator, denominator):
    """Compute a percentage ratio, returning None if denominator is zero."""
    if denominator == 0 or denominator is None:
        return None
    return (numerator / denominator) * 100


def parse_bis_period(period_str):
    """
    Parse a BIS semiannual period string into a decimal year.

    Parameters
    ----------
    period_str : str
        e.g. '2008-S2' -> 2008.5, '2008-S1' -> 2008.0

    Returns
    -------
    float
    """
    year, half = period_str.split('-S')
    return int(year) + (0.5 if half == '2' else 0.0)


def format_trillions(value, decimals=1):
    """Format a value in trillions with a T suffix."""
    return f'${value:.{decimals}f}T'


def gfc_stress_indicator(year_decimal):
    """Return True if the period falls within a major stress episode."""
    stress_periods = [
        (2007.5, 2009.5),   # Global Financial Crisis
        (2010.5, 2012.5),   # European sovereign debt crisis
        (2019.75, 2020.75), # COVID-19
        (2022.0, 2023.0),   # Rate-hiking cycle
    ]
    return any(s <= year_decimal <= e for s, e in stress_periods)
