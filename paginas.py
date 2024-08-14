import streamlit as st
import requests
import streamlit.components.v1 as components
import pandas as pd
import json
from components import input 
from data import consulta_auto_avaliar,consulta_estoque,trata_estoque,ano_garantia,tem_garantia,resposta,trata_data,referencias_media,referencias_min,referencias_max,trata_itens

def dados_da_avaliacao(avaliacao,classificacao):

    st.markdown(input("Data Avaliação",trata_data(avaliacao['valuation_date'])),unsafe_allow_html=True)
    st.markdown(input("Veiculo Avaliado",avaliacao['vehicle']['model']['name'] + " " + avaliacao['vehicle']['version']['name']),unsafe_allow_html=True)
    st.markdown(input("Veiculo de Interesse",value=avaliacao['interested_vehicle']),unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(input("KM",value=avaliacao['vehicle']['mileage']),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Ano Fabricação",value=avaliacao['vehicle']['year']),unsafe_allow_html=True)


    col3, col4 = st.columns(2)
    with col3:
        st.markdown(input("Finalidade",value=avaliacao['goal_name']),unsafe_allow_html=True)
    with col4:
        st.markdown(input("Classificacao",value=classificacao[avaliacao['rating']]),unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown(input("Tipo de Avaliação",value=avaliacao['valuation_type_name']),unsafe_allow_html=True)
    with col6:
        st.markdown(input("Municipio Vec",value=avaliacao['vehicle']['city']),unsafe_allow_html=True)
    col7, col8 = st.columns(2)
    with col7:
        st.markdown(input("Avaliador",value=avaliacao['valuer']['name']),unsafe_allow_html=True)
    with col8:
        st.markdown(input("Vendedor",value=avaliacao['user']['name']),unsafe_allow_html=True)
    col9, col10, col11 = st.columns(3)
    with col9:
        st.markdown(input("Cor",value=avaliacao['vehicle']['color']['name']),unsafe_allow_html=True)
    with col10:
        st.markdown(input("Combustivel",value=avaliacao['vehicle']['fuel']['name']),unsafe_allow_html=True)
    with col11:
        st.markdown(input("Transmissão",value=avaliacao['vehicle']['transmission']['name']),unsafe_allow_html=True)

def referencias_garantia(avaliacao,classificacao):

        st.markdown(input("Marca",value=avaliacao['vehicle']['make']['name']),unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(input("Ano Fabricacao",value=avaliacao['vehicle']['assembly']),unsafe_allow_html=True)
        with col2:
            st.markdown(input("Anos de Garantia",value=ano_garantia(avaliacao['vehicle']['make']['name'],)),unsafe_allow_html=True)
        st.markdown(input("Provavel Garantia",value=tem_garantia(avaliacao['vehicle']['make']['name'],avaliacao['vehicle']['assembly'])),unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(input("Concessionaria Origem",value=resposta(avaliacao['questions'],240)),unsafe_allow_html=True)
        with col4:
            st.markdown(input("Revisoes Garantia",value= ("Sim" if resposta(avaliacao['questions'],154) == "1" else "Nao")),unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            st.markdown(input("Revisão 10.000KM",value= ("Sim" if resposta(avaliacao['questions'],241) == "1" else "Nao")),unsafe_allow_html=True)
        with col6:
            st.markdown(input("Revisão 20.000KM",value= ("Sim" if resposta(avaliacao['questions'],242) == "1" else "Nao")),unsafe_allow_html=True)
        st.markdown(input("Revisão 30.000KM",value= ("Sim" if resposta(avaliacao['questions'],243) == "1" else "Nao")),unsafe_allow_html=True)

def referencias(avaliacao,classificacao):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(input("Valor Avaliado",value=avaliacao['valuation_value']),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Gasto Previsto",value=avaliacao['expenses_value']),unsafe_allow_html=True)
    with col3:
        st.markdown(input("Top",value=avaliacao['top_dealer']),unsafe_allow_html=True)
    with col4:
        custo = avaliacao['valuation_value'] + avaliacao['expenses_value']
        st.markdown(input("Custo",value=custo),unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown(input("Fipe",value=avaliacao['fipe_value']),unsafe_allow_html=True)
    with col6:
        percent_fipe = (custo / avaliacao['fipe_value'])*100
        st.markdown(input("% fipe",value=f"{int(percent_fipe)} %"),unsafe_allow_html=True)

    col7, col8, col9, col10 = st.columns(4)
    with col7:
        st.markdown(input("Compra Fortaleza",value=referencias_media(avaliacao['references'],2)),unsafe_allow_html=True)
    with col8:
        st.markdown(input("Compra CE",value=referencias_max(avaliacao['references'],2)),unsafe_allow_html=True)
    with col9:
        st.markdown(input("Compra Brasil",value=referencias_min(avaliacao['references'],2)),unsafe_allow_html=True)

    col11, col12, col13, col14 = st.columns(4)
    with col11:
        st.markdown(input("B2B Fortaleza",value=referencias_media(avaliacao['references'],8)),unsafe_allow_html=True)
    with col12:
        st.markdown(input("B2B Ceara",value=referencias_max(avaliacao['references'],8)),unsafe_allow_html=True)
    with col13:
        st.markdown(input("B2B Brasil",value=referencias_min(avaliacao['references'],8)),unsafe_allow_html=True)

    col15, col16, col17, col18 = st.columns(4)
    with col15:
        st.markdown(input("B2C Fortaleza",value=referencias_media(avaliacao['references'],7)),unsafe_allow_html=True)
    with col16:
        st.markdown(input("B2C Ceara",value=referencias_max(avaliacao['references'],7)),unsafe_allow_html=True)
    with col17:
        st.markdown(input("B2C Brasil",value=referencias_min(avaliacao['references'],7)),unsafe_allow_html=True)

    st.markdown(input("WEB MOTORS",value=referencias_min(avaliacao['references'],1)),unsafe_allow_html=True)

    st.markdown(input("Sugestao de Venda",value=avaliacao['proposed_value']),unsafe_allow_html=True)

    st.markdown(input("Expectativa do Cliente",value=avaliacao['expected_value']),unsafe_allow_html=True)

def itens_avaliados(avaliacao):

    st.table(trata_itens(avaliacao['items']))
