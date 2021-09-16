#Projeto 2 - Construindo um dashboard
#'Previsão do preço de ações (NASDAQ)'

# Bibliotecas
import time
import pandas as pd
import numpy as np

import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from pandas_datareader.data import DataReader
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols

import datetime as dt
import streamlit as st

from fbprophet import Prophet
from fbprophet.plot import plot_plotly

import warnings

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#init_notebook_mode(connected=True)
cf.go_offline()


# Parametrizações ##################################################
#sns.set_style('whitegrid')
#plt.style.use("fivethirtyeight")
st.set_option('deprecation.showPyplotGlobalUse', False)
#plt.rcParams['axes.facecolor'] = 'white'

# Funções #########################################################
#@st.cache
def plot_candlestick(df, acao):
    load_state.text('Loading graphic candlestick...')
    fig = go.Figure(data=
        [go.Candlestick(x=df.index,
                        open=df["Open"],
                        high=df["High"],
                        low=df["Low"],
                        close=df["Close"])]
    )
    fig.update_layout(
        title=f"Value of {acao}",
        yaxis_title="Price ($)"
    )
    st.plotly_chart(fig)
    return

def plot_line(df, company_name):
    load_state.text('Loading graphic line...')
    year_min = df.Year.min()
    year_max = df.Year.max()
    fig = px.line(df, 
                  x=df.index, 
                  y="Adj Close",
                  title= f'{company_name} - Stock price ({year_min} - {year_max})',
                  labels={'x':'Year','y':'Price'}
                 )
    st.plotly_chart(fig)
    return

def plot_bar(df, company_name):
    load_state.text('Loading graphic bar...')
    dfbar=df.groupby('Year')['Adj Close'].mean()
    fig = px.bar(dfbar, 
                 x=dfbar.index, 
                 y=dfbar.values, 
                 title = f'{company_name} - Average Value',
                 labels={'x':'Year','y':'Price'}                 
                )
    st.plotly_chart(fig)
    return

def plot_bubble(acao, company_name):
    load_state.text('Loading graphic bubble...')
    dfbb = df_dict[acao].reset_index()
    dfbb = dfbb.loc[dfbb['Year']==dfbb.Year.max(),['Date','Adj Close','Volume','Year','Month']]
    fig = px.scatter(dfbb, 
                     x="Date", 
                     y="Adj Close", 
                     labels={'x':'Year','y':'Price'},
                     size='Volume',
                     color='Month',
                     title = f'{company_name} - Stock price'
                    )
    st.plotly_chart(fig)
    return

def plot_box(df, company_name):
    load_state.text('Loading graphic boxplot...')
    fig = px.box(df, 
                 x="Year", 
                 y="Adj Close",
                 title = f'{company_name} - Boxplot Stock price',
                 labels={'x':'Year','y':'Price'}
                )
    st.plotly_chart(fig)
    return

def plot_hist(df, company_name):
    load_state.text('Loading graphic histogram...')
    year_min = df.Year.min()
    year_max = df.Year.max()    
    fig = px.histogram(df, x="Adj Close",
                      title= f'{company_name} - Stock price ({year_min} - {year_max})',
                      labels={'x':'Year','y':'Price'})
    st.plotly_chart(fig)
    return

def plot_area(df, company_name):
    load_state.text('Loading graphic area...')
    year_min = df.Year.min()
    year_max = df.Year.max()    
    fig = px.area(y=df["Adj Close"],
                  x=df.index,
                  title= f'{company_name} - Stock price ({year_min} - {year_max})',
                  labels={'x':'Year','y':'Price'})
    fig.update_layout(showlegend = False)
    st.plotly_chart(fig)
    return

def plot_cufflinks(df, company_name):
    load_state.text('Loading graphic "cufflinks"...')
    columns = ["High", "Low", "Open", "Close", "Volume"]
    year_min = df.Year.min()
    year_max = df.Year.max()    
    fig = df[columns].iplot(
                asFigure=True, 
                xTitle="Date",
                yTitle="Price", 
                title=f'{company_name} - ({year_min} - {year_max})')
    st.plotly_chart(fig)
    return

def make_forecast(acao, period):
    load_state.text(f'{acao} - Processing ML prophet (forecast calculations)...')
    df = df_dict[acao].reset_index()
    df_train = df[["Date", "Close"]]
    df_train = df_train.rename(columns={'Date': 'ds', 'Close': 'y'})
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    return m, forecast


# Side Bar #######################################################
project_title = st.sidebar.text_input(label="Project title",
                                      value="Forecast stock calculations")



dt_end = dt.datetime.now().date()
dt_start = st.sidebar.date_input('Start date', dt.date(dt_end.year - 4, 1, 1))
dt_end = st.sidebar.date_input('End date')

n_years = st.sidebar.slider('Years of forecast', 1, 4, 1)
period = n_years * 365

# Criando a lista de ações da Nasdaq para multipla seleção
symbols = get_nasdaq_symbols()
acoes = symbols["NASDAQ Symbol"]

# Selecionando várias ações selecionadas
acoes_selected = st.sidebar.multiselect('Select stocks', acoes)
mask_acoes = symbols["NASDAQ Symbol"].isin(acoes_selected)
filtro_acoes = mask_acoes > 0
acao_list = mask_acoes[filtro_acoes].index.values.tolist()

run_button = st.sidebar.button(label='Execute')


# BODY ################################################################################################################
st.title(project_title)

if run_button:
    if len(acao_list) == 0:
        data_load_state = st.text('Please select stocks...')
    else:
        # Define a data final para o periodo de download das ações
        dt_end = dt.datetime.now().date()

        # Verifica se a data inicial da previsão é compatível, deve ter pelo menos 1 ano para efetuar a previsão
        # Se a data final for menor ou igual a data inicial a data inicial será decrescida em 1 ano 
        if dt_end <= dt_start:
            dt_start = dt.datetime(dt_end.year - 4, dt_end.month, dt_end.day).strftime('%Y-%m-%d')

        data_load_state = st.text('Downloading information...')
        load_state = st.text('')

        my_bar = st.progress(0)
        percent_complete = 0

        company_list = list()

        #Efetuando o download dos dados financeiros yahoo e criando os dataframes
        df_dict = dict()      
        for acao in acao_list:
            load_state.text(f'Download: {acao}')
            try: 
                df_dict[acao] = DataReader(acao, 'yahoo', dt_start, dt_end)
                df_dict[acao]["Year"] = pd.DatetimeIndex(df_dict[acao].index).year
                df_dict[acao]["Month"] = pd.DatetimeIndex(df_dict[acao].index).month

                filtro = symbols["NASDAQ Symbol"]==acao
                acao_company = symbols.loc[filtro, "Security Name"].values[0]    
                acao_company = acao_company.split('Common Stock', 1)[0]
                acao_company = acao_company.split('-', 1)[0]
                company_list.append(acao_company)
                load_state.text(f'Information {acao} successfully updated!')

                percent_complete += (0.2/len(acao_list))
                my_bar.progress(percent_complete)

            except:
                load_state.text (f'Information {acao} not found!')
                percent_complete += (0.2/len(acao_list))
                my_bar.progress(percent_complete)               

        data_load_state.text('Creating graphics')
        load_state.text('')
        
        for i, acao in enumerate(acao_list, 1):
            try: 
                company_name = company_list[i - 1]
                new_title = f'<p style="font-family:sans-serif; color:Green; font-size: 22px;">{acao} - {company_name}</p>'
                st.markdown(new_title, unsafe_allow_html=True)        
                st.write()
                
                plot_cufflinks(df_dict[acao], company_name)
                percent_complete += (0.1/len(acao_list))
                my_bar.progress(percent_complete)
                
                plot_bubble(acao, company_name)
                percent_complete += (0.1/len(acao_list))
                my_bar.progress(percent_complete)
                
                #plot_hist(df_dict[acao], company_name)

                plot_area(df_dict[acao], company_name)
                percent_complete += (0.1/len(acao_list))
                my_bar.progress(percent_complete)

                plot_bar(df_dict[acao], company_name)
                percent_complete += (0.1/len(acao_list))
                my_bar.progress(percent_complete)

                plot_box(df_dict[acao], company_name)
                percent_complete += (0.1/len(acao_list))
                my_bar.progress(percent_complete)
                
                #plot_line(df_dict[acao], company_name)        
                #plot_candlestick(df_dict[acao], acao)

                m, forecast = make_forecast(acao, period)
                st.subheader(f'FB Prophet forecast to {acao} from {period} days')
                fig_forecast = plot_plotly(m, forecast)
                st.plotly_chart(fig_forecast)
                percent_complete += (0.3/len(acao_list))
                my_bar.progress(round(percent_complete,2))

                #st.subheader(f'Explaining the characteristics of the forecast model')
                #fig_components = m.plot_components(forecast)
                #st.write(fig_components)
            except:
                new_title = f'<p style="font-family:sans-serif; color:Green; font-size: 22px;">{acao}</p>'
                st.markdown(new_title, unsafe_allow_html=True)
                st.write()
                
                load_state.text (f'Information {acao} not found!')
                percent_complete += (0.8/len(acao_list))
                my_bar.progress(round(percent_complete,2))
                
                except_title = f"<p style='font-family:sans-serif; color:Red; font-size: 12px;'>Sorry, we can't find the download information.</p>"
                st.markdown(except_title, unsafe_allow_html=True)        
                st.write()
                    
        data_load_state.text('Prediction created!')
        #data_load_state.text('')
        load_state.text('')
