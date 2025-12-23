---
title: 'FluxIQ: A Python-based Interface for Franz Cell Release and Permeation Analysis'
tags:
  - Python
  - Streamlit
  - pharmacokinetics
  - permeation
  - drug release
  - Franz cells
  - diffusion
authors:
  - name: Fabiola Vieira Carvalho
    orcid: 0000-0002-4450-0563
    affiliation: 1
  - name: G. H. Rodrigues da Silva
    orcid: 0000-0001-7377-8532
    affiliation: 1
affiliations:
 - name: IMeT Group, Institution Name, Brazil
   index: 1
date: 24 November 2025
bibliography: paper.bib
---

# Summary

**FluxIQ** is a user-friendly analytical platform designed to automate the processing and modeling of *in vitro* release (IVR) and permeation (IVP) data obtained from Franz diffusion cell experiments. Built with Python and Streamlit, it provides a graphical interface for researchers to calculate kinetic parameters without requiring advanced programming skills.

# Statement of Need

Franz diffusion cells are the gold standard method for evaluating topical and transdermal drug delivery systems. However, the data analysis pipeline is often fragmented, relying on manual spreadsheets (e.g., Excel) to perform sink condition corrections, cumulative amount calculations, and linear regressions for steady-state flux. This manual process is prone to calculation errors and lacks standardization.

**FluxIQ** addresses these challenges by offering a unified workflow that:

1.  **Automates Data Processing:** Converts raw HPLC/UV data (concentration) into cumulative amounts ($Q$) and percentage released, automatically applying sink condition corrections.
2.  **Kinetic Modeling:** Fits experimental data to seven standard mathematical models (Zero-Order, First-Order, Higuchi, Korsmeyer-Peppas, Hixson-Crowell, Weibull, and Peppas-Sahlin) to elucidate drug release mechanisms [@Costa:2001].
3.  **Permeation Analysis:** Calculates key parameters such as Steady-State Flux ($J_{ss}$), Permeability Coefficient ($K_p$), Lag Time ($T_{lag}$), and Diffusion Coefficient ($D$) through an interactive interface that allows users to visually select the steady-state linear region.
4.  **Statistical Comparison:** Performs automated t-tests and ANOVA, as well as the similarity factor ($f_2$) calculation required by regulatory agencies (FDA/EMA) [@FDA:1997].

FluxIQ is designed for pharmaceutical researchers, students, and formulation scientists seeking a reproducible and open-source alternative to proprietary software for permeation analysis.

# References
