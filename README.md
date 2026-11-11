# The Value and Cost of Renegotiation Rights in Over-the-Counter Derivative Contracts

**Working Paper — October 2026**

---

## Overview

This repository contains the data processing code and figure generation scripts for the working paper:

> **The Value and Cost of Renegotiation Rights in Over-the-Counter Derivative Contracts**  
> Working Paper, October 2026

### Abstract

Over-the-counter (OTC) derivative contracts are inherently incomplete: no ex ante specification can anticipate every contingency affecting the value of a long-tenor financial obligation. Every OTC contract embeds an implicit option — the right to renegotiate its terms when circumstances diverge sufficiently from initial expectations. This paper estimates that the aggregate value of these embedded renegotiation rights currently lies between **$2.5 and $4.2 trillion** globally. Using BIS semiannual data (1998–2025), OCC quarterly call report data (1999–2025), and the ISDA margin survey (2017–2025), we document renegotiation option value across market segments and stress episodes, identify a specific regulatory gap, and propose a hazard-model empirical strategy for direct measurement once CFTC data access is obtained.

---

## Repository Structure

```
.
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── .gitignore
├── src/
│   ├── figures.py              # Generates all 6 figures from raw data
│   ├── data_processing.py      # Processes and validates raw data sources
│   └── utils.py                # Shared helper functions
├── data/
│   └── README.md               # Data download instructions
├── output/
│   └── figures/                # Generated figures (created by figures.py)
└── paper/
    └── renegotiation_rights_otc_derivatives.md   # Paper source (Markdown)
```

---

## Data Sources

All data used in this paper is **publicly available** at no cost. The table below lists each source, what it provides, and where to download it.

| Source | Variables Used | Download Link |
|--------|---------------|---------------|
| **BIS OTC Derivatives Statistics** (WS_OTC_DERIV2) | Global notional outstanding, gross market value (GMV), gross credit exposure (GCE), semiannual 1998–2025 | [data.bis.org/topics/OTC_DER](https://data.bis.org/topics/OTC_DER/data) |
| **OCC Quarterly Derivatives Report** (Q3 2025) | U.S. bank notional, GPFV, NCCE, netting benefit, CCP clearing rate by product, collateral composition | [occ.gov](https://www.occ.gov/publications-and-resources/publications/quarterly-report-on-bank-trading-and-derivatives-activities/index-quarterly-report-on-bank-trading-and-derivatives-activities.html) |
| **ISDA Annual Margin Survey** (Year-end 2025) | Initial margin (IM) and variation margin (VM) for non-cleared derivatives, 2017–2025 | [isda.org/research](https://www.isda.org/research/) |

> **Note on SDR data:** The empirical strategy proposed in Section 4 of the paper would additionally use DTCC Swap Data Repository (SDR) trade-level records (event codes NEWT, AMND, NOVA, TERM). This data exists but is not publicly accessible at the counterparty-identified level; it requires a formal CFTC research data access agreement. No SDR data is used in this repository.

### Downloading the Data

See [`data/README.md`](data/README.md) for step-by-step download instructions for each source.

After downloading, place files as follows:

```
data/
├── WS_OTC_DERIV2_csv_col.csv        # BIS OTC derivatives statistics
├── pub-derivatives-quarterly-qtr3-2025.pdf   # OCC Q3 2025 report
└── isda-margin-survey-2025.pdf      # ISDA margin survey year-end 2025
```

---

## Reproducing the Figures

### Requirements

Python 3.8 or higher. Install dependencies with:

```bash
pip install -r requirements.txt
```

### Generate All Figures

```bash
python src/figures.py
```

This will read the BIS CSV and hardcoded OCC/ISDA series extracted from the reports, and write six figures to `output/figures/`:

| Figure | Description | Primary Data Source |
|--------|-------------|-------------------|
| `fig1_renegotiation_proxy.png` | GMV-to-Notional ratio, 1998–2025 | BIS WS_OTC_DERIV2 |
| `fig2_exposure_layers.png` | Notional, GMV, and GCE, 1998–2025 | BIS WS_OTC_DERIV2 |
| `fig3_netting_clearing.png` | Netting benefit vs. CCP clearing rate, 2008–2025 | OCC Q3 2025 Report (Figure 11, Table 12) |
| `fig4_isda_margin.png` | Initial and variation margin, 2017–2025 | ISDA Margin Survey Year-end 2025 |
| `fig5_noncleared_stable.png` | Non-cleared notional vs. clearing rate, 2022–2025 | OCC Q3 2025 Report (Figure 6, Table 12) |
| `fig6_option_value.png` | Calibrated renegotiation option value by product | BIS + OCC (calibrated) |

### Process BIS Data Separately

To re-extract and validate the BIS time series from the raw CSV:

```bash
python src/data_processing.py
```

This script reads `data/WS_OTC_DERIV2_csv_col.csv`, validates the key series, and prints summary statistics used in the paper.

---

## Key Empirical Results

The table below summarises the core BIS data series used in Figure 1 and Table 1 of the paper.

| Period | Notional ($T) | GMV ($T) | GCE ($T) | GMV/Notional (%) |
|--------|:---:|:---:|:---:|:---:|
| 1998-H2 | 80 | 3.2 | 1.3 | 4.00 |
| 2008-H2 | 598 | 34.9 | 5.0 | **5.84** (peak) |
| 2018-H1 | 595 | 10.3 | 2.6 | **1.74** (trough) |
| 2022-H2 | 618 | 20.8 | 3.6 | 3.36 |
| 2025-H1 | 846 | 21.8 | 3.0 | 2.58 |

*Source: BIS OTC Derivatives Statistics, WS_OTC_DERIV2.*

---

## Theoretical Framework

The paper draws on three bodies of literature:

- **Incomplete contracts:** Hart and Moore (1988, 1999); Maskin and Tirole (1999); Segal (1999)
- **Default rules and legal entitlements:** Ayres and Gertner (1989); Ayres (2012); Ayres and Balkin (1996); Calabresi and Melamed (1972)
- **OTC market microstructure:** Duffie, Gârleanu, and Pedersen (2005); Hendershott and Madhavan (2015)

The renegotiation option's value is defined as:

$$V^{renegotiate} = \mathbb{E}_0 \left[\max\left(0, \frac{1}{2} S(\omega_t) - c(\omega_t)\right)\right]$$

where $S(\omega_t)$ is the joint bilateral surplus from contract modification in state $\omega_t$ and $c(\omega_t)$ is the renegotiation cost (search friction, legal costs, bargaining friction).

---

## Empirical Strategy (Proposed)

The paper proposes but does not execute a hazard-model strategy adapted from Roberts and Sufi (2009):

$$h(t | X) = h_0(t) \cdot \exp\!\left(\beta_1 \Delta CDS_{i,t} + \beta_2 \mathbf{1}[\text{CollateralCall}_{i,t}] + \beta_3 \mathbf{1}[\text{Stress}_t] + \beta_4 \log(Notional_i) + \gamma_{type} + \gamma_{dealer}\right)$$

This requires DTCC SDR counterparty-level event data (AMND, NOVA, TERM event codes), which is not currently accessible without a CFTC data access agreement.

---

## Author Contributions

This project was a collaboration. Professor Robert Meister contributed to the theoretical framework and provided conceptual guidance on the incomplete contracts and legal entitlements literature. Muhammad Jibrail designed the empirical strategy, built the data processing pipeline, generated the figures, and drafted the manuscript. Both authors contributed to the final interpretation of the results and the policy recommendations.

## Citation

If you use the code or data in this repository, please cite:

```bibtex
@techreport{renegotiation_rights_2026,
  title   = {The Value and Cost of Renegotiation Rights in
             Over-the-Counter Derivative Contracts},
  author  = {Meister, Robert and Jibrail, Muhammad},
  year    = {2026},
  month   = {October},
  type    = {Working Paper}
}
```

---

## License

The code in this repository is released under the MIT License. The paper text is copyright the author. The underlying data is subject to the terms of each respective data provider (BIS, OCC, ISDA).

---

## Contact

For questions about the code or data, please contact Muhammad Jibrail or Professor Robert Meister, or open an issue in this repository.
