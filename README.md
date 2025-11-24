# FluxIQ: Franz Cell Release & Permeation Analyzer

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fluxiq.streamlit.app/)

**FluxIQ** is an open-source, intelligent analytical platform designed to automate the processing, modeling, and visualization of data from *in vitro* release (IVR) and permeation (IVP) studies using Franz diffusion cells.

Developed to replace fragmented workflows involving manual spreadsheets, FluxIQ offers a unified interface for pharmaceutical researchers to perform kinetic analysis and statistical comparisons with reproducibility and ease.

## 🌐 Quick Access (Live Demo)

You can use FluxIQ directly in your browser without any installation via Streamlit Cloud:

👉 **[Click here to access FluxIQ Online](https://fluxiq.streamlit.app/)**

## 🚀 Key Features

* **Release Module (IVR):**
    * Automated **Sink Condition Correction** for cumulative amounts.
    * **Kinetic Modeling:** Automatically fits and ranks 7 standard mathematical models:
        * Zero-Order, First-Order, Higuchi, Korsmeyer-Peppas, Hixson-Crowell, Weibull, and Peppas-Sahlin.
    * **Mechanism Interpretation:** AI-driven logic to interpret release mechanisms (Fickian diffusion, Anomalous transport, Case-II relaxation).
* **Permeation Module (IVP):**
    * Interactive selection of the **Steady-State** (linear) region.
    * Automatic calculation of Flux ($J_{ss}$), Lag Time ($T_{lag}$), Permeability Coefficient ($K_p$), and Diffusion Coefficient ($D$).
* **Statistical Analysis:**
    * Automated **ANOVA** and **t-tests** for comparisons between groups.
    * Calculation of the Similarity Factor ($f_2$) according to FDA/EMA guidelines.
* **AI Integration:** Generates structured prompts summarizing the results to assist in writing scientific discussions.

## 📦 Local Installation

If you prefer to run FluxIQ locally on your machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/gustavohrs-met/fluxiq.git](https://github.com/gustavohrs-met/fluxiq.git)
    cd fluxiq
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    streamlit run app_main.py
    ```

## 📊 Input Data Format

FluxIQ accepts `.csv`, `.txt`, or `.xlsx` files. The data must be in **Wide Format**.

### Example Structure:

| Sample_Name | Group | 0.5 | 1 | 2 | 4 | 6 | 24 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F1_Rep1 | Formulation_A | 1050 | 2500 | 4800 | 9000 | 12500 | 35000 |
| F1_Rep2 | Formulation_A | 1020 | 2450 | 4750 | 8950 | 12400 | 34800 |
| F2_Rep1 | Formulation_B | 500 | 1200 | 2400 | 4500 | 6000 | 18000 |

* **Column 1:** Unique Name for the replicate/sample.
* **Column 2:** Group Name (used for aggregation and statistics).
* **Columns 3+:** Time points (headers must be numbers representing time). Values are the raw signal (Area/Absorbance).

## 🧮 Mathematical Models

### Release Kinetics
The software utilizes `scipy.optimize.curve_fit` to minimize the sum of squared residuals (SSR) for the following models:

* **Higuchi:** $Q_t = K_H \sqrt{t}$
* **Korsmeyer-Peppas:** $Q_t / Q_{\infty} = K_{KP} t^n$
* **Peppas-Sahlin:** $Q_t / Q_{\infty} = k_1 t^m + k_2 t^{2m}$
* (And others...)

### Permeation Parameters
Based on Fick's First Law of Diffusion under steady-state conditions:

* **Flux ($J_{ss}$):** Calculated from the slope of the linear portion of the cumulative amount vs. time curve per unit area.
* **Permeability ($K_p$):** $J_{ss} / C_d$ (where $C_d$ is the donor concentration).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the GNU GPLv3 License. See `LICENSE` for more information.

## 🖊️ Citation

If you use **FluxIQ** in your research, please cite it as:

> **[Carvalho, F. V. & Rodrigues da Silva, G. H.]. FluxIQ: Franz Cell Analyzer (Version V1.0.0). [2025]. Available at [https://fluxiq.streamlit.app/].**

---
Developed by **IMeT Group**.