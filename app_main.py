import streamlit as st
import pandas as pd
import sys # Importar sys para manipular o caminho de busca (sys.path)
import os  # Importar os para obter caminhos de arquivo
import warnings

# --- Versão e Informações Globais (NOVO) ---
APP_VERSION = "V64.0"

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


# --- Importa os módulos (Tratamento de Erro de Inicialização V53) ---
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
        'app_title': "FluxIQ: Analisador de Liberação e Permeação (Célula de Franz)",
        'app_description': "Plataforma analítica inteligente para modelagem, cálculo e visualização da cinética de liberação e permeação de fármacos usando células de difusão de Franz.",
        'sidebar_nav': "Navegação",
        
        # --- Home ---
        'home_header': "Selecione o Módulo de Análise",
        'home_subheader': "Escolha o tipo de experimento que você deseja analisar.",
        'home_release_button': "Análise de Liberação",
        'home_release_desc': "Calcular a % de liberação, ajustar modelos cinéticos (Higuchi, Peppas, etc.) e analisar o mecanismo de liberação.",
        'home_permeation_button': "Análise de Permeação",
        'home_permeation_desc': "Calcular parâmetros de permeação (Fluxo $J_{ss}$, $K_p$, $T_{lag}$) a partir de um perfil de permeação cutânea ou de membrana **sintética ou tecido *ex vivo* **.", 
        'home_footer': "Retornar à Seleção de Módulo",
        
        # --- Footer/Nota de Citação ---
        'app_footer': f"""
        ---
        **FluxIQ** | Versão {APP_VERSION} | Desenvolvido por [Nome do Desenvolvedor/Grupo].
        Este software é gratuito para fins acadêmicos e de pesquisa.
        **Citação Obrigatória:** Caso utilize este software em pesquisa publicada, cite-o como:
        * [Nome do Desenvolvedor/Grupo]. **FluxIQ: Franz Cell Analyzer** (Versão {APP_VERSION}). [Ano de Uso]. Disponível em https://aws.amazon.com/pt/what-is/repo/.
        """,
        
    },
    'en': {
        'app_title': "FluxIQ: Franz Cell Release & Permeation Analyzer",
        'app_description': "Intelligent analytical platform for modeling, calculating, and visualizing drug release and permeation kinetics using Franz diffusion cells.",
        'sidebar_nav': "Navigation",

        # --- Home ---
        'home_header': "Select Analysis Module",
        'home_subheader': "Choose the type of experiment you want to analyze.",
        'home_release_button': "Drug Release Analysis",
        'home_release_desc': "Calculate % release, fit kinetic models (Higuchi, Peppas, etc.), and analyze the release mechanism.",
        'home_permeation_button': "Permeation Analysis",
        'home_permeation_desc': "Calculate permeation parameters (Flux $J_{ss}$, $K_p$, $T_{lag}$) from a synthetic membrane or *ex vivo* tissue permeation profile.",
        'home_footer': "Return to Module Selection",
        
        # --- Footer/Nota de Citação ---
        'app_footer': f"""
        ---
        **FluxIQ** | Version {APP_VERSION} | Developed by [Developer Name/Group].
        This software is free for academic and research purposes.
        **Mandatory Citation:** If you use this software in a published research, cite it as:
        * [Developer Name/Group]. **FluxIQ: Franz Cell Analyzer** (Version {APP_VERSION}). [Year of Use]. Available at [Repository/Platform URL].
        """,
    }
}

# --- Página Inicial (Home) --- 
def render_home(T):
    st.title(T['app_title'])
    st.markdown(f"### {T['app_description']}")
    st.markdown("---")
    
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
        # A mensagem de erro já foi exibida no bloco 'try'/'except'
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
    lang_choice = st.sidebar.selectbox("Language / Idioma", ["Português", "English"], index=1)
    st.session_state.lang = 'pt' if lang_choice == "Português" else 'en'
    T = TEXT_DICT[st.session_state.lang]

    # Configuração da Página (Primeiro comando Streamlit no fluxo de execução)
    st.set_page_config(layout="wide", page_title=T['app_title'])
    
    # A navegação principal está na sidebar
    st.sidebar.title(T['sidebar_nav'])
    
    # --- REMOVIDO: Exibição da versão na Sidebar ---
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