import streamlit as st
import pandas as pd
import sys # Importar sys para manipular o caminho de busca (sys.path)
import os  # Importar os para obter caminhos de arquivo
import warnings

# --- Versão e Informações Globais ---
APP_VERSION = "V1.0.0" 

# --- CORREÇÃO ROBUSTA DE CAMINHO ---
# Isso garante que a pasta raiz do repositório seja procurada primeiro, 
# contornando problemas de importação no Streamlit Cloud.
try:
    path_root = os.path.dirname(os.path.abspath(__file__))
    if path_root not in sys.path:
        sys.path.insert(0, path_root)
except Exception:
    pass 
# ---------------------------------------------


# --- Importa os módulos (Tratamento de Erro de Inicialização) ---
try:
    from m_release import render_release_app 
    from m_permeation import render_permeation_app 
    MODULES_LOADED = True
except ImportError:
    # Se a importação falhar, defina funções dummy e exiba um erro crítico
    st.error("ERRO CRÍTICO: Não foi possível carregar 'm_release.py' ou 'm_permeation.py'. Verifique se todos os arquivos estão na raiz do repositório.")
    def render_release_app(): pass
    def render_permeation_app(): pass
    MODULES_LOADED = False


# --- Dicionário de Tradução (i18n) - Apenas HOME/GLOBAL ---
TEXT_DICT = {
    'pt': {
        # Título da aba do navegador
        'app_title': "FluxIQ: Franz Cell Release & Permeation Analyzer",
        'sidebar_nav': "Navegação",
        
        # --- Home Texts ---
        # Título principal na página
        'home_title': "FluxIQ: Franz Cell Release & Permeation Analyzer",
        'home_description_main': "Plataforma analítica inteligente para modelagem, cálculo e visualização da cinética de liberação e permeação de fármacos usando células de difusão de Franz.",
        'home_text_features': "Recursos Principais:",
        
        # Item 1 removido conforme solicitado anteriormente
        'home_feature_2': "Modelagem Cinética: Ajuste dos 7 modelos clássicos (Zero-Order, First-Order, Higuchi, Korsmeyer-Peppas, etc.).",
        'home_feature_3': "Análise de Permeação: Cálculo de $J_{ss}$, $T_{lag}$, $K_p$ e $D$ com seleção interativa de Steady-State.",
        'home_feature_4': "Análise Estatística: Testes t/ANOVA e Fator $f_2$ (FDA/EMA) para comparação de perfis.",
        'home_feature_5': "Prompt para IA: Geração de prompt estruturado com resultados para análise complementar.",

        'home_release_button': "Análise de Liberação",
        'home_release_desc': "Calcular a % de liberação, ajustar modelos cinéticos (Higuchi, Peppas, etc.) e analisar o mecanismo de liberação.",
        'home_permeation_button': "Análise de Permeação",
        'home_permeation_desc': "Calcular parâmetros de permeação (Fluxo $J_{ss}$, $K_p$, $T_{lag}$) a partir de um perfil de permeação cutânea ou membrana sintética.", 
        'home_footer_nav': "Retornar à Seleção de Módulo",
        
        # --- Footer/Nota de Citação ---
        'app_footer': f"""
        ---
        **FluxIQ** | Versão {APP_VERSION} | Desenvolvido por [IMeT Group].
        Este software é gratuito para fins acadêmicos e de pesquisa.
        **Citação:** Caso utilize este software em pesquisa publicada, cite-o como:
        * [Carvalho, F. V. & Rodrigues da Silva, G. H.]. **FluxIQ: Franz Cell Analyzer** (Versão {APP_VERSION}). [2025]. Disponível em [https://fluxiq.streamlit.app/].
        """,
        
    },
    'en': {
        # Browser tab title
        'app_title': "FluxIQ: Franz Cell Release & Permeation Analyzer",
        'sidebar_nav': "Navigation",

        # --- Home Texts ---
        # Main page title
        'home_title': "FluxIQ: Franz Cell Release & Permeation Analyzer",
        'home_description_main': "Intelligent analytical platform for modeling, calculating, and visualizing drug release and permeation kinetics using Franz diffusion cells.",
        'home_text_features': "Key Features:",
        
        # Item 1 removed as requested previously
        'home_feature_2': "Kinetic Modeling: Fitting of 7 classic models (Zero-Order, First-Order, Higuchi, Korsmeyer-Peppas, etc.).",
        'home_feature_3': "Permeation Analysis: Calculation of $J_{ss}$, $T_{lag}$, $K_p$, and $D$ with interactive Steady-State selection.",
        'home_feature_4': "Statistical Analysis: t-tests/ANOVA and $f_2$ factor (FDA/EMA) for profile comparison.",
        'home_feature_5': "AI Prompt: Structured prompt generation with results for complementary analysis.",

        'home_release_button': "Drug Release Analysis",
        'home_release_desc': "Calculate % release, fit kinetic models (Higuchi, Peppas, etc.), and analyze the release mechanism.",
        'home_permeation_button': "Permeation Analysis",
        'home_permeation_desc': "Calculate permeation parameters (Flux $J_{ss}$, $K_p$, $T_{lag}$) from a synthetic membrane or skin permeation profile.",
        'home_footer_nav': "Return to Module Selection",
        
        # --- Footer/Citation Note ---
        'app_footer': f"""
        ---
        **FluxIQ** | Version {APP_VERSION} | Developed by [IMeT Group].
        This software is free for academic and research purposes.
        **Citation:** If you use this software in a published research, cite it as:
        * [Carvalho, F. V. & Rodrigues da Silva, G. H.]. **FluxIQ: Franz Cell Analyzer** (Version {APP_VERSION}). [2025]. Available at [https://fluxiq.streamlit.app/].
        """,
    }
}

# --- Página Inicial (Home) --- 
def render_home(T):
    st.title(T['home_title'])
    st.markdown(f"### {T['home_description_main']}")
    
    # Lista de Recursos
    st.markdown(f"**{T['home_text_features']}**")
    st.markdown(f"""
    - {T['home_feature_2']}
    - {T['home_feature_3']}
    - {T['home_feature_4']}
    - {T['home_feature_5']}
    """)
    
    st.markdown("---")
    
    # Layout com Cores e Emojis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"💊 {T['home_release_button']}")
        st.markdown(T['home_release_desc'])
        if st.button(T['home_release_button'], type="primary"):
            st.session_state.app_mode = 'release'
            st.rerun()
            
    with col2:
        st.subheader(f"🧪 {T['home_permeation_button']}")
        st.markdown(T['home_permeation_desc'])
        if st.button(T['home_permeation_button'], type="primary"):
            st.session_state.app_mode = 'permeation'
            st.rerun()
            
    # --- Exibição da Nota de Rodapé/Citação ---
    st.markdown(T['app_footer'])
    st.markdown(f"")


# --- Função Principal do App (Roteador) --- 
def main():
    
    # Se os módulos não carregaram, pare aqui e exiba a mensagem
    if not MODULES_LOADED:
        return

    # Inicializar estado da sessão (Deve ser o primeiro comando)
    if 'lang' not in st.session_state:
        st.session_state.lang = 'en'
    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = 'home'
    
    # Estados de dados e configuração
    if 'df_long_processado' not in st.session_state:
        st.session_state.df_long_processado = None
    if 'df_agregado' not in st.session_state:
        st.session_state.df_agregado = None
    if 'config' not in st.session_state:
        st.session_state.config = {}
    if 'fit_results' not in st.session_state:
        st.session_state.fit_results = None
    if 'perm_results' not in st.session_state:
        st.session_state.perm_results = {}
    
    # V52: Garante que o estado seja True por padrão (Exclude t=0)
    if 'excluir_t_zero' not in st.session_state:
        st.session_state.excluir_t_zero = True 

    # Seletor de Idioma 
    # Use o estado 'lang' para definir o index inicial
    initial_index = 0 if st.session_state.lang == 'pt' else 1
    lang_choice = st.sidebar.selectbox("Language / Idioma", ["Português", "English"], index=initial_index)
    st.session_state.lang = 'pt' if lang_choice == "Português" else 'en'
    T = TEXT_DICT[st.session_state.lang]

    # Configuração da Página (Primeiro comando Streamlit no fluxo de execução)
    st.set_page_config(layout="wide", page_title=T['app_title'])
    
    # A navegação principal está na sidebar
    st.sidebar.title(T['sidebar_nav'])
    
    # Exibição da versão na Sidebar
    st.sidebar.markdown(f"**Versão:** {APP_VERSION}") 
    st.sidebar.markdown("---")
    
    if st.session_state.app_mode == 'home':
        render_home(T)
    elif st.session_state.app_mode == 'release':
        st.title(f"FluxIQ - {T['home_release_button']}")
        render_release_app() 
    elif st.session_state.app_mode == 'permeation':
        st.title(f"FluxIQ - {T['home_permeation_button']}")
        render_permeation_app()

if __name__ == "__main__":
    main()