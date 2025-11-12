import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from scipy import stats 
import warnings
import io 
# Não precisamos do xlsxwriter aqui, pois o Pandas Streamlit já o utiliza internamente para o download.

# --- Dicionário de Tradução (i18n) - MÓDULO RELEASE ---
# Contém apenas as chaves específicas do módulo Release.
TEXT_DICT = {
    'pt': {
        'release_sidebar_info': "Módulo de Liberação", # SIMPLIFICADO
        'nav_step1': "Etapa 1: Configuração e Upload",
        'nav_step2': "Etapa 2: Dados Processados e Agregados",
        'nav_step3': "Etapa 3: Gráficos de Liberação",
        'nav_step4': "Etapa 4: Modelagem Cinética",
        'nav_step5': "Etapa 5: Análise Comparativa", 
        'nav_step6': "Etapa 6: Análise por IA (Gerar Prompt)", 
        
        'step1_header': "Etapa 1: Configuração e Upload (Liberação)",
        'step1_subheader_units': "Unidades Globais",
        'step1_label_vol_unit': "Unidade de Volume",
        'step1_label_conc_unit': "Unidade de Concentração",
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
        'step1_expander_model': "Ver Modelo de Referência da Planilha",
        'step1_uploader_label': "Carregue seu arquivo",
        'step1_csv_options': "Opções de leitura de CSV/TXT detectadas:",
        'step1_csv_sep': "Separador de Coluna",
        'step1_csv_sep_semi': "; (Ponto e Vírgula)",
        'step1_csv_sep_comma': ", (Vírgula)",
        'step1_csv_sep_tab': "Tab",
        'step1_csv_dec': "Separador Decimal",
        'step1_csv_dec_comma': ", (Vírgula)",
        'step1_csv_dec_point': ". (Ponto)",
        'step1_error_calib_a': "O Coeficiente Angular (a) da calibração não pode ser zero.",
        'step1_upload_preview': "Dados Carregados (Pré-visualização):",
        'step1_subheader_dose': "Configurações da Formulação (Dose por Grupo)",
        'step1_dose_group': "Grupo:",
        'step1_dose_conc': "Concentração",
        'step1_dose_vol': "Volume Adicionado",
        'step1_button_process': "Processar Dados",
        'step1_spinner_process': "Processando...",
        'step1_success_process': "Dados processados! Navegue para a 'Etapa 2'.",
        'step1_error_process': "Erro ao ler ou processar o arquivo:",
        'step1_col_conc_name': "Concentracao",
        'step1_col_q_name': "Q_Acumulada_Corrigida",
        'step1_col_pct_name': "Percent_Liberado (%)",
        'step1_y_label_pct': "Fármaco Liberado (%)",
        'step1_y_label_q': "Quantidade Acumulada",

        'step2_header': "Etapa 2: Análise de Dados Processados",
        'step2_warning_process': "Por favor, carregue e processe os dados na 'Etapa 1' primeiro.",
        'step2_info': "Resultados dos cálculos. A 'Tabela Agregada' é usada para gráficos e modelagem.",
        'step2_subheader_raw': "1. Tabela de Dados Processados (Por Réplica)",
        'step2_subheader_agg': "2. Tabela de Dados Agregados (Média e Desvio Padrão)",
        'download_excel': "Baixar como Excel",

        'step3_header': "Etapa 3: Gráficos de Liberação",
        'step3_info_export': "Use o ícone de câmera 📷 no canto superior direito dos gráficos (ao passar o mouse) para exportá-los como PNG.",
        'step3_subheader_individual': "1. Análise de Grupo Individual (com Desvio Padrão)",
        'step3_selectbox_group': "Selecione o Grupo para Análise:",
        'step3_legend_individual': "Média (± SD)",
        'step3_title_individual': "Perfil de Liberação (Média ± SD) para:",
        'step3_xaxis_label': "Tempo (horas)",
        'step3_subheader_compare': "2. Gráfico Comparativo (Médias de Todos os Grupos com Desvio Padrão)",
        'step3_title_compare': "Comparação dos Perfis de Liberação (Média ± SD)",
        'step3_color_picker_label': "Personalizar Cores (Gráfico Comparativo)",
        'step3_color_picker_group': "Cor para",

        'step4_header': "Etapa 4: Modelagem Cinética",
        'step4_info_model': "A modelagem é realizada sobre os dados de **Média** do grupo selecionado.",
        'step4_selectbox_group': "Selecione o Grupo para Modelagem:",
        'step4_checkbox_label_t0': "Excluir o ponto (0,0) da modelagem (Recomendado)", # NOVO V50
        'step4_checkbox_help_t0': "A inclusão do ponto (t=0, Q=0) pode distorcer o ajuste ao 'puxar' a curva para a origem, inflando artificialmente o R² e prejudicando a descrição do mecanismo real de liberação (t > 0).", # NOVO V50
        'step4_error_points': "Pontos de dados insuficientes (mínimo 3) para modelar.", # ATUALIZADO V50
        'step4_error_fit': "Nenhum modelo pôde ser ajustado.",
        'step4_subheader_results': "Resultados da Modelagem para:",
        'step4_subheader_plot': "Gráfico de Ajuste dos Modelos",
        'step4_plot_experimental': "Dados Experimentais (Média)",
        'step4_subheader_interp': "Interpretação Automática (Detalhada)",
        'step4_success_model': "O modelo com melhor ajuste (maior R²) é:",
        'step4_interp_params': "Parâmetros:",
        'step4_interp_const': "Constante (k ou a):",
        'step4_interp_exp': "Expoente (n ou b):",
        'step4_interp_interp': "Interpretação:",
        'step4_glossary_header': "Glossário do Mecanismo",
        'step4_glossary_fickian': "Significado: A taxa de liberação é controlada pela difusão do fármaco através da matriz (ex: gel, polímero). A velocidade de liberação diminui com o tempo à medida que a concentração de fármaco diminui. É proporcional à raiz quadrada do tempo (Modelo de Higuchi).",
        'step4_glossary_anomalous': "Significado: A liberação é controlada por uma *combinação* de dois mecanismos: (1) a difusão do fármaco (Fickiana) e (2) o inchaço (swelling) ou relaxamento das cadeias do polímero. É comum em hidrogéis e sistemas poliméricos.",
        'step4_glossary_case_ii': "Significado: A liberação é dominada *inteiramente* pelo relaxamento ou erosão da matriz polimérica. A difusão é muito rápida em comparação. Isso geralmente resulta em uma liberação de Ordem Zero (taxa constante).",
        'step4_glossary_zero_order': "Significado: A liberação ocorre a uma taxa constante, liberando a *mesma quantidade de fármaco por unidade de tempo*, independente da concentração restante. É o ideal para liberação controlada.",
        'step4_glossary_first_order': "Significado: A taxa de liberação é *dependente da concentração*. Ela é rápida no início (quando a concentração é alta) e diminui exponencialmente à medida que o fármaco é liberado. Típico de sistemas onde o fármaco está dissolvido na matriz.",
        'step4_glossary_hixson': "Significado: Este modelo descreve a liberação de fármacos onde a *área de superfície* do sistema diminui com o tempo. É típico de sistemas que se dissolvem ou erodem uniformemente (ex: comprimidos que se dissolvem).",
        'step4_glossary_peppas_sahlin': "Significado: Este é um modelo bifásico que *separa* os mecanismos. Ele quantifica a contribuição da Difusão Fickiana (k_diff, dependente de t^0.5) e do Relaxamento da Matriz (k_relax, dependente de t). Se k_diff > k_relax, a difusão domina. Se k_relax > k_diff, o inchaço/relaxamento da matriz domina.",
        'step4_glossary_complex': "Significado: A liberação não segue um único mecanismo claro, but sim uma combinação de vários processos (ex: difusão, erosão, inchaço) de forma simultânea.",
        'step4_glossary_select': "Selecione um grupo para ver a interpretação do mecanismo.",

        'step5_header': "Etapa 5: Análise Comparativa",
        'step5_info': "Use as abas abaixo para comparar seus grupos usando diferentes métodos.",
        'step5_tab_summary': "Resumo Cinético e AUC", 
        'step5_tab_stats': "Análise Estatística (ANOVA/t-test)",
        'step5_tab_f2': "Fator de Similaridade (f₂)",
        'step5_summary_info': "Resumo dos parâmetros independentes de modelo (AUC, Ponto Final) e do melhor modelo cinético (maior R²) para cada grupo.",
        'step5_spinner': "Analisando todos os grupos...",
        'step5_col_group': "Grupo",
        'step5_col_auc': "AUC", 
        'step5_col_release_final': "Liberacao_Final", 
        'step5_col_model': "Melhor_Modelo",
        'step5_col_r2': "R2",
        'step5_col_k': "Constante_1 (k ou a)",
        'step5_col_k_unit': "Unidade_k1",
        'step5_col_k2': "Constante_2 (k2 ou b)",
        'step5_col_k2_unit': "Unidade_k2",
        'step5_col_n': "Expoente (n)",
        'step5_col_interp': "Interpretação",
        'step5_error_data': "Dados insuficientes.",
        'step5_stats_header': "Comparação Estatística (t-test ou ANOVA)",
        'step5_stats_info': "Esta análise usa os dados de *réplica* (não a média) para determinar se a diferença entre os grupos é estatisticamente significante (p < 0.05).",
        'step5_stats_select_groups': "Selecione os grupos para comparar (2 ou mais):",
        'step5_stats_select_time': "Selecione o parâmetro para comparar:",
        'step5_stats_time_final': "Último ponto de tempo",
        'step5_stats_auc': "AUC (Área Sob a Curva)",
        'step5_stats_button': "Rodar Análise Estatística",
        'step5_stats_results': "Resultados da Análise",
        'step5_stats_ttest': "Teste t (2 Grupos)",
        'step5_stats_anova': "ANOVA (>2 Grupos)",
        'step5_stats_p_value': "Valor-p",
        'step5_stats_conclusion_sig': "SIGNIFICANTE: A diferença entre os grupos é estatisticamente significante (p < 0.05).",
        'step5_stats_conclusion_nonsig': "NÃO SIGNIFICANTE: A diferença entre os grupos não é estatisticamente significante (p >= 0.05).",
        'step5_stats_error_replicas': "Erro: Pelo menos um dos grupos selecionados não possui réplicas suficientes (mínimo 2) para um teste estatístico.",
        'step5_f2_header': "Cálculo do Fator de Similaridade (f₂)",
        'step5_f2_info': "O fator f₂ é um método da FDA/EMA para comparar perfis. Um valor de f₂ entre 50 e 100 sugere que os dois perfis são similares.",
        'step5_f2_ref': "Selecione o Grupo de Referência (R):",
        'step5_f2_test': "Selecione o Grupo de Teste (T):",
        'step5_f2_button': "Calcular f₂",
        'step5_f2_result_sim': "SIMILARES (f₂ = {:.2f})",
        'step5_f2_result_nonsim': "NÃO SIMILARES (f₂ = {:.2f})",
        'step5_f2_error': "Erro: Os grupos devem ser diferentes.",
        'step5_f2_error_points': "Erro: Não há pontos de tempo em comum (excluindo t=0) entre os grupos.",
        'step5_f2_warning_rules': "Aviso: O cálculo padrão do f₂ tem regras estritas (ex: apenas um ponto > 85% de liberação). Este cálculo usa todos os pontos de tempo comuns (t>0) para uma estimativa.",

        'model_zero_order': "Ordem Zero",
        'model_first_order': "Primeira Ordem",
        'model_higuchi': "Higuchi",
        'model_korsmeyer': "Korsmeyer-Peppas",
        'model_hixson': "Hixson-Crowell",
        'model_weibull': "Weibull",
        'model_peppas_sahlin': "Peppas-Sahlin (Bifásico)",
        
        'interp_fail': "Falha na modelagem.",
        'interp_r2_fail': "Falha ao determinar R².",
        'interp_fickian': "Difusão Fickiana",
        'interp_anomalous': "Transporte Anômalo (Não-Fickiano)",
        'interp_case_ii': "Transporte Caso-II (Zero Ordem)",
        'interp_zero_order_mech': "Liberação a taxa constante",
        'interp_first_order_mech': "Liberação dependente da concentração",
        'interp_hixson_mech': "Liberação por dissolução/erosão da matriz",
        'interp_peppas_sahlin_mech': "Modelo bifásico (Difusão vs. Relaxamento)",
        'interp_complex': "Mecanismo complexo/combinado",
        
        'step6_header': "Etapa 6: Análise por IA (Gerador de Prompt)",
        'step6_info': "Esta etapa prepara um 'briefing' completo com seus dados. Copie o texto gerado e cole-o em um chat com uma IA (como o Gemini) para obter uma análise detalhada, pesquisa de literatura e redação de resultados.",
        'step6_subheader_context': "1. Forneça o Contexto do Estudo",
        'step6_label_drug': "Nome do Fármaco",
        'step6_label_system': "Veículo ou Sistema (ex: 'nanopartículas de PLGA', 'gel de quitosana')",
        'step6_label_objective': "Principal Objetivo ou Comparação (ex: 'Comparar F1 vs F2', 'Avaliar efeito do polímero')",
        'step6_label_medium': "Solução de Liberação (Meio)", 
        'step6_label_membrane': "Membrana Utilizada (ex: acetato de celulose)", 
        'step6_button_generate': "Gerar Prompt de Análise para IA",
        'step6_prompt_header': "Seu Prompt de IA (Pronto para Copiar):",
        'step6_copy_success': "Prompt gerado com sucesso! Copie o texto abaixo e cole no seu chat de IA.",
        
        'prompt_title': "### Análise de Estudo de Liberação de Fármaco (Células de Franz)",
        'prompt_context_header': "### 1. Contexto do Estudo",
        'prompt_context_drug': "Fármaco",
        'prompt_context_system': "Sistema/Veículo",
        'prompt_context_objective': "Objetivo Principal",
        'prompt_methods_header': "### 2. Parâmetros Metodológicos (Resumido)",
        'prompt_methods_vol_receptor': "Volume da Célula Receptora",
        'prompt_methods_vol_sample': "Volume da Amostra Coletada",
        'prompt_methods_medium': "Meio de Liberação", 
        'prompt_methods_membrane': "Membrana", 
        'prompt_results_header': "### 3. Resultados de Liberação (Ponto Final)",
        'prompt_kinetics_header': "### 4. Resultados da Modelagem Cinética",
        'prompt_tasks_header': "### 5. Tarefas Solicitadas",
        'prompt_task_1': "1. **Redação de Metodologia:** Com base nos parâmetros, escreva uma seção de 'Metodologia' em formato de artigo científico para o ensaio de liberação *in vitro*.",
        'prompt_task_2': "2. **Pesquisa e Tabela de Literatura:** Com base no Fármaco e Sistema, pesquise na literatura por estudos semelhantes. Crie uma tabela comparando os resultados da literatura (especialmente o mecanismo e a % de liberação) com os meus 'Resultado da Modelagem Cinética' (Tabela 4). **Importante: Inclua o DOI ou Link para cada artigo na tabela.**", 
        'prompt_task_3': "3. **Discussão dos Resultados:** Escreva uma 'Discussão' em formato de artigo. Analise os dados das Tabelas 3 e 4, explique o que o 'Melhor Modelo' (ex: Higuchi, Peppas-Sahlin) significa para cada formulação e compare os grupos entre si (e com a literatura da Tarefa 2), focando no 'Objetivo Principal'.",
        'home_footer': "Retornar à Seleção de Módulo", # <-- CORRIGIDO
    },
    'en': {
        'release_sidebar_info': "Release Module", # SIMPLIFICADO
        'nav_step1': "Step 1: Setup & Upload",
        'nav_step2': "Step 2: Processed & Aggregated Data",
        'nav_step3': "Step 3: Release Plots",
        'nav_step4': "Step 4: Kinetic Modeling",
        'nav_step5': "Step 5: Comparative Analysis",
        'nav_step6': "Step 6: AI Analysis (Prompt Generator)",
        
        'step1_header': "Step 1: Setup & Upload (Release)",
        'step1_subheader_units': "Global Units",
        'step1_label_vol_unit': "Volume Unit",
        'step1_label_conc_unit': "Concentration Unit",
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
        'step1_expander_model': "View Spreadsheet Reference Model",
        'step1_uploader_label': "Upload your file",
        'step1_csv_options': "Detected CSV/TXT reading options:",
        'step1_csv_sep': "Column Separator",
        'step1_csv_sep_semi': "; (Semicolon)",
        'step1_csv_sep_comma': ", (Comma)",
        'step1_csv_sep_tab': "Tab",
        'step1_csv_dec': "Decimal Separator",
        'step1_csv_dec_comma': ", (Comma)",
        'step1_csv_dec_point': ". (Point)",
        'step1_error_calib_a': "The calibration Slope (a) cannot be zero.",
        'step1_upload_preview': "Uploaded Data (Preview):",
        'step1_subheader_dose': "Formulation Settings (Dose per Group)",
        'step1_dose_group': "Group:",
        'step1_dose_conc': "Concentration",
        'step1_dose_vol': "Volume Added",
        'step1_button_process': "Process Data",
        'step1_spinner_process': "Processing...",
        'step1_success_process': "Data processed! Navigate to 'Step 2'.",
        'step1_error_process': "Error reading or processing file:",
        'step1_col_conc_name': "Concentration",
        'step1_col_q_name': "Q_Accumulated_Corrected",
        'step1_col_pct_name': "Percent_Released (%)",
        'step1_y_label_pct': "Drug Released (%)",
        'step1_y_label_q': "Cumulative Amount",

        'step2_header': "Step 2: Processed Data Analysis 📊",
        'step2_warning_process': "Please upload and process data in 'Step 1' first.",
        'step2_info': "Calculation results. The 'Aggregated Table' is used for plots and modeling.",
        'step2_subheader_raw': "1. Processed Data Table (Per Replicate)",
        'step2_subheader_agg': "2. Aggregated Data Table (Mean and Std Dev)",
        'download_excel': "Download as Excel",

        'step3_header': "Step 3: Release Plots 📈",
        'step3_info_export': "Use the camera icon 📷 in the top-right of the plots (on hover) to export them as PNG.",
        'step3_subheader_individual': "1. Individual Group Analysis (with Std Dev)",
        'step3_selectbox_group': "Select Group for Analysis:",
        'step3_legend_individual': "Mean (± SD)",
        'step3_title_individual': "Release Profile (Mean ± SD) for:",
        'step3_xaxis_label': "Time (hours)",
        'step3_subheader_compare': "2. Comparative Plot (All Group Means with Std Dev)",
        'step3_title_compare': "Comparison of Release Profiles (Mean ± SD)",
        'step3_color_picker_label': "Customize Colors (Comparative Plot)",
        'step3_color_picker_group': "Color for",

        'step4_header': "Step 4: Kinetic Modeling 🔬",
        'step4_info_model': "Modeling is performed on the **Mean** data of the selected group.",
        'step4_selectbox_group': "Select Group for Modeling:",
        'step4_checkbox_label_t0': "Exclude (0,0) point from modeling (Recommended)", # NOVO V50
        'step4_checkbox_help_t0': "Including the (t=0, Q=0) point can distort the fit by 'pulling' the curve to the origin, artificially inflating the R² and harming the description of the actual release mechanism (t > 0).", # NOVO V50
        'step4_error_points': "Insufficient data points (minimum 3) for modeling.", # ATUALIZADO V50
        'step4_error_fit': "No model could be fitted.",
        'step4_subheader_results': "Modeling Results for:",
        'step4_subheader_plot': "Model Fit Plot",
        'step4_plot_experimental': "Experimental Data (Mean)",
        'step4_subheader_interp': "Automatic Interpretation (Detailed)",
        'step4_success_model': "The best-fit model (highest R²) is:",
        'step4_interp_params': "Parameters:",
        'step4_interp_const': "Constant (k or a):",
        'step4_interp_exp': "Exponent (n or b):",
        'step4_interp_interp': "Interpretation:",
        'step4_glossary_header': "Mechanism Glossary",
        'step4_glossary_fickian': "Meaning: Release rate is controlled by drug diffusion through the matrix (e.g., gel, polymer). The release speed decreases over time as the drug concentration decreases. It is proportional to the square root of time (Higuchi Model).",
        'step4_glossary_anomalous': "Meaning: Release is controlled by a *combination* of two mechanisms: (1) drug diffusion (Fickian) and (2) polymer swelling or relaxation. Common in hydrogels and polymeric systems.",
        'step4_glossary_anomalous': "Meaning: Release is controlled by a *combination* of two mechanisms: (1) drug diffusion (Fickian) and (2) polymer swelling or relaxation. Common in hydrogels and polymeric systems.",
        'step4_glossary_case_ii': "Meaning: Release is dominated *entirely* by the relaxation or erosion of the polymer matrix. Diffusion is very fast in comparison. This often results in Zero-Order release (constant rate).",
        'step4_glossary_zero_order': "Meaning: Release occurs at a constant rate, releasing the *same amount of drug per unit of time*, independent of the remaining concentration. Ideal for controlled release.",
        'step4_glossary_first_order': "Meaning: The release rate is *concentration-dependent*. It is fast at the beginning (when concentration is high) and decreases exponentially as the drug is released. Typical for systems where the drug is dissolved in the matrix.",
        'step4_glossary_hixson': "Meaning: This model describes drug release where the *surface area* of the system decreases over time. Typical for systems that dissolve or erode uniformly (e.g., dissolving tablets).",
        'step4_glossary_peppas_sahlin': "Meaning: This is a biphasic model that *separates* the mechanisms. It quantifies the contribution of Fickian Diffusion (k_diff, dependent on t^0.5) and Matrix Relaxation (k_relax, dependent on t). If k_diff > k_relax, diffusion dominates. If k_relax > k_diff, swelling/relaxation dominates.",
        'step4_glossary_complex': "Meaning: The release does not follow a single clear mechanism, but rather a combination of several processes (e.g., diffusion, erosion, swelling) simultaneously.",
        'step4_glossary_select': "Select a group to see the mechanism interpretation.",
        
        'step5_header': "Step 5: Comparative Analysis 🏆",
        'step5_info': "Use the tabs below to compare your groups using different methods.",
        'step5_tab_summary': "Kinetic Summary & AUC",
        'step5_tab_stats': "Statistical Analysis (ANOVA/t-test)",
        'step5_tab_f2': "Similarity Factor (f₂)",
        'step5_summary_info': "Summary of model-independent parameters (AUC, Endpoint) and the best-fit kinetic model (highest R²) for each group.",
        'step5_spinner': "Analyzing all groups...",
        'step5_col_group': "Group",
        'step5_col_auc': "AUC",
        'step5_col_release_final': "Final_Release",
        'step5_col_model': "Best_Model",
        'step5_col_r2': "R2",
        'step5_col_k': "Constant_1 (k or a)",
        'step5_col_k_unit': "Unit_k1",
        'step5_col_k2': "Constant_2 (k2 or b)",
        'step5_col_k2_unit': "Unit_k2",
        'step5_col_n': "Exponent (n)",
        'step5_col_interp': "Interpretation",
        'step5_error_data': "Insufficient data.",
        'step5_stats_header': "Statistical Comparison (t-test or ANOVA)",
        'step5_stats_info': "This analysis uses *replicate* data (not the mean) to determine if the difference between groups is statistically significant (p < 0.05).",
        'step5_stats_select_groups': "Select groups to compare (2 or more):",
        'step5_stats_select_time': "Select parameter to compare:",
        'step5_stats_time_final': "Last time point",
        'step5_stats_auc': "AUC (Area Under the Curve)",
        'step5_stats_button': "Run Statistical Analysis",
        'step5_stats_results': "Analysis Results",
        'step5_stats_ttest': "t-test (2 Groups)",
        'step5_stats_anova': "ANOVA (>2 Groups)",
        'step5_stats_p_value': "p-value",
        'step5_stats_conclusion_sig': "SIGNIFICANT: The difference between the groups is statistically significant (p < 0.05).",
        'step5_stats_conclusion_nonsig': "NOT SIGNIFICANT: The difference between the groups is not statistically significant (p >= 0.05).",
        'step5_stats_error_replicas': "Error: At least one of the selected groups does not have enough replicates (minimum 2) for a statistical test.",
        'step5_f2_header': "Similarity Factor (f₂) Calculation",
        'step5_f2_info': "The f₂ factor is an FDA/EMA method for comparing profiles. An f₂ value between 50 and 100 suggests the two profiles are similar.",
        'step5_f2_ref': "Select Reference Group (R):",
        'step5_f2_test': "Select Test Group (T):",
        'step5_f2_button': "Calculate f₂",
        'step5_f2_result_sim': "SIMILAR (f₂ = {:.2f})",
        'step5_f2_result_nonsim': "NOT SIMILAR (f₂ = {:.2f})",
        'step5_f2_error': "Error: Groups must be different.",
        'step5_f2_error_points': "Error: No common time points (excluding t=0) between groups.",
        'step5_f2_warning_rules': "Warning: Standard f₂ calculation has strict rules (e.g., only one point > 85% release). This calculation uses all common time points (t>0) for an estimation.",

        'model_zero_order': "Zero-Order",
        'model_first_order': "First-Order",
        'model_higuchi': "Higuchi",
        'model_korsmeyer': "Korsmeyer-Peppas",
        'model_hixson': "Hixson-Crowell",
        'model_weibull': "Weibull",
        'model_peppas_sahlin': "Peppas-Sahlin (Biphasic)",
        
        'interp_fail': "Modeling failed.",
        'interp_r2_fail': "Failed to determine R².",
        'interp_fickian': "Fickian Diffusion",
        'interp_anomalous': "Anomalous Transport (Non-Fickian)",
        'interp_case_ii': "Case-II Transport (Zero-Order)",
        'interp_zero_order_mech': "Constant-rate release",
        'interp_first_order_mech': "Concentration-dependent release",
        'interp_hixson_mech': "Release by matrix dissolution/erosion",
        'interp_peppas_sahlin_mech': "Biphasic model (Diffusion vs. Relaxation)",
        'interp_complex': "Complex/combined mechanism",
        
        'step6_header': "Step 6: AI Analysis (Prompt Generator) 🤖",
        'step6_info': "This step prepares a complete briefing with your data. Copy the generated text and paste it into a chat with an AI (like Gemini) to get a detailed analysis, literature research, and results write-up.",
        'step6_subheader_context': "1. Provide Study Context",
        'step6_label_drug': "Drug Name",
        'step6_label_system': "Vehicle or System (e.g., 'PLGA nanoparticles', 'chitosan gel')",
        'step6_label_objective': "Main Objective or Comparison (e.g., 'Compare F1 vs F2', 'Evaluate effect of polymer')",
        'step6_label_medium': "Release Medium",
        'step6_label_membrane': "Membrane Used (e.g., cellulose acetate)",
        'step6_button_generate': "Generate AI Analysis Prompt",
        'step6_prompt_header': "Your AI Prompt (Ready to Copy):",
        'step6_copy_success': "Prompt generated successfully! Copy the text below and paste it into your AI chat.",
        
        'prompt_title': "### Drug Release Study Analysis (Franz Cells)",
        'prompt_context_header': "### 1. Study Context",
        'prompt_context_drug': "Drug",
        'prompt_context_system': "System/Vehicle",
        'prompt_context_objective': "Main Objective",
        'prompt_methods_header': "### 2. Methodological Parameters (Summary)",
        'prompt_methods_vol_receptor': "Receptor Cell Volume",
        'prompt_methods_vol_sample': "Collected Sample Volume",
        'prompt_methods_medium': "Release Medium",
        'prompt_methods_membrane': "Membrane",
        'prompt_results_header': "### 3. Release Results (Endpoint)",
        'prompt_kinetics_header': "### 4. Kinetic Modeling Results",
        'prompt_tasks_header': "### 5. Requested Tasks",
        'prompt_task_1': "1. **Methodology Write-up:** Based on the parameters, write a scientific article-style 'Methodology' section for the *in vitro* release assay.",
        'prompt_task_2': "2. **Literature Research & Table:** Based on the Drug and System, search the literature for similar studies. Create a table comparing the literature results (especially mechanism and % release) with my 'Kinetic Modeling Results' (Table 4). **Important: Include the DOI or Link for each article in the table.**",
        'prompt_task_3': "3. **Results Discussion:** Write an article-style 'Discussion'. Analyze the data from Tables 3 and 4, explain what the 'Best Model' (e.g., Higuchi, Peppas-Sahlin) means for each formulation, and compare the groups against each other (and with the literature from Task 2), focusing on the 'Main Objective'.",
        'home_footer': "Return to Module Selection", # <-- CORRIGIDO
    }
}

# --- Função de Carregamento de Dados ---
def load_data(uploaded_file, sep, decimal):
    """Tenta ler um CSV/TXT com codificações comuns."""
    try:
        return pd.read_csv(uploaded_file, sep=sep, decimal=decimal, encoding='utf-8')
    except UnicodeDecodeError:
        st.warning("Failed to read with UTF-8. Trying 'latin-1' encoding...")
        uploaded_file.seek(0) 
        return pd.read_csv(uploaded_file, sep=sep, decimal=decimal, encoding='latin-1')
    except Exception as e:
        st.error(f"Unexpected error reading file: {e}")
        return None

# --- Funções dos Modelos Cinéticos ---
def model_zero_order(t, k0): return k0 * t
def model_first_order(t, Q_inf, k1): return Q_inf * (1 - np.exp(-k1 * t))
def model_higuchi(t, kH): return kH * np.sqrt(t)
def model_korsmeyer_peppas(t, kKP, n): return kKP * (t**n)
def model_hixson_crowell(t, Q_inf, kHC):
    termo = 1 - kHC * t
    termo = np.where(termo < 0, 0, termo)
    return Q_inf * (1 - (termo)**3)
def model_weibull(t, Q_inf, a, b):
    t_a = t / a
    t_a = np.where(t_a <= 0, 1e-9, t_a)
    return Q_inf * (1 - np.exp(-(t_a**b)))
def model_peppas_sahlin(t, k_diff, k_relax):
    return (k_diff * np.sqrt(t)) + (k_relax * t)

# --- Função de Cálculo V9 (Liberação/Permeação) ---
def calcular_liberacao_replica_v9(df_group, col_grupo, vol_celula, vol_amostra, cal_a, cal_b, doses_dict, col_conc, col_q_acumulada, col_percent):
    df_group = df_group.sort_values(by='Tempo')
    grupo_da_replica = df_group[col_grupo].iloc[0]
    dose_total = doses_dict.get(grupo_da_replica, {}).get('dose_total', 0.0)
    df_group[col_conc] = (df_group['Area'] - cal_b) / cal_a
    
    df_group[col_conc] = df_group[col_conc].fillna(0)

    correcao_acumulada = 0
    q_acumulada_corrigida = []
    
    for i in range(len(df_group)):
        conc_atual = df_group.iloc[i][col_conc]
        
        if pd.isna(conc_atual):
            conc_atual = 0.0

        q_no_recipiente = conc_atual * vol_celula
        q_corrigida = q_no_recipiente + correcao_acumulada
        q_acumulada_corrigida.append(q_corrigida)
        correcao_acumulada += (conc_atual * vol_amostra)
        
    df_group[col_q_acumulada] = q_acumulada_corrigida
    
    if dose_total > 0:
        df_group[col_percent] = (df_group[col_q_acumulada] / dose_total) * 100
        df_group[col_percent] = df_group[col_percent].clip(lower=0)
        
        idx_100_series = (df_group[col_percent] > 99.9999)
        if idx_100_series.any():
            first_idx_100 = idx_100_series.idxmax()
            df_group.loc[first_idx_100:, col_percent] = 100.0
            
    else:
        df_group[col_percent] = 0.0
        
    return df_group

# --- Função de Modelagem V12 ---
def rodar_modelagem_v12(t_data, q_data, df_model, y_axis_mean, has_dose_info):
    resultados_df_list = []
    modeling_messages = []
    
    R2_THRESHOLD = 0.05
    q_max = q_data.max()
    if q_max == 0: q_max = 1.0
    t_data = np.array(t_data)
    q_data = np.array(q_data)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        limite_kp = 60.0 if has_dose_info else q_max * 0.6
        df_kp = df_model[df_model[y_axis_mean] <= limite_kp]
        t_data_kp = df_kp["Tempo"]
        q_data_kp = df_kp[y_axis_mean]

        # Modelo 4: Korsmeyer-Peppas
        if len(t_data_kp) >= 3:
            try:
                popt_kp, _ = curve_fit(model_korsmeyer_peppas, t_data_kp, q_data_kp, 
                                       p0=[q_max*0.1, 0.5], maxfev=5000,
                                       bounds=([0, 0], [np.inf, 2.0]))
                r2_kp = r2_score(q_data_kp, model_korsmeyer_peppas(t_data_kp, *popt_kp))
                if r2_kp >= R2_THRESHOLD:
                    resultados_df_list.append({"Modelo": "Korsmeyer-Peppas", "R2": r2_kp, "kKP": popt_kp[0], "n": popt_kp[1]})
                else:
                    resultados_df_list.append({"Modelo": "Korsmeyer-Peppas", "R2": np.nan, "kKP": np.nan, "n": np.nan})
            except (RuntimeError, ValueError) as e:
                resultados_df_list.append({"Modelo": "Korsmeyer-Peppas", "R2": np.nan, "kKP": np.nan, "n": np.nan})
        else:
            pass # Pular silenciosamente
        
        # Modelo 1: Ordem Zero
        try:
            popt_zo, _ = curve_fit(model_zero_order, t_data, q_data, bounds=([0], [np.inf]), maxfev=10000)
            r2_zo = r2_score(q_data, model_zero_order(t_data, *popt_zo))
            if r2_zo >= R2_THRESHOLD:
                resultados_df_list.append({"Modelo": "Zero-Order", "R2": r2_zo, "k0": popt_zo[0]})
            else:
                resultados_df_list.append({"Modelo": "Zero-Order", "R2": np.nan, "k0": np.nan})
        except (RuntimeError, ValueError) as e:
            resultados_df_list.append({"Modelo": "Zero-Order", "R2": np.nan, "k0": np.nan})

        # Modelo 2: Primeira Ordem
        try:
            popt_fo, _ = curve_fit(model_first_order, t_data, q_data, 
                                   p0=[q_max, 0.1], bounds=([0, 0], [np.inf, np.inf]), maxfev=10000)
            r2_fo = r2_score(q_data, model_first_order(t_data, *popt_fo))
            if r2_fo >= R2_THRESHOLD:
                resultados_df_list.append({"Modelo": "First-Order", "R2": r2_fo, "k1": popt_fo[1]})
            else:
                resultados_df_list.append({"Modelo": "First-Order", "R2": np.nan, "k1": np.nan})
        except (RuntimeError, ValueError) as e:
            resultados_df_list.append({"Modelo": "First-Order", "R2": np.nan, "k1": np.nan})

        # Modelo 3: Higuchi
        try:
            popt_h, _ = curve_fit(model_higuchi, t_data, q_data, bounds=([0], [np.inf]), maxfev=10000)
            r2_h = r2_score(q_data, model_higuchi(t_data, *popt_h))
            if r2_h >= R2_THRESHOLD:
                resultados_df_list.append({"Modelo": "Higuchi", "R2": r2_h, "kH": popt_h[0]})
            else:
                resultados_df_list.append({"Modelo": "Higuchi", "R2": np.nan, "kH": np.nan})
        except (RuntimeError, ValueError) as e:
            resultados_df_list.append({"Modelo": "Higuchi", "R2": np.nan, "kH": np.nan})

        # Modelo 5: Hixson-Crowell
        try:
            popt_hc, _ = curve_fit(model_hixson_crowell, t_data, q_data, 
                                   p0=[q_max, 0.01], maxfev=10000,
                                   bounds=([0, 0], [np.inf, np.inf])) 
            r2_hc = r2_score(q_data, model_hixson_crowell(t_data, *popt_hc))
            if r2_hc >= R2_THRESHOLD:
                resultados_df_list.append({"Modelo": "Hixson-Crowell", "R2": r2_hc, "kHC": popt_hc[1]})
            else:
                resultados_df_list.append({"Modelo": "Hixson-Crowell", "R2": np.nan, "kHC": np.nan})
        except (RuntimeError, ValueError) as e:
            resultados_df_list.append({"Modelo": "Hixson-Crowell", "R2": np.nan, "kHC": np.nan})

        # Modelo 6: Weibull
        try:
            popt_w, _ = curve_fit(model_weibull, t_data, q_data, 
                                  p0=[q_max, 2, 1], maxfev=10000,
                                  bounds=([0, 1e-9, 1e-9], [np.inf, np.inf, np.inf])) 
            r2_w = r2_score(q_data, model_weibull(t_data, *popt_w))
            if r2_w >= R2_THRESHOLD:
                resultados_df_list.append({"Modelo": "Weibull", "R2": r2_w, "a": popt_w[1], "b": popt_w[2]})
            else:
                resultados_df_list.append({"Modelo": "Weibull", "R2": np.nan, "a": np.nan, "b": np.nan})
        except (RuntimeError, ValueError) as e:
            resultados_df_list.append({"Modelo": "Weibull", "R2": np.nan, "a": np.nan, "b": np.nan})

        # Modelo 7: Peppas-Sahlin
        try:
            popt_ps, _ = curve_fit(model_peppas_sahlin, t_data, q_data, 
                                  p0=[q_max*0.1, q_max*0.1], maxfev=10000,
                                  bounds=([0, 0], [np.inf, np.inf])) 
            r2_ps = r2_score(q_data, model_peppas_sahlin(t_data, *popt_ps))
            if r2_ps >= R2_THRESHOLD:
                resultados_df_list.append({"Modelo": "Peppas-Sahlin", "R2": r2_ps, "k_diff": popt_ps[0], "k_relax": popt_ps[1]})
            else:
                resultados_df_list.append({"Modelo": "Peppas-Sahlin", "R2": np.nan, "k_diff": np.nan, "k_relax": np.nan})
        except (RuntimeError, ValueError) as e:
            resultados_df_list.append({"Modelo": "Peppas-Sahlin", "R2": np.nan, "k_diff": np.nan, "k_relax": np.nan})


    if not resultados_df_list:
        return pd.DataFrame(), modeling_messages
        
    df_resultados = pd.DataFrame(resultados_df_list).set_index("Modelo").fillna(np.nan)
    
    return df_resultados, modeling_messages

# --- Função de Interpretação V12 ---
def interpretar_resultados_v12(df_resultados, y_label, lang_key):
    T = TEXT_DICT[lang_key] # Usa o dicionário do próprio módulo
    base_unit = "%" if "%" in y_label else y_label.split('(')[-1].replace(')', '')
    time_unit = "h"
    
    if df_resultados.empty or 'R2' not in df_resultados.columns or df_resultados['R2'].isnull().all():
        return "N/A", 0.0, np.nan, "-", np.nan, "-", np.nan, T['interp_fail'], "N/A"
    
    try:
        r2_series = df_resultados["R2"].astype(float).dropna()
        if r2_series.empty:
            return "N/A", 0.0, np.nan, "-", np.nan, "-", np.nan, T['interp_fail'], "N/A"
        
        melhor_modelo_key = r2_series.idxmax()
        melhor_modelo_str = T.get(f'model_{melhor_modelo_key.lower().replace("-","_")}', melhor_modelo_key)
        r2_melhor = df_resultados.loc[melhor_modelo_key, 'R2']
    
    except Exception as e:
        return "N/A", 0.0, np.nan, "-", np.nan, "-", np.nan, T['interp_r2_fail'], "N/A"
    
    interpretacao_mecanismo = ""
    glossario_key = "N/A" 
    k_val = np.nan
    k_unit = "-"
    k2_val = np.nan 
    k2_unit = "-" 
    n_val = np.nan
    
    try:
        if melhor_modelo_key == "Korsmeyer-Peppas":
            n_val = df_resultados.loc[melhor_modelo_key, "n"]
            k_val = df_resultados.loc[melhor_modelo_key, "kKP"]
            k_unit = f"{base_unit}/{time_unit}^n"
            if pd.notna(n_val):
                interpretacao_mecanismo = f"**{T['step4_interp_exp']}** {n_val:.3f}. "
                if n_val < 0.45: glossario_key = "fickian"
                elif 0.45 <= n_val < 0.89: glossario_key = "anomalous"
                elif n_val >= 0.89: glossario_key = "case_ii"
            interpretacao_mecanismo += f"Mecanismo: {T[f'interp_{glossario_key}']}."
        
        elif melhor_modelo_key == "Higuchi":
            k_val = df_resultados.loc[melhor_modelo_key, "kH"]
            k_unit = f"{base_unit}/{time_unit}^0.5"
            glossario_key = "fickian"
            interpretacao_mecanismo = T['interp_fickian']

        elif melhor_modelo_key == "Zero-Order":
            k_val = df_resultados.loc[melhor_modelo_key, "k0"]
            k_unit = f"{base_unit}/{time_unit}"
            glossario_key = "zero_order"
            interpretacao_mecanismo = f"{T['interp_zero_order_mech']} (k0 = {k_val:.4f} {k_unit})."

        elif melhor_modelo_key == "First-Order":
            k_val = df_resultados.loc[melhor_modelo_key, "k1"]
            k_unit = f"1/{time_unit}"
            glossario_key = "first_order"
            interpretacao_mecanismo = T['interp_first_order_mech']

        elif melhor_modelo_key == "Hixson-Crowell":
            k_val = df_resultados.loc[melhor_modelo_key, "kHC"]
            k_unit = f"1/{time_unit}"
            glossario_key = "hixson"
            interpretacao_mecanismo = T['interp_hixson_mech']

        elif melhor_modelo_key == "Weibull":
            n_val = df_resultados.loc[melhor_modelo_key, "b"]
            k_val = df_resultados.loc[melhor_modelo_key, "a"]
            k_unit = time_unit
            k2_val = n_val 
            k2_unit = "-"
            n_val = np.nan 
            if pd.notna(k2_val):
                interpretacao_mecanismo = f"Expoente de Forma (b) = {k2_val:.3f}. "
                if k2_val < 0.75: glossario_key = "fickian"
                elif 0.75 <= k2_val <= 1.0: glossario_key = "complex"
                elif k2_val > 1.0: glossario_key = "case_ii"
            interpretacao_mecanismo += f"Mecanismo: {T[f'interp_{glossario_key}']}."

        elif melhor_modelo_key == "Peppas-Sahlin":
            k_val = df_resultados.loc[melhor_modelo_key, "k_diff"] 
            k_unit = f"{base_unit}/{time_unit}^0.5"
            k2_val = df_resultados.loc[melhor_modelo_key, "k_relax"] 
            k2_unit = f"{base_unit}/{time_unit}"
            glossario_key = "peppas_sahlin"
            interpretacao_mecanismo = T['interp_peppas_sahlin_mech']
            if pd.notna(k_val) and pd.notna(k2_val):
                 if k_val > k2_val:
                     interpretacao_mecanismo += " (Domínio da Difusão: k_diff > k_relax)"
                 else:
                     interpretacao_mecanismo += " (Domínio do Relaxamento: k_relax > k_diff)"
    
    except KeyError:
        return melhor_modelo_str, r2_melhor, np.nan, "-", np.nan, "-", np.nan, interpretacao_mecanismo, glossario_key
        
    return melhor_modelo_str, r2_melhor, k_val, k_unit, k2_val, k2_unit, n_val, interpretacao_mecanismo, glossario_key

# --- Função Glossário ---
def exibir_glossario(termo_chave, lang_key):
    T = TEXT_DICT[lang_key]
    st.subheader(T['step4_glossary_header'])
    
    glossario_map = {
        "fickian": T['step4_glossary_fickian'],
        "anomalous": T['step4_glossary_anomalous'],
        "case_ii": T['step4_glossary_case_ii'],
        "zero_order": T['step4_glossary_zero_order'],
        "first_order": T['step4_glossary_first_order'],
        "hixson": T['step4_glossary_hixson'],
        "peppas_sahlin": T['step4_glossary_peppas_sahlin'],
        "complex": T['step4_glossary_complex']
    }
    
    st.info(glossario_map.get(termo_chave, T['step4_glossary_select']))

# --- Função Helper para Download ---
def get_download_button(df, T, file_name_csv, file_name_excel):
    """Gera botões de download para CSV e Excel."""
    
    # Garantir que o índice seja incluído se for nomeado (como 'Grupo')
    index_bool = df.index.name is not None
    csv_data = df.to_csv(index=index_bool).encode('utf-8') 
    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name=file_name_csv,
        mime='text/csv',
    )
    
    # Simula o motor de Excel sem importação direta do xlsxwriter
    # Requer que o Streamlit tenha o xlsxwriter instalado no ambiente de execução.
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=index_bool, sheet_name='Data')
    excel_data = output.getvalue()
    
    st.download_button(
        label=T['download_excel'],
        data=excel_data,
        file_name=file_name_excel,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# --- Função de Plotagem de Modelos Ajustados ---
def plotar_modelos_ajustados(df_model_exp, df_resultados, t_data, q_data, y_label, T):
    """Plota os dados experimentais (média) e as curvas dos modelos ajustados."""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_model_exp['Tempo'], 
        y=df_model_exp[y_label],
        mode='markers',
        name=T['step4_plot_experimental'],
        marker=dict(color='black', size=10, symbol='circle')
    ))
    
    t_fit = np.linspace(0, t_data.max(), 100)
    q_max = q_data.max()
    
    colors = px.colors.qualitative.Plotly
    
    try:
        if 'k0' in df_resultados.columns and pd.notna(df_resultados.loc['Zero-Order', 'k0']):
            k0 = df_resultados.loc['Zero-Order', 'k0']
            fig.add_trace(go.Scatter(x=t_fit, y=model_zero_order(t_fit, k0), mode='lines', name=T['model_zero_order'], line=dict(color=colors[0], dash='dash')))
            
        if 'k1' in df_resultados.columns and pd.notna(df_resultados.loc['First-Order', 'k1']):
            k1 = df_resultados.loc['First-Order', 'k1']
            fig.add_trace(go.Scatter(x=t_fit, y=model_first_order(t_fit, q_max, k1), mode='lines', name=T['model_first_order'], line=dict(color=colors[1], dash='dash')))

        if 'kH' in df_resultados.columns and pd.notna(df_resultados.loc['Higuchi', 'kH']):
            kH = df_resultados.loc['Higuchi', 'kH']
            fig.add_trace(go.Scatter(x=t_fit, y=model_higuchi(t_fit, kH), mode='lines', name=T['model_higuchi'], line=dict(color=colors[2], dash='dash')))
        
        if 'kKP' in df_resultados.columns and pd.notna(df_resultados.loc['Korsmeyer-Peppas', 'kKP']):
            kKP = df_resultados.loc['Korsmeyer-Peppas', 'kKP']
            n = df_resultados.loc['Korsmeyer-Peppas', 'n']
            t_kp = df_model_exp[df_model_exp[y_label] <= (q_max * 0.6)]["Tempo"]
            if t_kp.empty: t_kp = t_data 
            fig.add_trace(go.Scatter(x=t_kp, y=model_korsmeyer_peppas(t_kp, kKP, n), mode='lines', name=T['model_korsmeyer'], line=dict(color=colors[3], dash='dot')))

        if 'kHC' in df_resultados.columns and pd.notna(df_resultados.loc['Hixson-Crowell', 'kHC']):
            kHC = df_resultados.loc['Hixson-Crowell', 'kHC']
            fig.add_trace(go.Scatter(x=t_fit, y=model_hixson_crowell(t_fit, q_max, kHC), mode='lines', name=T['model_hixson'], line=dict(color=colors[4], dash='dash')))
        
        if 'a' in df_resultados.columns and pd.notna(df_resultados.loc['Weibull', 'a']):
            a = df_resultados.loc['Weibull', 'a']
            b = df_resultados.loc['Weibull', 'b']
            fig.add_trace(go.Scatter(x=t_fit, y=model_weibull(t_fit, q_max, a, b), mode='lines', name=T['model_weibull'], line=dict(color=colors[5], dash='dash')))

        if 'k_diff' in df_resultados.columns and pd.notna(df_resultados.loc['Peppas-Sahlin', 'k_diff']):
            k_diff = df_resultados.loc['Peppas-Sahlin', 'k_diff']
            k_relax = df_resultados.loc['Peppas-Sahlin', 'k_relax']
            fig.add_trace(go.Scatter(x=t_fit, y=model_peppas_sahlin(t_fit, k_diff, k_relax), mode='lines', name=T['model_peppas_sahlin'], line=dict(color=colors[6], dash='longdash')))
    
    except Exception as e:
        pass # Ignorar erros de plotagem silenciosamente
        
    fig.update_layout(
        title=f"{T['step4_subheader_plot']}",
        xaxis_title=T['step3_xaxis_label'], yaxis_title=y_label.split('(')[0].replace('Média_',''),
        template="plotly_white", 
        xaxis_mirror=True, yaxis_mirror=True, 
        xaxis_linewidth=1, yaxis_linewidth=1,
        xaxis_linecolor='black', yaxis_linecolor='black',
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=50, r=50, t=50, b=150) 
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Função de Cálculo f2 ---
def calcular_f2(df_agg, grupo_R, grupo_T, col_grupo, y_axis_mean):
    """Calcula o Fator de Similaridade f2 entre dois grupos."""
    
    df_R = df_agg[df_agg[col_grupo] == grupo_R][['Tempo', y_axis_mean]].rename(columns={y_axis_mean: 'R'})
    df_T = df_agg[df_agg[col_grupo] == grupo_T][['Tempo', y_axis_mean]].rename(columns={y_axis_mean: 'T'})
    
    df_merged = pd.merge(df_R, df_T, on='Tempo')
    df_merged = df_merged[df_merged['Tempo'] > 0]
    
    if df_merged.empty:
        return None
        
    n = len(df_merged)
    sum_sq_diff = np.sum((df_merged['R'] - df_merged['T'])**2)
    
    f2_termo_interno = 1 + (1 / n) * sum_sq_diff
    f2 = 50 * np.log10(100 / np.sqrt(f2_termo_interno))
    
    return f2

# --- Funções de Renderização de Página ---

def render_step1(T):
    st.header(T['step1_header'])
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(T['step1_subheader_units'])
        unidade_vol = st.selectbox(T['step1_label_vol_unit'], ["mL", "L", "µL"], 0)
        unidade_conc = st.selectbox(T['step1_label_conc_unit'], ["mg/mL", "µg/mL", "g/L", "mmol/L", "µmol/L"], 0)
        unidade_massa = unidade_conc.split('/')[0]
        st.markdown("---")
        st.subheader(T['step1_subheader_cell'])
        vol_celula = st.number_input(f"{T['step1_label_vol_receptor']} ({unidade_vol})", min_value=0.01, value=12.0, format="%.2f", step=0.1)
        vol_amostra = st.number_input(f"{T['step1_label_vol_sample']} ({unidade_vol})", min_value=0.0, value=1.0, format="%.2f", step=0.1)
    with col2:
        st.subheader(T['step1_subheader_calib'])
        st.markdown(f"`Área = a * Conc. ({unidade_conc}) + b`")
        cal_a = st.number_input(T['step1_label_calib_a'], value=10000.0, format="%.2f", step=1.0)
        cal_b = st.number_input(T['step1_label_calib_b'], value=0.0, format="%.2f", step=0.01, help=T['step1_help_calib_b'])
        st.markdown("---")
        st.subheader(T['step1_subheader_time'])
        unidade_tempo = st.selectbox(T['step1_label_time_unit'], [T['step1_time_hours'], T['step1_time_minutes']], 0)
    
    st.markdown("---")
    st.subheader(T['step1_subheader_upload'])
    with st.expander(T['step1_expander_model']):
            st.markdown("""
        | Sample_Name | Group | 0 | 0.5 | 1 | 2 |
        | :--- | :--- | :-: | :-: | :-: | :-: |
        | F1_Rep1 | F1 | 0 | 15023 | 28904 | 45002 |
        | F1_Rep2 | F1 | 0 | 14990 | 29100 | 44888 |
        | F2_Rep1 | F2 | 0 | 5000 | 9500 | 15000 |
        """)
    
    uploaded_file = st.file_uploader(T['step1_uploader_label'], type=["csv", "xlsx", "txt"])
    
    sep = ','
    decimal = '.'
    if uploaded_file and (uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt')):
        st.info(T['step1_csv_options'])
        col_parse1, col_parse2 = st.columns(2)
        with col_parse1:
            sep_label = st.selectbox(T['step1_csv_sep'], [T['step1_csv_sep_semi'], T['step1_csv_sep_comma'], T['step1_csv_sep_tab']], 0)
            sep = sep_label.split(" ")[0].replace("Tab","\t")
        with col_parse2:
            dec_label = st.selectbox(T['step1_csv_dec'], [T['step1_csv_dec_comma'], T['step1_csv_dec_point']], 1)
            decimal = dec_label.split(" ")[0]

    if uploaded_file is not None:
        if cal_a == 0:
            st.error(T['step1_error_calib_a'])
            return
        try:
            if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
                df_wide = load_data(uploaded_file, sep=sep, decimal=decimal)
            else:
                df_wide = pd.read_excel(uploaded_file)
            
            if df_wide is None: 
                return

            st.write(T['step1_upload_preview'], df_wide.head())
            
            col_amostra_nome = df_wide.columns[0]
            col_grupo = df_wide.columns[1]
            cols_tempo = df_wide.columns[2:]
            
            st.markdown("---")
            st.subheader(T['step1_subheader_dose'])
            unique_groups = df_wide[col_grupo].unique()
            doses_dict = {}
            has_any_dose = False 

            for grupo in unique_groups:
                st.markdown(f"**{T['step1_dose_group']} {grupo}**")
                c1, c2 = st.columns(2)
                conc_form = c1.number_input(f"{T['step1_dose_conc']} ({unidade_conc})", key=f"conc_{grupo}", min_value=0.0, value=10.0, format="%.2f", step=0.1)
                vol_form = c2.number_input(f"{T['step1_dose_vol']} ({unidade_vol})", key=f"vol_{grupo}", min_value=0.0, value=1.0, format="%.2f", step=0.1)
                dose_total_grupo = conc_form * vol_form
                doses_dict[grupo] = {'dose_total': dose_total_grupo}
                if dose_total_grupo > 0: has_any_dose = True

            st.markdown("---")
            if st.button(T['step1_button_process'], type="primary"):
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
                        'unidade_massa': unidade_massa, 'has_dose_info': has_any_dose,
                        'col_q_acumulada': col_q_acumulada_nome, 'col_percent': col_percent_nome,
                        'col_conc': col_conc_nome, 'col_grupo': col_grupo,
                        'col_amostra_nome': col_amostra_nome,
                        'vol_celula': vol_celula,
                        'vol_amostra': vol_amostra,
                        'unidade_vol': unidade_vol,
                        'unidade_conc': unidade_conc,
                        'doses_dict': doses_dict, 
                    }
                    
                    if has_any_dose:
                        config_dict['y_label'] = T['step1_y_label_pct']
                        config_dict['y_axis_mean'] = 'Média_Percent'
                        config_dict['y_axis_sd'] = 'SD_Percent'
                        config_dict['y_axis_col'] = col_percent_nome
                    else:
                        config_dict['y_label'] = f"{T['step1_y_label_q']} ({unidade_massa})"
                        config_dict['y_axis_mean'] = 'Média_Q_Acumulada'
                        config_dict['y_axis_sd'] = 'SD_Q_Acumulada'
                        config_dict['y_axis_col'] = col_q_acumulada_nome
                    
                    st.session_state.config = config_dict
                    st.success(T['step1_success_process'])
        except Exception as e:
            st.error(f"{T['step1_error_process']} {e}")
            
def render_step2(T):
    st.header(T['step2_header'])
    if st.session_state.df_long_processado is None:
        st.warning(T['step2_warning_process'])
        return
    st.info(T['step2_info'])
    
    st.subheader(T['step2_subheader_raw'])
    st.dataframe(st.session_state.df_long_processado, use_container_width=True) 
    get_download_button(st.session_state.df_long_processado, T, "dados_processados_replicas.csv", "dados_processados_replicas.xlsx")

    st.subheader(T['step2_subheader_agg'])
    st.dataframe(st.session_state.df_agregado, use_container_width=True) 
    get_download_button(st.session_state.df_agregado, T, "dados_agregados_media_sd.csv", "dados_agregados_media_sd.xlsx")

def render_step3(T):
    st.header(T['step3_header'])
    
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

    st.info(T['step3_info_export'])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(T['step3_subheader_individual'])
        grupo_selecionado = st.selectbox(T['step3_selectbox_group'], grupos_disponiveis)
        
        if grupo_selecionado:
            df_grupo_agg = df_agg[df_agg[col_grupo] == grupo_selecionado].copy()
            fig_individual = go.Figure()
            
            fig_individual.add_trace(go.Scatter(
                x=df_grupo_agg['Tempo'], y=df_grupo_agg[y_axis_mean],
                mode='lines+markers', name=T['step3_legend_individual'],
                line=dict(color='blue', width=2), marker=dict(size=8),
                error_y=dict(
                    type='data', array=df_grupo_agg[y_axis_sd],
                    visible=True, thickness=1.5, width=3
                )
            ))
            
            fig_individual.update_layout(
                title=f"{T['step3_title_individual']} {grupo_selecionado}",
                xaxis_title=T['step3_xaxis_label'], yaxis_title=y_label, 
                template="plotly_white", 
                height=500, 
                xaxis_mirror=True, yaxis_mirror=True, 
                xaxis_linewidth=1, yaxis_linewidth=1,
                xaxis_linecolor='black', yaxis_linecolor='black',
                legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
                margin=dict(l=50, r=50, t=50, b=150) 
            )
            st.plotly_chart(fig_individual, use_container_width=True)

    with col2:
        st.subheader(T['step3_subheader_compare'])
        
        color_map = {}
        default_colors = px.colors.qualitative.Plotly
        with st.expander(T['step3_color_picker_label']):
            for i, grupo in enumerate(grupos_disponiveis):
                default_color = default_colors[i % len(default_colors)]
                color_map[grupo] = st.color_picker(f"{T['step3_color_picker_group']} {grupo}", value=default_color, key=f"color_{grupo}")
        
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
                    type='data', array=df_grupo[y_axis_sd],
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
        st.plotly_chart(fig_comparativo, use_container_width=True)

def render_step4(T):
    st.header(T['step4_header'])
    
    # 1. Pré-requisito: Verifica se os dados foram processados
    if st.session_state.df_agregado is None:
        st.warning(T['step2_warning_process'])
        return

    df_agg = st.session_state.df_agregado
    config = st.session_state.config
    col_grupo = config['col_grupo']
    grupos_disponiveis = df_agg[col_grupo].unique()
    
    st.info(T['step4_info_model'])
    
    # 2. Seleção de Grupo
    grupo_selecionado_modelagem = st.selectbox(T['step4_selectbox_group'], grupos_disponiveis, key="model_select")
    
    st.markdown("---")
    
    # 3. Checkbox de Exclusão (V52: Padrão True)
    st.checkbox(
        label=T['step4_checkbox_label_t0'], 
        key='excluir_t_zero', # Salva a mudança no estado de sessão
        value=st.session_state.excluir_t_zero, # Garante que comece como True
        help=T['step4_checkbox_help_t0']
    )
    
    st.markdown("---")
    
    # 4. Início da Análise (Acontece SOMENTE se um grupo for selecionado)
    if grupo_selecionado_modelagem:
        df_grupo_agg = df_agg[df_agg[col_grupo] == grupo_selecionado_modelagem].copy()
        y_axis_mean = config['y_axis_mean']
        
        # Lógica do filtro lendo o estado do checkbox
        if st.session_state.excluir_t_zero:
            df_model = df_grupo_agg[df_grupo_agg["Tempo"] > 0].copy()
        else:
            df_model = df_grupo_agg.copy()
            
        t_data = df_model["Tempo"]
        q_data = df_model[y_axis_mean] 
        
        df_plot = df_grupo_agg.copy() 

        # 5. Validação de pontos (Se falhar, retorna um erro, não fica vazio)
        if len(q_data) < 3:
            st.error(T['step4_error_points'])
            return

        # 6. Modelagem
        df_resultados, mensagens_modelagem = rodar_modelagem_v12(t_data, q_data, df_model, y_axis_mean, config.get('has_dose_info', False))

        for msg in mensagens_modelagem:
            st.warning(msg) 

        if df_resultados.empty:
            st.error(T['step4_error_fit'])
            return
        
        # 7. Exibição dos Resultados
        df_resultados_display = df_resultados.copy()
        df_resultados_display.index = [T.get(f'model_{idx.lower().replace("-","_")}', idx) for idx in df_resultados_display.index]

        st.subheader(f"{T['step4_subheader_results']} {grupo_selecionado_modelagem}")
        
        cols_to_format = ['R2', 'kKP', 'n', 'k0', 'k1', 'kH', 'kHC', 'a', 'b', 'k_diff', 'k_relax']
        cols_exist = [col for col in cols_to_format if col in df_resultados_display.columns]
        
        st.dataframe(
            df_resultados_display.style
            .highlight_max(subset=["R2"], color="lightgreen", axis=0)
            .format("{:.4f}", na_rep="-", subset=pd.IndexSlice[:, cols_exist]),
            use_container_width=True
        )
        get_download_button(df_resultados_display, T, f"modelos_{grupo_selecionado_modelagem}.csv", f"modelos_{grupo_selecionado_modelagem}.xlsx")
        
        st.markdown("---")
        
        plotar_modelos_ajustados(df_plot, df_resultados, t_data, q_data, y_axis_mean, T)

        st.markdown("---")
        st.subheader(T['step4_subheader_interp'])
        
        (melhor_modelo, r2_melhor, 
        k_val, k_unit, k2_val, k2_unit, n_val, 
        interpretacao, glossario_key) = interpretar_resultados_v12(df_resultados, config['y_label'], st.session_state.lang)
        
        if r2_melhor >= 0.05:
            st.success(f"O modelo com melhor ajuste (maior R²) é: **{melhor_modelo}** (R² = {r2_melhor:.4f})")
            
            param_str_list = []
            if pd.notna(k_val):
                param_str_list.append(f"**Constante 1:** {k_val:.4f} ({k_unit})")
            if pd.notna(k2_val):
                 param_str_list.append(f"**Constante 2:** {k2_val:.4f} ({k2_unit})")
            if pd.notna(n_val):
                param_str_list.append(f"**Expoente (n):** {n_val:.3f}")
            
            st.markdown(" | ".join(param_str_list))
            
            st.info(f"**Interpretação:** {interpretacao}")
            
            exibir_glossario(glossario_key, st.session_state.lang)
        else:
            st.error(T['interp_fail'])

def render_step5(T):
    st.header(T['step5_header'])
    
    if st.session_state.df_agregado is None:
        st.warning(T['step2_warning_process'])
        return
        
    st.info(T['step5_info'])

    df_agg = st.session_state.df_agregado
    df_long = st.session_state.df_long_processado
    config = st.session_state.config
    col_grupo = config['col_grupo']
    grupos_disponiveis = df_agg[col_grupo].unique()
    y_axis_col = config['y_axis_col'] 
    y_axis_mean = config['y_axis_mean']
    col_amostra = config['col_amostra_nome'] # <-- Nome dinâmico da coluna de réplica/amostra
    
    tab_summary, tab_stats, tab_f2 = st.tabs([
        T['step5_tab_summary'], 
        T['step5_tab_stats'], 
        T['step5_tab_f2']
    ])
    
    with tab_summary:
        st.info(T['step5_summary_info'])
        resumo_list = []

        with st.spinner(T['step5_spinner']):
            y_unit_base = config['y_label'].split('(')[-1].replace(')', '')
            
            for grupo in grupos_disponiveis:
                df_grupo_agg = df_agg[df_agg[col_grupo] == grupo].copy()
                
                df_grupo_agg = df_grupo_agg.sort_values(by='Tempo')
                tempos = df_grupo_agg['Tempo']
                valores_medios = df_grupo_agg[y_axis_mean]
                
                auc_val = np.trapezoid(valores_medios, x=tempos)
                release_final = valores_medios.iloc[-1]
                
                resumo_dict = {
                    T['step5_col_group']: grupo,
                    f"{T['step5_col_auc']} ({y_unit_base}⋅h)": auc_val,
                    f"{T['step5_col_release_final']} ({y_unit_base})": release_final,
                    T['step5_col_model']: "N/A",
                    T['step5_col_r2']: 0.0,
                    T['step5_col_k']: np.nan, T['step5_col_k_unit']: "-",
                    T['step5_col_k2']: np.nan, T['step5_col_k2_unit']: "-",
                    T['step5_col_n']: np.nan,
                    T['step5_col_interp']: T['step5_error_data']
                }
                
                # --- V51: Lógica do filtro lendo o state para modelagem (Bug 1 Fix) ---
                if st.session_state.excluir_t_zero:
                    df_model = df_grupo_agg[df_grupo_agg["Tempo"] > 0].copy()
                else:
                    df_model = df_grupo_agg.copy()
                
                t_data = df_model["Tempo"]
                q_data = df_model[y_axis_mean] 

                if len(q_data) < 3:
                    resumo_list.append(resumo_dict) 
                    continue
                
                df_resultados_grupo, _ = rodar_modelagem_v12(t_data, q_data, df_model, y_axis_mean, config.get('has_dose_info', False))
                
                (melhor_modelo, r2_melhor, 
                 k_val, k_unit, k2_val, k2_unit, n_val, 
                 interpretacao, _) = interpretar_resultados_v12(df_resultados_grupo, config['y_label'], st.session_state.lang)
                
                resumo_dict.update({
                    T['step5_col_model']: melhor_modelo,
                    T['step5_col_r2']: r2_melhor, 
                    T['step5_col_k']: k_val,
                    T['step5_col_k_unit']: k_unit,
                    T['step5_col_k2']: k2_val,
                    T['step5_col_k2_unit']: k2_unit,
                    T['step5_col_n']: n_val,
                    T['step5_col_interp']: interpretacao
                })
                
                resumo_list.append(resumo_dict)
        
        df_resumo = pd.DataFrame(resumo_list).set_index(T['step5_col_group'])
        
        df_resumo_display = df_resumo.copy()
        df_resumo_display[T['step5_col_r2']] = df_resumo_display[T['step5_col_r2']].apply(lambda x: np.nan if x is not None and x < 0.05 else x)
        
        format_dict = {
            T['step5_col_r2']: "{:.4f}",
            T['step5_col_k']: "{:.4f}",
            T['step5_col_k2']: "{:.4f}",
            T['step5_col_n']: "{:.3f}",
            f"{T['step5_col_auc']} ({y_unit_base}⋅h)": "{:.2f}",
            f"{T['step5_col_release_final']} ({y_unit_base})": "{:.2f}"
        }
        
        st.dataframe(
            df_resumo_display.style.format(format_dict, na_rep="-"),
            use_container_width=True
        )
        get_download_button(df_resumo_display, T, "resumo_cinetico_completo.csv", "resumo_cinetico_completo.xlsx")
    
    with tab_stats:
        st.subheader(T['step5_stats_header'])
        st.info(T['step5_stats_info'])
        
        col_stats1, col_stats2 = st.columns(2)
        with col_stats1:
            grupos_selecionados_stats = st.multiselect(T['step5_stats_select_groups'], grupos_disponiveis)
        
        with col_stats2:
            tempos_disponiveis = df_long['Tempo'].unique()
            tempos_disponiveis.sort()
            opcoes_tempo = [T['step5_stats_auc'], T['step5_stats_time_final']] + [f"{t} h" for t in tempos_disponiveis if t > 0]
            tempo_selecionado_str = st.selectbox(T['step5_stats_select_time'], options=opcoes_tempo)
        
        if st.button(T['step5_stats_button'], type="primary"):
            if len(grupos_selecionados_stats) < 2:
                st.error("Please select at least 2 groups to compare.")
            else:
                dados_para_teste = []
                grupos_validos = True
                
                if tempo_selecionado_str == T['step5_stats_auc']:
                    st.markdown(f"**Comparing Groups:** `{', '.join(grupos_selecionados_stats)}` by **{T['step5_stats_auc']}**")

                    for grupo in grupos_selecionados_stats:
                        
                        # --- V51: CORREÇÃO do KeyError ('Sample_Name') ---
                        replicas_do_grupo = df_long[df_long[col_grupo] == grupo][col_amostra].unique()
                        
                        if len(replicas_do_grupo) < 2:
                            grupos_validos = False
                            st.error(f"Group '{grupo}' has less than 2 replicates for AUC statistical calculation.")
                            break
                        
                        aucs_grupo = []
                        for replica_id in replicas_do_grupo:
                            df_replica = df_long[df_long[col_amostra] == replica_id].sort_values(by='Tempo')
                            tempos_replica = df_replica['Tempo']
                            valores_replica = df_replica[y_axis_col]
                            
                            if len(tempos_replica) > 1:
                                auc_replica = np.trapezoid(valores_replica, x=tempos_replica)
                                aucs_grupo.append(auc_replica)
                        
                        if len(aucs_grupo) < 2: 
                            grupos_validos = False
                            st.error(f"Could not calculate AUC for sufficient replicates in group '{grupo}'. (N={len(aucs_grupo)})")
                            break
                            
                        dados_para_teste.append(pd.Series(aucs_grupo))
                
                else: 
                    if tempo_selecionado_str == T['step5_stats_time_final']:
                        tempo_selecionado_val = df_long['Tempo'].max()
                    else:
                        tempo_selecionado_val = float(tempo_selecionado_str.split(" ")[0])
                    
                    st.markdown(f"**Comparing Groups:** `{', '.join(grupos_selecionados_stats)}` at **Time:** `{tempo_selecionado_val} h`")
                    
                    for grupo in grupos_selecionados_stats:
                        replicas = df_long[
                            (df_long[col_grupo] == grupo) & 
                            (df_long['Tempo'] == tempo_selecionado_val)
                        ][y_axis_col].dropna()
                        
                        if len(replicas) < 2:
                            grupos_validos = False
                            st.error(f"Group '{grupo}' has less than 2 replicates at time {tempo_selecionado_val}h. Cannot run test.")
                            break
                        
                        dados_para_teste.append(replicas)
                
                if grupos_validos and len(dados_para_teste) >= 2:
                    st.subheader(T['step5_stats_results'])
                    
                    variancias_zero = [np.var(dados) == 0 for dados in dados_para_teste]
                    
                    if all(variancias_zero) and len(dados_para_teste[0]) > 0 and dados_para_teste[0].iloc[0] == 0:
                        st.info("All groups have zero variance (e.g., all replicates are identical, likely 0). No statistical test can be applied.")
                    else:
                        if len(dados_para_teste) == 2:
                            stat, p_value = stats.ttest_ind(dados_para_teste[0], dados_para_teste[1], equal_var=False) # Welch's T-test
                            label_teste = f"{T['step5_stats_ttest']} (p-value)"
                        else:
                            stat, p_value = stats.f_oneway(*dados_para_teste)
                            label_teste = f"{T['step5_stats_anova']} (p-value)"
                        
                        # --- V51: Lógica de formatação do p-valor (Já corrigida na última interação) ---
                        if p_value < 0.0001:
                            p_valor_formatado_str = "< 0.0001"
                            p_valor_formatado_desc = "(p < 0.0001)"
                        else:
                            p_valor_formatado_str = f"{p_value:.5f}" 
                            p_valor_formatado_desc = f"(p = {p_value:.5f})" 
                        
                        st.metric(label=label_teste, value=p_valor_formatado_str)
                        
                        if p_value < 0.05:
                            st.success(f"**{T['step5_stats_conclusion_sig']}** {p_valor_formatado_desc}")
                        else:
                            st.info(f"**{T['step5_stats_conclusion_nonsig']}** {p_valor_formatado_desc}")

    with tab_f2:
        st.subheader(T['step5_f2_header'])
        st.info(T['step5_f2_info'])
        st.warning(T['step5_f2_warning_rules'])
        
        col_f2_1, col_f2_2 = st.columns(2)
        with col_f2_1:
            grupo_R = st.selectbox(T['step5_f2_ref'], grupos_disponiveis, key="f2_R")
        with col_f2_2:
            grupo_T = st.selectbox(T['step5_f2_test'], grupos_disponiveis, key="f2_T", index=min(1, len(grupos_disponiveis)-1))
            
        if st.button(T['step5_f2_button'], type="primary"):
            if grupo_R == grupo_T:
                st.error(T['step5_f2_error'])
            else:
                f2_valor = calcular_f2(df_agg, grupo_R, grupo_T, col_grupo, y_axis_mean)
                if f2_valor is None:
                    st.error(T['step5_f2_error_points'])
                else:
                    if f2_valor >= 50:
                        st.success(T['step5_f2_result_sim'].format(f2_valor))
                    else:
                        st.error(T['step5_f2_result_nonsim'].format(f2_valor))
        
def render_step6(T):
    st.header(T['step6_header'])
    
    if st.session_state.df_agregado is None or st.session_state.config == {}:
        st.warning(T['step2_warning_process'])
        return
        
    st.info(T['step6_info'])
    
    st.subheader(T['step6_subheader_context'])
    
    col1, col2 = st.columns(2)
    with col1:
        drug_name = st.text_input(T['step6_label_drug'], "Ex: Curcumin")
        release_medium = st.text_input(T['step6_label_medium'], "Ex: Phosphate buffer (pH 7.4) + 0.5% Tween 80")
    with col2:
        system_name = st.text_input(T['step6_label_system'], "Ex: PLGA nanoparticles")
        membrane_type = st.text_input(T['step6_label_membrane'], "Ex: Cellulose acetate (0.45 µm)")
    
    objective = st.text_input(T['step6_label_objective'], "Ex: Compare release of free curcumin vs. nanoencapsulated")
    
    if st.button(T['step6_button_generate'], type="primary"):
        with st.spinner("Analisando e gerando Prompt..."):
            df_agg = st.session_state.df_agregado
            config = st.session_state.config
            col_grupo = config['col_grupo']
            grupos_disponiveis = df_agg[col_grupo].unique()
            y_axis_mean = config['y_axis_mean']
            resumo_list = []
            
            for grupo in grupos_disponiveis:
                df_grupo_agg = df_agg[df_agg[col_grupo] == grupo].copy()
                
                # --- V51: Lógica do filtro lendo o state para modelagem (Bug 1 Fix) ---
                if st.session_state.excluir_t_zero:
                    df_model = df_grupo_agg[df_grupo_agg["Tempo"] > 0].copy()
                else:
                    df_model = df_grupo_agg.copy()
                
                t_data = df_model["Tempo"]
                q_data = df_model[y_axis_mean]
                if len(q_data) < 3: continue
                
                df_resultados_grupo, _ = rodar_modelagem_v12(t_data, q_data, df_model, y_axis_mean, config.get('has_dose_info', False))
                
                (melhor_modelo, r2_melhor, 
                 k_val, k_unit, k2_val, k2_unit, n_val, 
                 interpretacao, _) = interpretar_resultados_v12(df_resultados_grupo, config['y_label'], st.session_state.lang)
                
                resumo_list.append({
                    T['step5_col_group']: grupo,
                    T['step5_col_model']: melhor_modelo,
                    T['step5_col_r2']: r2_melhor,
                    T['step5_col_k']: k_val,
                    T['step5_col_k_unit']: k_unit,
                    T['step5_col_k2']: k2_val,
                    T['step5_col_n']: n_val,
                })
            
            df_resumo = pd.DataFrame(resumo_list).set_index(T['step5_col_group'])
            df_resumo[T['step5_col_r2']] = df_resumo[T['step5_col_r2']].apply(lambda x: np.nan if x is not None and x < 0.05 else x)
            
            y_axis_label = config['y_axis_mean']
            y_unit = "(%)" if '%' in y_axis_label else f"({config.get('unidade_massa', 'unit')})"
            max_time = df_agg['Tempo'].max()
            
            final_results_str = f"| {T['step5_col_group']} | Final Time (h) | Mean Release {y_unit} |\n"
            final_results_str += f"| :--- | :--- | :--- |\n"
            for grupo in grupos_disponiveis:
                val = df_agg.loc[(df_agg[col_grupo] == grupo) & (df_agg['Tempo'] == max_time), y_axis_label].values
                if len(val) > 0:
                    final_results_str += f"| {grupo} | {max_time} | {val[0]:.2f} |\n"
            
            prompt = f"{T['prompt_title']}\n\n"
            prompt += f"{T['prompt_context_header']}\n"
            prompt += f"* **{T['prompt_context_drug']}:** {drug_name}\n"
            prompt += f"* **{T['prompt_context_system']}:** {system_name}\n"
            prompt += f"* **{T['prompt_context_objective']}:** {objective}\n\n"
            
            prompt += f"{T['prompt_methods_header']}\n"
            prompt += f"* **{T['prompt_methods_vol_receptor']}:** {config.get('vol_celula', 'N/A')} {config.get('unidade_vol', '')}\n"
            prompt += f"* **{T['prompt_methods_vol_sample']}:** {config.get('vol_amostra', 'N/A')} {config.get('unidade_vol', '')}\n"
            prompt += f"* **{T['prompt_methods_medium']}:** {release_medium}\n" 
            prompt += f"* **{T['prompt_methods_membrane']}:** {membrane_type}\n" 
            prompt += "\n"
            
            prompt += f"{T['prompt_results_header']}\n"
            prompt += final_results_str
            prompt += "\n"
            
            prompt += f"{T['prompt_kinetics_header']}\n"
            prompt += df_resumo.to_markdown(float_format="%.4f", na_rep='-') 
            prompt += "\n\n"
            
            prompt += f"{T['prompt_tasks_header']}\n"
            prompt += f"{T['prompt_task_1']}\n"
            prompt += f"{T['prompt_task_2']}\n"
            prompt += f"{T['prompt_task_3']}\n"
            
            st.text_area(T['step6_prompt_header'], value=prompt, height=400)
            st.success(T['step6_copy_success'])

# --- MÓDULO DE LIBERAÇÃO - App Principal ---
def render_release_app():
    T = TEXT_DICT[st.session_state.lang]
    st.sidebar.info(T['release_sidebar_info']) # USA A INFORMAÇÃO SIMPLIFICADA
    pagina_opcoes = [
        T['nav_step1'], T['nav_step2'], T['nav_step3'],
        T['nav_step4'], T['nav_step5'], T['nav_step6']
    ]
    pagina = st.sidebar.radio("Navegação", pagina_opcoes, key="release_nav") # Rótulo fixo "Navegação"
    
    # --- MUDANÇA: Botão de Retorno Movido para Cima e Corrigido para i18n ---
    if st.sidebar.button(T['home_footer']): 
        st.session_state.app_mode = 'home'
        st.rerun()

    st.sidebar.markdown("---") # Linha divisória após o botão de retorno
    
    if pagina == T['nav_step1']:
        render_step1(T)
    elif pagina == T['nav_step2']:
        render_step2(T)
    elif pagina == T['nav_step3']:
        render_step3(T)
    elif pagina == T['nav_step4']:
        render_step4(T)
    elif pagina == T['nav_step5']:
        render_step5(T)
    elif pagina == T['nav_step6']:
        render_step6(T)