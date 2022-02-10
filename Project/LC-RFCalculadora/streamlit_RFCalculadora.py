# Avaliação – Produto Renda Fixa
# Construção de uma calculadora de renda fixa em Python - NTN-F

# Bibliotecas
import datetime as dt
from dateutil.relativedelta import relativedelta
import streamlit as st
import warnings

# importando a biblioteca RFCalculadora
from RFCalculadora import RFCalculadora

# Instanciando o objeto com a classe RFCalculadora
ntnF = RFCalculadora()


# Parametrizações ########################################################################################################
#sns.set_style('whitegrid')
#plt.style.use("fivethirtyeight")
st.set_option('deprecation.showPyplotGlobalUse', False)
#plt.rcParams['axes.facecolor'] = 'white'

# Funções ################################################################################################################



# Side Bar ###############################################################################################################
#project_title = st.sidebar.text_input(label="Calculadora de Renda Fixa",
#                                      value=tp_calculo)

tp_calculo = st.sidebar.selectbox('Calculadora', ("Titulos NTN-F", "Titulos NTN-B"))

dt_entrada = dt.datetime.now().date()
dt_entrada = dt_entrada - relativedelta(days=1)
dt_entrada = st.sidebar.date_input('Data Entrada', dt_entrada)
dt_vencimento = st.sidebar.date_input('Data Vencimento', dt.date(dt_entrada.year + 5, 1, 1))
tx_anual = st.sidebar.number_input('Rentabilidade Anual')

run_button = st.sidebar.button(label='Execute')


# BODY ###################################################################################################################
st.title('Calculo ' + tp_calculo)
    
carrega_feriado = 0

if run_button:
    if dt_vencimento <= dt_entrada:
        data_load_state = st.text('A data de vencimento é menor ou igual a data de entrada. Preencha as datas corretamente.')
            
    else:
        data_load_state = st.text('Preparando informações...')
        load_state = st.text('')

        my_bar = st.progress(0)
        percent_complete = 0

        if carrega_feriado == 0:
            # Carrega planilha de feriados
            caminho_arquivo = '.\\dados\\feriados_nacionais.xls'
            load_state.text(f'Carregando planilha de Feriados {caminho_arquivo}')
            df = ntnF.Carrega_Feriados(caminho_arquivo)
            load_state.text(f'Carga da planilha efetuada com sucesso!')
            percent_complete += (0.2)
            my_bar.progress(percent_complete)
            carrega_feriado = 1
        else:
            percent_complete += (0.2)
            my_bar.progress(percent_complete)

        data_load_state.text('Calculando informações...')
        load_state.text('')

        dt_entrada_str = dt_entrada.strftime("%d/%m/%Y")
        dt_vencimento_str = dt_vencimento.strftime("%d/%m/%Y")
                                                
        # Calculadora NTN-F
        if tp_calculo == "Titulos NTN-F":
            vl_nominal = 1000
            D1=1
            df_fluxo, vl_principal, vl_pu_ntnf = ntnF.Calcula_PU_NTNF(dt_entrada_str, dt_vencimento_str, vl_nominal, tx_anual, D1)
            percent_complete += (0.7)
            my_bar.progress(percent_complete)

            df_fluxo.rename(columns = {'Data_Entrada': 'Data Entrada', 'Data_Compra': 'Data Compra', 'Data_Pagamento': 'Data Vencimento'}, inplace = True)
            st.write(f'Título Prefixado com juros semestrais {dt_vencimento.strftime("%Y")}')
            st.write(f'Valor do Preço Unitário: {vl_pu_ntnf}')
            st.dataframe(df_fluxo)
            percent_complete += (0.1)
            my_bar.progress(percent_complete)
            data_load_state.text('Calculo efetuado!')
            
        elif tp_calculo == "Titulos NTN-B":
                st.write(f'A calculdora ainda não esta disponível! Estamos trabalhando nisso...')
                my_bar.progress(100)
                data_load_state.text('')
        
        load_state.text('')
