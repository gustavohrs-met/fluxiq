import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats 
import io 
import xlsxwriter 
from scipy.optimize import curve_fit 

# O m_release.py deve estar presente para importar as funções básicas de cálculo
try:
    from m_release import calcular_liberacao_replica_v9, load_data, get_download_button
except ImportError:
    st.error("Erro no módulo de Permeação: Falha ao importar funções básicas de 'm_release.py'. Verifique se 'm_release.py' existe.")
    st.stop()

# Configuração padrão do Plotly (para remover warnings de depreciação)
PLOTLY_CONFIG = {
    'displayModeBar': True,
    'responsive': True
}


# --- Dicionário de Tradução (i18n) - MÓDULO PERMEAÇÃO ---
TEXT_DICT = {
    'pt': {
        'perm_sidebar_info': "Módulo de Permeação", # SIMPLIFICADO
        'nav_step1': "Etapa 1: Configuração e Upload",
        'step2_warning_process': "Por favor, carregue e processe os dados na 'Etapa 1' primeiro.",
        'step2_subheader_raw': "1. Tabela de Dados Processados (Por Réplica)",
        'step2_subheader_agg': "2. Tabela de Dados Agregados (Média e Desvio Padrão)",
        'download_excel': "Baixar como Excel",
        'step1_subheader_units': "Unidades Globais",
        'step1_label_vol_unit': "Unidade de Volume",
        'step1_label_conc_unit': "Unidade de Concentração (Massa/Volume)",
        'step1_subheader_cell': "Parâmetros da Célula (Global)",
        'step1_label_vol_receptor': "Volume Receptor",
        'step1_label_vol_sample': "Volume da Amostra Coletada",
        'step1_subheader_calib': "Curva de Calibração (Global)",
        'step1_label_calib_a': "Coeficiente Angular (a)",
        'step1_label_calib_b': "Intercepto (b)",
        'step1_help_calib_b': "Valores negativos são permitidos.",
        'step1_subheader_time': "Configuração do Tempo (Planilha)",
        'step1_label_time_unit': "Unidade de Tempo no Cabeçalho",
        'step1_time_hours': "Horas",
        'step1_time_minutes': "Minutos",
        'step1_subheader_upload': "Carregar Dados do Experimento (Formato Largo)",
        'step1_upload_preview': "Dados Carregados (Pré-visualização):",
        'step1_csv_options': "Opções de leitura de CSV/TXT detectadas:",
        'step1_csv_sep': "Separador de Coluna",
        'step1_csv_sep_semi': "; (Ponto e Vírgula)",
        'step1_csv_sep_comma': ", (Vírgula)",
        'step1_csv_sep_tab': "Tab",
        'step1_csv_dec': "Separador Decimal",
        'step1_csv_dec_comma': ", (Vírgula)",
        'step1_csv_dec_point': ". (Ponto)",
        'step1_error_calib_a': "O Coeficiente Angular (a) da calibração não pode ser zero.",
        'step1_expander_model': "Ver Modelo de Referência da Planilha",
        'step1_uploader_label': "Carregue seu arquivo",
        'step1_dose_group': "Grupo:",
        'step1_button_process': "Processar Dados",
        'step1_spinner_process': "Processando...",
        'step1_success_process': "Dados processados! Navegue para a 'P-Etapa 2'.",
        'step1_error_process': "Erro ao ler ou processar o arquivo:",
        'step1_col_conc_name': "Concentracao",
        'step1_col_q_name': "Q_Acumulada_Corrigida",
        'step1_col_pct_name': "Percent_Liberado (%)",
        
        'perm_nav_step1': "P-Etapa 1: Configuração e Upload",
        'perm_nav_step2': "P-Etapa 2: Dados Processados",
        'perm_nav_step3': "P-Etapa 3: Gráficos de Permeação", 
        'perm_nav_step4': "P-Etapa 4: Cálculo do Fluxo e Parâmetros", 
        'perm_nav_step5': "P-Etapa 5: Resumo Comparativo",
        
        'perm_step1_header': "P-Etapa 1: Configuração e Upload (Permeação)",
        'perm_step1_subheader_params': "Parâmetros de Permeação (Global)",
        'perm_step1_label_area': "Área da Membrana (cm²)",
        'perm_step1_label_thickness': "Espessura da Membrana (cm)",
        'perm_step1_help_thickness': "Opcional. Necessário para calcular o Coeficiente de Difusão (D).",
        'perm_step1_subheader_donor': "Configuração da Amostra (por Grupo)", 
        'perm_step1_label_dose_type': "Tipo de Dose Doadora:", 
        'perm_step1_type_infinite': "Dose Infinita (Volume Grande / $C_{0}$ Constante)", 
        'perm_step1_type_finite': "Dose Finita (Volume/Massa Limitada)", 
        'perm_step1_label_sample_type': "Formato da Amostra/Unidades de Dose:", 
        'perm_step1_type_vol': "Líquido/Solução (Concentração em Volume, ex: mg/mL)", 
        'perm_step1_type_mass': "Sólido/Gel/Creme (Concentração em Massa, ex: mg/g)", 
        'perm_step1_label_donor_conc': "Concentração Doadora Inicial ($C_{0}$)", 
        'perm_step1_label_donor_vol_mass': "Volume/Massa Doador Aplicado", 
        'perm_y_label_q': "Qtd. Permeada",

        'perm_step2_header': "P-Etapa 2: Dados Processados 📊",
        'perm_step2_info': "Estes são os dados brutos calculados. A coluna 'Q_Acumulada_Corrigida' (e suas médias) é usada para todos os cálculos de permeação.",

        'perm_step3_header': "P-Etapa 3: Gráficos de Permeação 📈",
        'perm_step3_info': "Visualize o perfil de permeação acumulada (Média $\pm$ SD) de todos os grupos. Use este gráfico para identificar a região de Steady-State (linear) que será usada na próxima etapa.",
        'step3_color_picker_label': "Personalizar Cores",
        'step3_color_picker_group': "Cor para",
        'step3_xaxis_label': "Tempo (horas)",
        'step3_title_compare': "Comparação dos Perfis de Permeação (Média $\pm$ SD)",

        'perm_step4_header': "P-Etapa 4: Cálculo do Fluxo (Steady-State) e Parâmetros",
        'perm_step4_info': "Esta etapa calcula os parâmetros chave ($J_{ss}$, $T_{lag}$, $K_p$, $D$) a partir da fase linear de Steady-State. **Ajuste o controle deslizante abaixo do gráfico para definir a fase linear.**",
        'perm_step4_subheader_params': "Parâmetros de Permeação Calculados para:",
        'perm_step4_selectbox_group': "Selecione o Grupo para Ajuste:",
        'perm_step4_slider_label': "Selecione o Intervalo de Tempo para o Ajuste Linear (Steady-State):",
        'perm_step4_plot_title': "Ajuste Linear de Steady-State para:",
        'perm_step4_plot_data': "Dados da Média",
        'perm_step4_plot_fit': "Extrapolação Linear (Jss / Tlag)",
        'perm_step4_subheader_fit': "Resultados do Ajuste Linear",
        'perm_step4_r2': "R² do Ajuste Linear",
        'perm_step4_slope': "Inclinação (Slope)",
        'perm_step4_intercept': "Intercepto",
        'perm_step4_error_fit': "Não foi possível realizar o ajuste. Selecione pelo menos 2 pontos.",
        'perm_step4_error_points': "Não há dados de média suficientes para este grupo.",
        'perm_step4_methodology_header': "Metodologia de Cálculo", 
        'sequence_analysis': "Sequência de Análise", # <-- NOVO
        'adjust_slider_label': "Ajuste o Controle Deslizante", # <-- NOVO
        
        'perm_param_jss': "Fluxo de Steady-State (Jss)",
        'perm_param_lag': "Tempo de Latência (T_lag)",
        'perm_param_kp': "Coef. de Permeabilidade (Kp)",
        'perm_param_d': "Coef. de Difusão (D)",
        'perm_step4_button_save': "Salvar Resultados para este Grupo",
        'perm_step4_save_success': "Resultados salvos para o grupo:",
        'perm_step4_error_area': "Erro: A Área da Membrana (Etapa 1) deve ser > 0 para calcular Jss e Kp.",
        'perm_step4_error_c0': "Aviso: A Conc. Doador (Etapa 1) é 0. Não é possível calcular Kp.",
        'perm_step4_error_thickness': "Aviso: A Espessura da Membrana (Etapa 1) é 0. Não é possível calcular D.",
        'perm_step4_error_no_fit': "Nenhum ajuste linear encontrado. Por favor, ajuste o Steady-State primeiro.",
        'perm_step4_warning_dose': "AVISO: Dose Finita. O cálculo de Kp assume que $C_0$ é a concentração inicial. Se houver depleção significativa do doador, o modelo pode não ser exato.",
        
        'perm_step5_header': "P-Etapa 5: Resumo Comparativo dos Parâmetros de Permeação",
        'perm_step5_info': "Use as abas abaixo para comparar seus grupos.",
        'perm_step5_tab_summary': "Resumo de Parâmetros", 
        'perm_step5_tab_stats': "Análise Estatística", 
        
        'perm_step5_col_group': "Grupo",
        'perm_step5_col_jss': "Fluxo (Jss)",
        'perm_step5_col_lag': "T_lag (h)",
        'perm_step5_col_kp': "Kp (cm/h)",
        'perm_step5_col_d': "D (cm²/h)",
        'perm_step5_col_r2': "R² (Ajuste)",
        'perm_step5_empty': "Nenhum resultado salvo ainda. Vá para a P-Etapa 4 para calcular e salvar os parâmetros de cada grupo.",
        
        'perm_stats_header': "Comparação Estatística (ANOVA/t-test)",
        'perm_stats_info': "Esta análise calcula o parâmetro selecionado para **cada réplica** no intervalo de tempo comum para determinar se a diferença entre os grupos é estatisticamente significante (p < 0.05).",
        'perm_stats_select_groups': "Selecione os grupos para comparar (2 ou mais):",
        'perm_stats_select_time_range': "Defina o Intervalo de Tempo (h) para o cálculo (Comum a Todos):",
        'perm_stats_select_param': "Selecione o Parâmetro para Comparar:",
        'perm_stats_param_jss': "Fluxo de Steady-State (Jss)",
        'perm_stats_param_lag': "Tempo de Latência (T_lag)",
        'perm_stats_param_kp': "Coef. de Permeabilidade (Kp)",
        'perm_stats_param_d': "Coef. de Difusão (D)",
        'perm_stats_button': "Rodar Análise Estatística",
        'perm_stats_results': "Resultados da Análise",
        'perm_stats_ttest': "Teste t (2 Grupos)",
        'perm_stats_anova': "ANOVA (>2 Grupos)",
        'perm_stats_p_value': "Valor-p",
        'perm_stats_conclusion_sig': "SIGNIFICANTE: A diferença entre os grupos é estatisticamente significante (p < 0.05).",
        'perm_stats_conclusion_nonsig': "NÃO SIGNIFICANTE: A diferença entre os grupos não é estatisticamente significante (p >= 0.05).",
        'perm_stats_error_replicas': "Erro: Pelo menos um dos grupos selecionados não possui réplicas suficientes (mínimo 2) ou dados válidos neste intervalo de tempo.",
        'perm_stats_error_no_fit': "Erro: Não foi possível calcular o parâmetro para algumas réplicas. Verifique a linearidade dos dados no intervalo selecionado.",
        'perm_stats_error_no_data': "Erro: Nenhum dado encontrado no intervalo selecionado para um dos grupos.",
        'home_footer': "Retornar à Seleção de Módulo", # <-- CORRIGIDO
    },
    'en': {
        'perm_sidebar_info': "Permeation Module", # SIMPLIFICADO
        'nav_step1': "Step 1: Setup & Upload",
        'step2_warning_process': "Please upload and process data in 'Step 1' first.",
        'step2_subheader_raw': "1. Processed Data Table (Per Replicate)",
        'step2_subheader_agg': "2. Aggregated Data Table (Mean and Std Dev)",
        'download_excel': "Download as Excel",
        'step1_subheader_units': "Global Units",
        'step1_label_vol_unit': "Volume Unit",
        'step1_label_conc_unit': "Concentration Unit (Mass/Volume)",
        'step1_subheader_cell': "Cell Parameters (Global)",
        'step1_label_vol_receptor': "Receptor Volume",
        'step1_label_vol_sample': "Collected Sample Volume",
        'step1_subheader_calib': "Calibration Curve (Global)",
        'step1_label_calib_a': "Slope (a)",
        'step1_label_calib_b': "Intercept (b)",
        'step1_help_calib_b': "Negative values are allowed.",
        'step1_subheader_time': "Time Setup (Spreadsheet)",
        'step1_label_time_unit': "Time Unit in Header",
        'step1_time_hours': "Hours",
        'step1_time_minutes': "Minutes",
        'step1_subheader_upload': "Upload Experiment Data (Wide Format)",
        'step1_upload_preview': "Uploaded Data (Preview):",
        'step1_csv_options': "Detected CSV/TXT reading options:",
        'step1_csv_sep': "Column Separator",
        'step1_csv_sep_semi': "; (Semicolon)",
        'step1_csv_sep_comma': ", (Comma)",
        'step1_csv_sep_tab': "Tab",
        'step1_csv_dec': "Decimal Separator",
        'step1_csv_dec_comma': ", (Comma)",
        'step1_csv_dec_point': ". (Point)",
        'step1_error_calib_a': "The calibration Slope (a) cannot be zero.",
        'step1_expander_model': "View Spreadsheet Reference Model",
        'step1_uploader_label': "Upload your file",
        'step1_dose_group': "Group:",
        'step1_button_process': "Process Data",
        'step1_spinner_process': "Processing...",
        'step1_success_process': "Data processed! Navigate to 'P-Step 2'.",
        'step1_error_process': "Error reading or processing file:",
        'step1_col_conc_name': "Concentration",
        'step1_col_q_name': "Q_Accumulated_Corrected",
        'step1_col_pct_name': "Percent_Released (%)",
        
        'perm_nav_step1': "P-Step 1: Setup & Upload",
        'perm_nav_step2': "P-Step 2: Processed Data",
        'perm_nav_step3': "P-Step 3: Permeation Plots", 
        'perm_nav_step4': "P-Step 4: Flux & Parameter Calculation", 
        'perm_nav_step5': "P-Step 5: Comparative Summary",
        
        'perm_step1_header': "P-Step 1: Setup & Upload (Permeation)",
        'perm_step1_subheader_params': "Permeation Parameters (Global)",
        'perm_step1_label_area': "Membrane Area (cm²)",
        'perm_step1_label_thickness': "Membrane Thickness (cm)",
        'perm_step1_help_thickness': "Optional. Needed to calculate Diffusion Coefficient (D).",
        'perm_step1_subheader_donor': "Sample Configuration (per Group)", 
        'perm_step1_label_dose_type': "Donor Dose Type:", 
        'perm_step1_type_infinite': "Infinite Dose (Large Volume / Constant $C_{0}$)", 
        'perm_step1_type_finite': "Finite Dose (Limited Volume/Mass)", 
        'perm_step1_label_sample_type': "Sample Format/Dose Units:", 
        'perm_step1_type_vol': "Liquid/Solution (Concentration in Volume, e.g., mg/mL)", 
        'perm_step1_type_mass': "Solid/Gel/Cream (Concentration in Mass, e.g., mg/g)", 
        'perm_step1_label_donor_conc': "Initial Donor Concentration ($C_{0}$)",
        'perm_step1_label_donor_vol_mass': "Donor Volume/Mass Applied", 
        'perm_y_label_q': "Amt. Permeated",
        
        'perm_step2_header': "P-Step 2: Processed Data 📊",
        'perm_step2_info': "This is the calculated raw data. The 'Q_Accumulated_Corrigida' column (and its mean) is used for all permeation calculations.",

        'perm_step3_header': "P-Step 3: Permeation Plots 📈",
        'perm_step3_info': "Visualize the cumulative permeation profile (Mean $\pm$ SD) of all groups. Use this plot to identify the Steady-State (linear) region, which will be used in the next step.",
        'step3_color_picker_label': "Customize Colors",
        'step3_color_picker_group': "Color for",
        'step3_xaxis_label': "Time (hours)",
        'step3_title_compare': "Comparison of Permeation Profiles (Mean $\pm$ SD)",

        'perm_step4_header': "P-Step 4: Flux (Steady-State) and Parameter Calculation",
        'perm_step4_info': "This step calculates the key parameters ($J_{ss}$, $T_{lag}$, $K_p$, $D$) from the Steady-State linear phase. **Adjust the slider below the plot to define the linear phase.**",
        'perm_step4_subheader_params': "Calculated Permeation Parameters for:",
        'perm_step4_selectbox_group': "Select Group for Fitting:",
        'perm_step4_slider_label': "Select Time Range for Linear Fit (Steady-State):",
        'perm_step4_plot_title': "Steady-State Linear Fit for:",
        'perm_step4_plot_data': "Mean Data",
        'perm_step4_plot_fit': "Linear Extrapolation (Jss / Tlag)",
        'perm_step4_subheader_fit': "Linear Fit Results",
        'perm_step4_r2': "Linear Fit R²",
        'perm_step4_slope': "Slope",
        'perm_step4_intercept': "Intercept",
        'perm_step4_error_fit': "Could not perform fit. Select at least 2 points.",
        'perm_step4_error_points': "Not enough mean data points for this group.",
        'perm_step4_methodology_header': "Calculation Methodology", 
        'sequence_analysis': "Analysis Sequence", # <-- NOVO
        'adjust_slider_label': "Adjust the Slider", # <-- NOVO
        
        'perm_param_jss': "Steady-State Flux (Jss)",
        'perm_param_lag': "Lag Time (T_lag)",
        'perm_param_kp': "Permeability Coeff. (Kp)",
        'perm_param_d': "Diffusion Coeff. (D)",
        'perm_step4_button_save': "Save Results for this Group",
        'perm_step4_save_success': "Results saved for group:",
        'perm_step4_error_area': "Error: Membrane Area (Step 1) must be > 0 to calculate Jss and Kp.",
        'perm_step4_error_c0': "Warning: Donor Conc. (Step 1) is 0. Cannot calculate Kp.",
        'perm_step4_error_thickness': "Warning: Membrane Thickness (Step 1) is 0. Cannot calculate D.",
        'perm_step4_error_no_fit': "No linear fit found. Please adjust the Steady-State first.",
        'perm_step4_warning_dose': "WARNING: Finite Dose. Kp calculation assumes $C_0$ is the initial concentration. If significant donor depletion occurs, the model may be inaccurate.",
        
        'perm_step5_header': "P-Step 5: Comparative Summary of Permeation Parameters",
        'perm_step5_info': "Use the tabs below to compare your groups.",
        'perm_step5_tab_summary': "Parameter Summary", 
        'perm_step5_tab_stats': "Statistical Analysis", 
        
        'perm_step5_col_group': "Group",
        'perm_step5_col_jss': "Flux (Jss)",
        'perm_step5_col_lag': "T_lag (h)",
        'perm_step5_col_kp': "Kp (cm/h)",
        'perm_step5_col_d': "Diffusion Coeff. (D)",
        'perm_step5_col_r2': "R² (Fit)",
        'perm_step5_empty': "No saved results yet. Go to P-Step 4 to calculate and save parameters for each group.",
        
        'perm_stats_header': "Statistical Comparison (ANOVA/t-test)",
        'perm_stats_info': "This analysis calculates the selected parameter for **each replicate** in the common time range to determine if the difference between groups is statistically significant (p < 0.05).",
        'perm_stats_select_groups': "Select groups to compare (2 or more):",
        'perm_stats_select_time_range': "Define Time Range (h) for calculation (Common to All):",
        'perm_stats_select_param': "Select Parameter to Compare:",
        'perm_stats_param_jss': "Steady-State Flux (Jss)",
        'perm_stats_param_lag': "Lag Time (T_lag)",
        'perm_stats_param_kp': "Permeability Coeff. (Kp)",
        'perm_stats_param_d': "Diffusion Coeff. (D)",
        'perm_stats_button': "Run Statistical Analysis",
        'perm_stats_results': "Analysis Results",
        'perm_stats_ttest': "t-test (2 Groups)",
        'perm_stats_anova': "ANOVA (>2 Groups)",
        'perm_stats_p_value': "p-value",
        'perm_stats_conclusion_sig': "SIGNIFICANT: The difference between the groups is statistically significant (p < 0.05).",
        'perm_stats_conclusion_nonsig': "NOT SIGNIFICANT: The difference between the groups is not statistically significant (p >= 0.05).",
        'perm_stats_error_replicas': "Error: At least one of the selected groups does not have enough replicates (minimum 2) or valid data in this time range.",
        'perm_stats_error_no_fit': "Error: Could not calculate the parameter for some replicates. Check data linearity in the selected range.",
        'perm_stats_error_no_data': "Error: No data found in the selected range for one of the groups.",
        'home_footer': "Return to Module Selection", # <-- CORRIGIDO
    }
}

# --- Função de Cálculo de Parâmetros por Réplica ---
def calculate_perm_params_replica(df_replica, area, thickness, c0, y_axis_col):
    """Calcula Jss, T_lag, Kp, D para uma única réplica (df_replica) usando fit linear."""
    
    t_data_rep = df_replica['Tempo']
    q_data_rep = df_replica[y_axis_col]
    
    # Mínimo de 2 pontos para regressão linear
    if len(q_data_rep) < 2:
        return None

    try:
        # Tenta a regressão linear
        fit = stats.linregress(t_data_rep, q_data_rep)
        slope = fit.slope
        intercept = fit.intercept
        
        # 1. Jss (Fluxo)
        jss = slope / area if area > 0 else 0.0
        
        # 2. T_lag (Tempo de Latência)
        t_lag = -intercept / slope if slope != 0 else 0.0
        t_lag = max(t_lag, 0)
        
        # 3. Kp (Coef. Permeabilidade)
        kp = jss / c0 if c0 > 0 and jss != 0 else 0.0
        
        # 4. D (Coef. Difusão)
        d_coeff = (thickness**2) / (6 * t_lag) if t_lag > 0 and thickness > 0 else 0.0
        
        return {
            'Jss': jss,
            'T_lag': t_lag,
            'Kp': kp,
            'D': d_coeff,
            'R2': fit.rvalue**2
        }
    except Exception:
        # Se linregress falhar (e.g., todos os pontos são iguais)
        return None


# --- Funções de Renderização de Página ---

def render_perm_step1(T):
    st.header(T['perm_step1_header'])
    
    # Coletar parâmetros de permeação
    st.subheader(T['perm_step1_subheader_params'])
    colp1, colp2 = st.columns(2)
    membrane_area = colp1.number_input(T['perm_step1_label_area'], min_value=0.0, value=1.77, format="%.2f", step=0.1, key="perm_area")
    membrane_thickness = colp2.number_input(T['perm_step1_label_thickness'], min_value=0.0, value=0.05, format="%.2f", step=0.01, help=T['perm_step1_help_thickness'], key="perm_thickness")
    
    st.markdown("---")
    
    # Coletar parâmetros de Célula e Calibração
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(T['step1_subheader_units'])
        unidade_vol = st.selectbox(T['step1_label_vol_unit'], ["mL", "L", "µL"], 0, key="perm_vol_unit")
        unidade_conc = st.selectbox(T['step1_label_conc_unit'], ["mg/mL", "µg/mL", "g/L", "mmol/L", "µmol/L"], 0, key="perm_conc_unit")
        unidade_massa = unidade_conc.split('/')[0]
        st.markdown("---")
        st.subheader(T['step1_subheader_cell'])
        vol_celula = st.number_input(f"{T['step1_label_vol_receptor']} ({unidade_vol})", min_value=0.01, value=12.0, format="%.2f", step=0.1, key="perm_vol_celula")
        vol_amostra = st.number_input(f"{T['step1_label_vol_sample']} ({unidade_vol})", min_value=0.0, value=1.0, format="%.2f", step=0.1, key="perm_vol_amostra")
    with col2:
        st.subheader(T['step1_subheader_calib'])
        st.markdown(f"`Área = a * Conc. ({unidade_conc}) + b`")
        cal_a = st.number_input(T['step1_label_calib_a'], value=10000.0, format="%.2f", step=1.0, key="perm_cal_a")
        cal_b = st.number_input(T['step1_label_calib_b'], value=0.0, format="%.2f", step=0.01, help=T['step1_help_calib_b'], key="perm_cal_b")
        st.markdown("---")
        st.subheader(T['step1_subheader_time'])
        unidade_tempo = st.selectbox(T['step1_label_time_unit'], [T['step1_time_hours'], T['step1_time_minutes']], 0, key="perm_time_unit")
    
    st.markdown("---")
    st.subheader(T['step1_subheader_upload'])
    
    uploaded_file = st.file_uploader(T['step1_uploader_label'], type=["csv", "xlsx", "txt"], key="perm_uploader")
    
    sep = ','
    decimal = '.'
    if uploaded_file and (uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt')):
        st.info(T['step1_csv_options'])
        col_parse1, col_parse2 = st.columns(2)
        with col_parse1:
            sep_label = st.selectbox(T['step1_csv_sep'], [T['step1_csv_sep_semi'], T['step1_csv_sep_comma'], T['step1_csv_sep_tab']], 0, key="perm_sep")
            sep = sep_label.split(" ")[0].replace("Tab","\t")
        with col_parse2:
            dec_label = st.selectbox(T['step1_csv_dec'], [T['step1_csv_dec_comma'], T['step1_csv_dec_point']], 1, key="perm_dec")
            decimal = dec_label.split(" ")[0]

    if uploaded_file is not None:
        if cal_a == 0:
            st.error(T['step1_error_calib_a'])
            return
        try:
            # Reutiliza load_data do m_release
            if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
                df_wide = load_data(uploaded_file, sep=sep, decimal=decimal)
            else:
                df_wide = pd.read_excel(uploaded_file)
            
            if df_wide is None: 
                return

            # FIX V62: width='stretch'
            st.write(T['step1_upload_preview'])
            st.dataframe(df_wide.head(), width='stretch')
            
            col_amostra_nome = df_wide.columns[0]
            col_grupo = df_wide.columns[1]
            cols_tempo = df_wide.columns[2:]
            
            st.markdown("---")
            st.subheader(T['perm_step1_subheader_donor'])
            
            # --- Configuração de Dose ---
            col_dose_type, col_sample_type = st.columns(2)
            dose_type = col_dose_type.selectbox(T['perm_step1_label_dose_type'], [T['perm_step1_type_infinite'], T['perm_step1_type_finite']], key="perm_dose_type_select")
            sample_type = col_sample_type.radio(T['perm_step1_label_sample_type'], [T['perm_step1_type_vol'], T['perm_step1_type_mass']], key="perm_sample_type_radio")
            
            # Define as unidades de aplicação e concentração C0
            unidade_aplicada = unidade_vol if sample_type == T['perm_step1_type_vol'] else 'g'
            unidade_conc_c0 = unidade_conc if sample_type == T['perm_step1_type_vol'] else f"{unidade_massa}/{unidade_aplicada}"
            
            # C0 (Concentração Doadora) - Requerida para Kp
            st.markdown(f"**{T['perm_step1_label_donor_conc']}** ({unidade_conc_c0}):")
            
            unique_groups = df_wide[col_grupo].unique()
            doses_dict = {} 
            c0_dict = {} 

            st.markdown("---")

            for grupo in unique_groups:
                st.markdown(f"**{T['step1_dose_group']} {grupo}**")
                c1, c2 = st.columns(2)
                
                # C0
                conc_form = c1.number_input("Conc. C0", key=f"perm_conc_{grupo}", min_value=0.0, value=10.0, format="%.2f", step=0.1)
                
                dose_total_grupo = 1.0 
                
                if dose_type == T['perm_step1_type_finite']:
                    # Dose Finita: pedimos a massa/volume aplicado
                    
                    vol_label = f"{T['perm_step1_label_donor_vol_mass']} ({unidade_aplicada})"
                    vol_or_mass_form = c2.number_input(vol_label, key=f"perm_vol_mass_{grupo}", min_value=0.0, value=1.0, format="%.3f", step=0.01)
                    
                    # Cálculo da Dose Total Q_initial
                    dose_total_grupo = conc_form * vol_or_mass_form
                    
                else: 
                    # Dose Infinita: campo oculto, Dose Total irrelevante
                    c2.markdown(f"**{T['perm_step1_label_donor_vol_mass']}**\n(N/A - {T['perm_step1_type_infinite']})")
                    dose_total_grupo = 1.0 # Valor dummy > 0 para evitar ZeroDivisionError no cálculo de %

                doses_dict[grupo] = {'dose_total': dose_total_grupo} 
                c0_dict[grupo] = conc_form 

            st.markdown("---")
            if st.button(T['step1_button_process'], type="primary", key="perm_process"):
                with st.spinner(T['step1_spinner_process']):
                    df_long = df_wide.melt(id_vars=[col_amostra_nome, col_grupo], value_vars=cols_tempo, var_name='Tempo', value_name='Area')
                    df_long['Tempo'] = pd.to_numeric(df_long['Tempo'], errors='coerce')
                    df_long['Area'] = pd.to_numeric(df_long['Area'], errors='coerce')
                    df_long = df_long.dropna(subset=['Tempo', 'Area'], how='any')
                    
                    if unidade_tempo == T['step1_time_minutes']:
                        df_long['Tempo'] = df_long['Tempo'] / 60
                    
                    col_conc_nome = f"{T['step1_col_conc_name']} ({unidade_conc})"
                    col_q_acumulada_nome = f"{T['step1_col_q_name']} ({unidade_massa})"
                    col_percent_nome = T['step1_col_pct_name'] 

                    # Reutiliza calcular_liberacao_replica_v9 do m_release
                    df_long_processado = df_long.groupby(col_amostra_nome).apply(
                        calcular_liberacao_replica_v9,
                        include_groups=False, 
                        col_grupo=col_grupo, vol_celula=vol_celula,
                        vol_amostra=vol_amostra, cal_a=cal_a, cal_b=cal_b,
                        doses_dict=doses_dict, col_conc=col_conc_nome,
                        col_q_acumulada=col_q_acumulada_nome,
                        col_percent=col_percent_nome
                    )
                    
                    df_long_processado = df_long_processado.reset_index()
                    
                    df_agregado = df_long_processado.groupby([col_grupo, 'Tempo']).agg(
                        Média_Q_Acumulada=(col_q_acumulada_nome, 'mean'),
                        SD_Q_Acumulada=(col_q_acumulada_nome, 'std'),
                        Média_Percent=(col_percent_nome, 'mean'),
                        SD_Percent=(col_percent_nome, 'std')
                    ).reset_index()
                    
                    df_agregado = df_agregado.fillna(0)
                    st.session_state.df_long_processado = df_long_processado
                    st.session_state.df_agregado = df_agregado
                    
                    config_dict = {
                        'unidade_massa': unidade_massa,
                        'unidade_conc': unidade_conc,
                        'col_q_acumulada': col_q_acumulada_nome,
                        'col_percent': col_percent_nome,
                        'col_conc': col_conc_nome,
                        'col_grupo': col_grupo,
                        'col_amostra_nome': col_amostra_nome,
                        'vol_celula': vol_celula,
                        'vol_amostra': vol_amostra,
                        'unidade_vol': unidade_vol,
                        'membrane_area': membrane_area,
                        'membrane_thickness': membrane_thickness,
                        'c0_dict': c0_dict, 
                        'dose_type': dose_type, 
                        'unidade_aplicada': unidade_aplicada, 
                        'y_label': f"{T['perm_y_label_q']} ({unidade_massa})",
                        'y_axis_mean': 'Média_Q_Acumulada',
                        'y_axis_sd': 'SD_Q_Acumulada',
                        'y_axis_col': col_q_acumulada_nome,
                    }
                    
                    st.session_state.config = config_dict
                    st.success(T['step1_success_process'])
        except Exception as e:
            st.error(f"{T['step1_error_process']} {e}")

def render_perm_step2(T):
    st.header(T['perm_step2_header'])
    if st.session_state.df_long_processado is None:
        st.warning(T['step2_warning_process'])
        return
    st.info(T['perm_step2_info'])
    
    st.subheader(T['step2_subheader_raw'])
    # FIX V62: width='stretch'
    st.dataframe(st.session_state.df_long_processado, width='stretch')
    get_download_button(st.session_state.df_long_processado, T, "dados_permeacao_replicas.csv", "dados_permeacao_replicas.xlsx")

    st.subheader(T['step2_subheader_agg'])
    # FIX V62: width='stretch'
    st.dataframe(st.session_state.df_agregado, width='stretch')
    get_download_button(st.session_state.df_agregado, T, "dados_permeacao_agregados.csv", "dados_permeacao_agregados.xlsx")

def render_perm_step3(T):
    st.header(T['perm_step3_header'])
    
    if st.session_state.df_agregado is None:
        st.warning(T['step2_warning_process'])
        return

    df_agg = st.session_state.df_agregado
    config = st.session_state.config
    col_grupo = config['col_grupo']
    grupos_disponiveis = df_agg[col_grupo].unique()
    
    y_axis_mean = config['y_axis_mean']
    y_axis_sd = config['y_axis_sd']
    y_label = config['y_label']

    st.info(T['perm_step3_info'])

    color_map = {}
    default_colors = px.colors.qualitative.Plotly
    with st.expander(T['step3_color_picker_label']):
        for i, grupo in enumerate(grupos_disponiveis):
            default_color = default_colors[i % len(default_colors)]
            if f"perm_color_{grupo}" not in st.session_state:
                st.session_state[f"perm_color_{grupo}"] = default_color
            
            st.session_state[f"perm_color_{grupo}"] = st.color_picker(
                f"{T['step3_color_picker_group']} {grupo}", 
                value=st.session_state[f"perm_color_{grupo}"], 
                key=f"color_picker_{grupo}"
            )
            color_map[grupo] = st.session_state[f"perm_color_{grupo}"]

    
    fig_comparativo = go.Figure()
    
    for i, grupo in enumerate(grupos_disponiveis):
        df_grupo = df_agg[df_agg[col_grupo] == grupo]
        cor_hex = color_map.get(grupo)
        
        fig_comparativo.add_trace(go.Scatter(
            x=df_grupo['Tempo'], y=df_grupo[y_axis_mean],
            mode='lines+markers', name=grupo,
            line=dict(color=cor_hex, width=2),
            marker=dict(size=8),
            error_y=dict(
                type='data', array=df_grupo[y_axis_sd].fillna(0),
                visible=True, thickness=1.5, width=3
            )
        ))

    fig_comparativo.update_layout(
        title=T['step3_title_compare'],
        xaxis_title=T['step3_xaxis_label'], yaxis_title=y_label,
        template="plotly_white", 
        height=500,
        xaxis_mirror=True, yaxis_mirror=True, 
        xaxis_linewidth=1, yaxis_linewidth=1,
        xaxis_linecolor='black', yaxis_linecolor='black',
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=50, r=50, t=50, b=150) 
    )
    # CORREÇÃO: Substitui width='stretch' por use_container_width=True e usa config
    st.plotly_chart(fig_comparativo, use_container_width=True, config=PLOTLY_CONFIG)

def render_perm_step4(T):
    st.header(T['perm_step4_header'])
    
    if st.session_state.df_agregado is None:
        st.warning(T['step2_warning_process'])
        return
        
    st.info(T['perm_step4_info'])

    df_agg = st.session_state.df_agregado
    config = st.session_state.config
    col_grupo = config['col_grupo']
    grupos_disponiveis = df_agg[col_grupo].unique()
    y_axis_mean = config['y_axis_mean']
    y_label = config['y_label']
    dose_type = config.get('dose_type', T['perm_step1_type_infinite'])
    
    # --- INSTRUÇÕES EXPLICATIVAS (CORRIGIDO PARA LINGUAGEM) ---
    st.markdown(f"### 🔍 {T['sequence_analysis']}")
    st.markdown(f"""
    1.  **{T['perm_step4_selectbox_group']}**
    2.  **{T['adjust_slider_label']}** to isolate the **linear phase** (Steady-State) of the permeation profile.
    3.  Observe the **{T['perm_step4_r2']}** of the fit and the {T['perm_param_jss']} calculated.
    4.  Click on **"{T['perm_step4_button_save']}"** to store the parameters for P-Step 5 ({T['perm_step5_tab_summary']} and {T['perm_step5_tab_stats']}).
    """)
    st.markdown("---")
    # --- FIM DAS INSTRUÇÕES ---
    
    # CORREÇÃO V60: Usando a tradução correta para o seletor
    grupo_selecionado = st.selectbox(T['perm_step4_selectbox_group'], grupos_disponiveis, key="perm_grup_select_4")
    
    if dose_type == T['perm_step1_type_finite']:
        st.warning(T['perm_step4_warning_dose'], icon="⚠️")

    if grupo_selecionado:
        df_grupo = df_agg[df_agg[col_grupo] == grupo_selecionado].copy()
        df_grupo = df_grupo[df_grupo[y_axis_mean] >= 0] 
        
        if len(df_grupo) < 2:
            st.error(T['perm_step4_error_points'])
            return

        min_time = float(df_grupo['Tempo'].min())
        max_time = float(df_grupo['Tempo'].max())
        
        default_range = (min_time, max_time)
        if len(df_grupo['Tempo']) >= 3:
             default_range = (df_grupo['Tempo'].iloc[1], max_time) if len(df_grupo['Tempo']) > 1 else (min_time, max_time)
        
        # CORREÇÃO: Removendo o argumento 'step' do st.select_slider
        time_range = st.select_slider(
            T['perm_step4_slider_label'],
            options=list(df_grupo['Tempo']),
            value=default_range,
            key="perm_time_slider"
        )
        
        df_fit = df_grupo[
            (df_grupo['Tempo'] >= time_range[0]) & 
            (df_grupo['Tempo'] <= time_range[1])
        ]
        
        t_data_fit = df_fit['Tempo']
        q_data_fit = df_fit[y_axis_mean]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_grupo['Tempo'], y=df_grupo[y_axis_mean],
            mode='markers', name=T['perm_step4_plot_data'],
            marker=dict(color='blue', size=10)
        ))
        
        # Variáveis de cálculo
        slope, intercept, r2, t_lag, jss, kp, d_coeff = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        fit_success = False

        if len(df_fit) >= 2:
            try:
                fit_results = stats.linregress(t_data_fit, q_data_fit)
                
                slope = fit_results.slope
                intercept = fit_results.intercept
                r2 = fit_results.rvalue**2
                
                # --- Cálculo dos Parâmetros ---
                area = config.get('membrane_area', 0.0)
                thickness = config.get('membrane_thickness', 0.0)
                c0 = config.get('c0_dict', {}).get(grupo_selecionado, 0.0)
                massa_unit = config.get('unidade_massa', 'unid.')
                conc_unit = config.get('unidade_conc', 'unid./mL')

                jss = slope / area if area > 0 else 0.0
                t_lag = -intercept / slope if slope != 0 else 0.0
                t_lag = max(t_lag, 0)
                kp = jss / c0 if c0 > 0 and jss != 0 else 0.0
                d_coeff = (thickness**2) / (6 * t_lag) if t_lag > 0 and thickness > 0 else 0.0
                
                # Salva resultados no estado para uso posterior
                st.session_state.fit_results = fit_results
                st.session_state.current_perm_group = grupo_selecionado
                st.session_state.current_time_range = time_range 
                
                fit_success = True
                
                # Extrapolação da linha (do tempo 0 até o tempo final)
                t_extrapol = np.array([0, max_time]) 
                q_extrapol = intercept + slope * t_extrapol
                
                fig.add_trace(go.Scatter(
                    x=t_extrapol, y=q_extrapol,
                    mode='lines', name=T['perm_step4_plot_fit'],
                    line=dict(color='red', dash='dash')
                ))
                
                fig.add_trace(go.Scatter(
                    x=t_data_fit, y=q_data_fit,
                    mode='markers', name=T.get('pontos_usados', "Pontos Usados"), 
                    marker=dict(color='red', size=12, symbol='cross')
                ))

            except Exception as e:
                st.error(f"{T['perm_step4_error_fit']} (Erro: {e})")
                st.session_state.fit_results = None
        else:
            st.warning(T['perm_step4_error_fit'])
            st.session_state.fit_results = None

        # CORREÇÃO V60: Títulos do gráfico
        fig.update_layout(
            title=f"{T['perm_step4_plot_title']} {grupo_selecionado}",
            xaxis_title=T['step3_xaxis_label'], yaxis_title=y_label,
            template="plotly_white",
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)
        )
        # CORREÇÃO: Substitui width='stretch' por use_container_width=True e usa config
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

        if fit_success:
            st.subheader(T['perm_step4_subheader_fit'])
            c1, c2, c3 = st.columns(3)
            # CORREÇÃO V60: Métricas
            c1.metric(T['perm_step4_r2'], f"{r2:.4f}")
            c2.metric(T['perm_step4_slope'], f"{slope:.4f}")
            c3.metric(T['perm_step4_intercept'], f"{intercept:.4f}")

            st.markdown("---")

            # --- EXIBIÇÃO DOS PARÂMETROS CALCULADOS ---
            st.subheader(f"{T['perm_step4_subheader_params']} **{grupo_selecionado}**")
            
            col_jss, col_lag = st.columns(2)
            col_kp, col_d = st.columns(2)
            
            col_jss.metric(T['perm_param_jss'], f"{jss:.4f}", f"{massa_unit} / (h⋅cm²)")
            col_lag.metric(T['perm_param_lag'], f"{t_lag:.4f}", "h")
            col_kp.metric(T['perm_param_kp'], f"{kp:.4f}", "cm/h")
            col_d.metric(T['perm_param_d'], f"{d_coeff:.2e}", "cm²/h")
            
            # CORREÇÃO V63: Usando o título traduzido
            st.markdown(f"### {T['perm_step4_methodology_header']}")
            
            # CORREÇÃO V61: Fórmula LaTeX em formato RAW f-string (rf) para evitar SyntaxWarning
            slope_label = T['perm_step4_slope']
            intercept_label = T['perm_step4_intercept']
            
            # O uso de rf""" garante que \text, \frac, etc. funcionem corretamente como comandos LaTeX
            st.markdown(rf"""
            * **{T['perm_param_jss']} ($\mathbf{{J_{{ss}}}}$):** Calculado como $\text{{Slope}} / \text{{Área}} = ({slope:.4f} \ \text{{Qtd}}/\text{{h}}) / ({area:.2f} \ \text{{cm}}^2)$.
            * **{T['perm_param_lag']} ($\mathbf{{T_{{lag}}}}$):** $\mathbf{{T_{{lag}}}} = - \frac{{\text{{{intercept_label}}}}}{{\text{{{slope_label}}}}} \approx {t_lag:.4f} \ \text{{h}}$.
            * **{T['perm_param_d']} ($\mathbf{{D}}$):** $\mathbf{{D}} = h^2 / (6 \cdot T_{{lag}})$, onde $h$ é a espessura ($h = {thickness:.4f} \ \text{{cm}}$).
            * **{T['perm_param_kp']} ($\mathbf{{K_p}}$):** $\mathbf{{K_p}} = J_{{ss}} / C_{{0}}$, onde $\mathbf{{C_{{0}}}} = {c0:.2f} \ {conc_unit}$.
            """)

            if st.button(T['perm_step4_button_save'], type="primary"):
                if 'perm_results' not in st.session_state:
                    st.session_state.perm_results = {}
                    
                results_to_save = {
                    T['perm_step5_col_jss']: jss,
                    T['perm_step5_col_lag']: t_lag,
                    T['perm_step5_col_kp']: kp,
                    T['perm_step5_col_d']: d_coeff,
                    T['perm_step5_col_r2']: r2
                }
                
                st.session_state.perm_results[grupo_selecionado] = results_to_save
                st.success(f"{T['perm_step4_save_success']} **{grupo_selecionado}**")


def render_perm_step5(T):
    st.header(T['perm_step5_header'])
    
    if st.session_state.df_agregado is None:
        st.warning(T['step2_warning_process'])
        return

    # Nomes das abas em Português
    tab_summary, tab_stats = st.tabs([
        T['perm_step5_tab_summary'], 
        T['perm_step5_tab_stats']
    ])

    df_agg = st.session_state.df_agregado
    df_long = st.session_state.df_long_processado
    config = st.session_state.config
    col_grupo = config['col_grupo']
    y_axis_col = config['y_axis_col']
    col_amostra = config['col_amostra_nome']
    grupos_disponiveis = df_agg[col_grupo].unique()
    area = config.get('membrane_area', 0.0)
    thickness = config.get('membrane_thickness', 0.0)

    with tab_summary:
        st.info(T['perm_step5_info'])
        
        if 'perm_results' not in st.session_state or not st.session_state.perm_results:
            st.info(T['perm_step5_empty'])
            return
        
        df_resumo_perm = pd.DataFrame.from_dict(st.session_state.perm_results, orient='index')
        df_resumo_perm.index.name = T['perm_step5_col_group']
        
        format_dict = {
            T['perm_step5_col_jss']: "{:.4f}",
            T['perm_step5_col_lag']: "{:.4f}",
            T['perm_step5_col_kp']: "{:.4f}",
            T['perm_step5_col_d']: "{:.2e}",
            T['perm_step5_col_r2']: "{:.4f}",
        }
        
        # FIX V62: width='stretch'
        st.dataframe(
            df_resumo_perm.style.format(format_dict, na_rep="-"),
            width='stretch'
        )
        
        get_download_button(df_resumo_perm, T, "resumo_permeacao.csv", "resumo_permeacao.xlsx")

    with tab_stats:
        st.subheader(T['perm_stats_header'])
        st.info(T['perm_stats_info'])
        
        # 1. Seleção de Grupos
        grupos_selecionados_stats = st.multiselect(T['perm_stats_select_groups'], grupos_disponiveis)
        
        # 2. Seleção de Parâmetro
        param_options = {
            T['perm_stats_param_jss']: 'Jss',
            T['perm_stats_param_lag']: 'T_lag',
            T['perm_stats_param_kp']: 'Kp',
            T['perm_stats_param_d']: 'D'
        }
        param_selecionado_str = st.selectbox(T['perm_stats_select_param'], list(param_options.keys()), key='stats_param_select')
        param_key = param_options.get(param_selecionado_str, 'Jss')

        # 3. Definição do Intervalo Comum
        tempos_disponiveis = df_long['Tempo'].unique()
        tempos_disponiveis = np.sort(tempos_disponiveis[tempos_disponiveis > 0]) # Exclui T=0
        
        if len(tempos_disponiveis) >= 2:
            min_t_total = tempos_disponiveis.min()
            max_t_total = tempos_disponiveis.max()
            default_t_stats = (min_t_total, max_t_total)
            
            # CORREÇÃO: Removendo a lógica complexa de step_val e usando um passo fixo
            time_range_stats = st.slider(
                T['perm_stats_select_time_range'],
                min_value=min_t_total,
                max_value=max_t_total,
                value=default_t_stats,
                step=0.5, # Usar um passo fixo razoável
                key='stats_time_slider'
            )
        else:
            st.warning("Dados insuficientes no eixo do tempo para análise estatística.")
            return

        # 4. Botão de Análise
        if st.button(T['perm_stats_button'], type="primary"):
            if len(grupos_selecionados_stats) < 2:
                st.error("Selecione pelo menos 2 grupos para comparar.")
                return

            dados_param_replicas = []
            grupos_validos = True

            with st.spinner(f"Calculando {param_key} das réplicas e rodando teste estatístico..."):
                for grupo in grupos_selecionados_stats:
                    replicas_param = []
                    c0_grupo = config.get('c0_dict', {}).get(grupo, 0.0)
                    
                    replicas_do_grupo = df_long[df_long[col_grupo] == grupo][col_amostra].unique()
                    
                    for replica_id in replicas_do_grupo:
                        df_replica = df_long[
                            (df_long[col_amostra] == replica_id) &
                            (df_long['Tempo'] >= time_range_stats[0]) & 
                            (df_long['Tempo'] <= time_range_stats[1])
                        ].sort_values(by='Tempo')
                        
                        if len(df_replica) >= 2:
                            params = calculate_perm_params_replica(df_replica, area, thickness, c0_grupo, y_axis_col)
                            
                            if params and params[param_key] is not None:
                                replicas_param.append(params[param_key])
                            else:
                                pass 
                        else:
                            pass 
                    
                    if len(replicas_param) < 2:
                        grupos_validos = False
                        st.error(f"{T['perm_stats_error_replicas']} (Grupo: {grupo}). Apenas {len(replicas_param)} réplicas válidas encontradas.")
                        break
                    
                    if len(replicas_param) > 0:
                        dados_param_replicas.append(np.array(replicas_param))
                    else:
                        grupos_validos = False
                        st.error(f"{T['perm_stats_error_no_data']} (Grupo: {grupo})")
                        break


            if grupos_validos:
                st.subheader(T['perm_stats_results'])
                
                # Teste Estatístico
                if len(dados_param_replicas) == 2:
                    stat, p_value = stats.ttest_ind(dados_param_replicas[0], dados_param_replicas[1], equal_var=False) 
                    label_teste = f"{T['perm_stats_ttest']} (2 Grupos)"
                else:
                    stat, p_value = stats.f_oneway(*dados_param_replicas)
                    label_teste = f"{T['perm_stats_anova']} (>2 Grupos)"
                
                # Formatação do p-valor
                if p_value < 0.0001:
                    p_valor_formatado_str = "< 0.0001"
                    p_valor_formatado_desc = "(p < 0.0001)"
                else:
                    p_valor_formatado_str = f"{p_value:.5f}" 
                    p_valor_formatado_desc = f"(p = {p_value:.5f})" 
                
                st.metric(label=label_teste, value=p_valor_formatado_str)
                
                if p_value < 0.05:
                    st.success(f"**{T['perm_stats_conclusion_sig']}** {p_valor_formatado_desc}")
                else:
                    st.info(f"**{T['perm_stats_conclusion_nonsig']}** {p_valor_formatado_desc}")


# --- MÓDULO DE PERMEAÇÃO - App Principal ---
def render_permeation_app():
    T = TEXT_DICT[st.session_state.lang]
    st.sidebar.info(T['perm_sidebar_info']) # USA A INFORMAÇÃO SIMPLIFICADA
    pagina_opcoes = [
        T['perm_nav_step1'], T['perm_nav_step2'], T['perm_nav_step3'],
        T['perm_nav_step4'], T['perm_nav_step5']
    ]
    pagina = st.sidebar.radio(f"Navegação do Módulo Permeação ({st.session_state.lang.upper()})", pagina_opcoes, key="perm_nav") 
    
    # --- MUDANÇA: Botão de Retorno Movido para Cima e Corrigido para i18n ---
    # CORREÇÃO: T['home_footer'] agora está acessível no dicionário local
    if st.sidebar.button(T['home_footer']): 
        st.session_state.app_mode = 'home'
        st.rerun()
        
    st.sidebar.markdown("---") # Linha divisória após o botão de retorno
    
    if pagina == T['perm_nav_step1']:
        render_perm_step1(T)
    elif pagina == T['perm_nav_step2']:
        render_perm_step2(T)
    elif pagina == T['perm_nav_step3']:
        render_perm_step3(T)
    elif pagina == T['perm_nav_step4']:
        render_perm_step4(T)
    elif pagina == T['perm_nav_step5']:
        render_perm_step5(T)