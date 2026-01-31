import streamlit as st
import requests
import streamlit.components.v1 as components
import pandas as pd
import json
from components import input 
from data import consulta_auto_avaliar,consulta_estoque,trata_estoque,ano_garantia,tem_garantia,resposta,trata_data,consulta_revisao
from paginas import dados_da_avaliacao,referencias_garantia, referencias, itens_avaliados


opcoes = {
      "Vouga": "101204609",
      "CDA": "101204610",
      "Sanauto": "101185528",
      "Jangada Renault": "101204604",
      "Nissan MT": "101204600",
      "Nissan WS": "101204608",
      "BYD Carmais": "101204605",
      "Honda BS": "101204612",
      "Honda WS": "101204684",
      "Honda SD": "101204686",
      "Honda SUL": "101204687",
      "NOSSAMOTO - HONDA": "101204688",
      "BYD Teresina": "101212127",
      "BYD Natal": "101212126",
      "GWM SLZ": "101212128",
      "NOSSAMOTO BATURITE": "101247207",
      "NOSSAMOTO CONJUNTO CEARA": "101247174",
      "NOSSAMOTO SIQUEIRA": "101247183",
      "GEELY": "101258510"     
}

classificacao = {
      int(1): "A",
      int(2): "B",
      int(3): "C",
      int(4): "D",
      int(5): "E"
}

cod_auth = [
            7582,
            4218,
            7735,
            6045,
            1079,
            5139,
            9099,
            4529,
            1707,
            6577,
            1631,
            8063,
            9456,
            7687,
            2274,
            6882,
            3604,
            6334,
            2094,
            5031,
            5516,
            7343,
            3059,
            9369,
            8184,
            4197,
            3578,
            5711,
            1350,
            1292,
            9595,
            1982,
            2204,
            7962,
            6111,
            6010,
            6498,
            7898,
            9713,
            8431,
            4927,
            6382,
            4621,
            7891,
            9149,
            6149,
            5381,
            9478,
            3341,
            7184,
            5145,
            2074,
            6556,
            1696,
            3616,
            3105,
            5541,
            5418,
            5938,
            1484,
            6732,
            2254,
            8784,
            4309,
            1240,
            9433,
            5722,
            4312,
            2268,
            8162,
            4070,
            6001,
            3698,
            1786,
            1151
            ]

empresas = list(opcoes.keys())

st.header("TCO CARMAIS", divider="gray")
col1, col2 = st.columns(2)
with col1:
    placa = st.text_input("Placa")
with col2:
    autenticator = st.text_input("Autenticador",type="password")

empresa = st.selectbox(
    "Empresa",
    empresas
)

emp_selecionada = opcoes[empresa]

button = st.button("Gerar TCO", type="primary")

if button and autenticator in str(cod_auth) and autenticator:

    avaliacao = consulta_auto_avaliar(placa,emp_selecionada)

    #revisoes = consulta_revisao(placa)


    #estoque = consulta_estoque(placa)
    #df_estoque = trata_estoque(estoque)
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("DADOS DA AVALIAÇÃO",divider="gray")

        dados_da_avaliacao(avaliacao,classificacao)
    with col4:

        st.subheader("DADOS DE GARANTIA",divider="gray")

        referencias_garantia(avaliacao,classificacao)

    st.subheader("REFERÊNCIAS",divider="gray")

    referencias(avaliacao,classificacao)

    st.subheader("ITENS AVALIADOS",divider="gray")

    itens_avaliados(avaliacao)

    #st.subheader("REVISÕES",divider="gray")
    #st.dataframe(revisoes)


    #st.subheader("MOVIMENTAÇÃO ESTOQUE",divider="gray")
    #st.table(df_estoque)
