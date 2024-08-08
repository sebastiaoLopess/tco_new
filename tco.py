import streamlit as st
import requests
import streamlit.components.v1 as components
import pandas as pd
import json
from components import input 
from data import consulta_auto_avaliar,consulta_estoque,trata_estoque,ano_garantia,tem_garantia,resposta,trata_data
from paginas import dados_da_avaliacao,referencias_garantia,referencias


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
      "Nossa Moto": "101204600",
      "BYD Teresina": "101212127",
      "BYD Natal": "101212126",
      "GWM SLZ": "101212128"      
}

classificacao = {
      int(1): "A",
      int(2): "B",
      int(3): "C",
      int(4): "D",
      int(5): "E"
}

empresas = list(opcoes.keys())

st.header("TCO CARMAIS", divider="gray")
placa = st.text_input("Placa")
empresa = st.selectbox(
    "Empresa",
    empresas
)

emp_selecionada = opcoes[empresa]

button = st.button("Gerar TCO", type="primary")

if button:
    avaliacao = consulta_auto_avaliar(placa,emp_selecionada)
    estoque = consulta_estoque(placa)
    df_estoque = trata_estoque(estoque)
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("DADOS DA AVALIAÇÃO",divider="gray")

        dados_da_avaliacao(avaliacao,classificacao)
    with col4:

        st.subheader("DADOS DE GARANTIA",divider="gray")

        referencias_garantia(avaliacao,classificacao)

    st.subheader("REFERÊNCIAS",divider="gray")

    referencias(avaliacao,classificacao)

    st.subheader("MOVIMENTAÇÃO ESTOQUE",divider="gray")
    st.table(df_estoque)
#st.text_input(label="Valor Avaliado",value=avaliacao['valuation_value'],disabled=True)