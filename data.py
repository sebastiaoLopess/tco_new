import streamlit as st
import requests
import streamlit.components.v1 as components
import pandas as pd
import json
import datetime
from datetime import date

def gera_token():
    url = 'https://apps-luke-dot-autoavaliar-apps.appspot.com/ego/syncService/refreshToken'
    headers = {
        'Content-Type': 'application/json',  # Tipo de conteúdo
        "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcHBzLmF1dG9hdmFsaWFyLmNvbS5iciIsImlhdCI6MTcxNjkxNTcxNywianRpIjoiNDlkMGM1NWM3YmMxZjVmYWIzNzU0MDA2OTY2ODdlYWQ3YjZjMzE0NyIsIm5iZiI6MTcxNjkxNTcxNywiZXhwIjoxNzQ4MDIwMzY3LCJkYXRhIjp7ImNvdW50cnlfaWQiOiI3NiIsImluc3RhbmNlX2lkIjoiMTMyNDkxIiwidG9rZW5faWQiOjE3OTI1OTY5OSwidHlwZSI6InJlZnJlc2gifX0.kCAJIwuT2KQ-6ZGGMAD6oMTRqcXbw-cvDOMGpxa5zZg"
    }

    response = requests.post(url, headers=headers)
    data = response.json()
    token = data['data']['token']

    return token

def consulta_auto_avaliar(placa,empresa):

    token = gera_token()

    url = 'https://apps-luke-dot-autoavaliar-apps.appspot.com//usbi/syncService/getValuation'  # Substitua pela URL do endpoint
    headers = {
        'Content-Type': 'application/json',  # Tipo de conteúdo
        "token": token,  # Cabeçalho de autorização, se necessário
        "signature": "9587915e-367335b4-e286dbc4-35585857-db78c0c5"
    }

    body = {
        "send_images": False, 
        "plate": placa, 
        "entity_id": empresa, 
        "get_tag_report": False, 
        "use_city_state_vehicle": True, 
        "use_svt": False, 
        "use_cod_fipe": True, 
        "require_solicitation": False,
        "status": [2,3,6],
        "get_reference_value": True,
        "use_valuations_answers":True
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    avaliacao = data['data']

    return avaliacao

def consulta_estoque(placa):
    url = 'https://c8b8-200-194-101-215.ngrok-free.app'
    response = requests.get(url, params={'placa': placa})
    data = response.json()
    return data

def trata_estoque(data):
    json_data = json.loads(data)
    df = pd.DataFrame.from_records(json_data)
    if df.empty:
        df = df
    else:
        df.set_index('ve_placa')
        df['me_dtent'] = pd.to_datetime(df['me_dtent'], unit='ms').dt.strftime('%d/%m/%Y')
        df['me_dtsai'] = pd.to_datetime(df['me_dtsai'], unit='ms').dt.strftime('%d/%m/%Y')
        columns = ['ve_placa','mod_ds','est_ds','me_dtent','me_dtsai']
        df = df[columns].sort_values(by='me_dtsai',ascending=True)
    return df

def trata_data(dt_aval):
    data = datetime.datetime.fromtimestamp(dt_aval)
    nova_data = data.strftime('%d/%m/%Y')
    return nova_data

def ano_garantia(marca):
    tab_garantia = pd.read_csv('tab_garantia.csv',sep=';',index_col = 'marca')
    garantia = tab_garantia.loc[marca,'garantia']
    return garantia

def tem_garantia(marca,ano_modelo):
    tab_garantia = pd.read_csv('tab_garantia.csv',sep=';',index_col = 'marca')
    garantia = tab_garantia.loc[marca,'garantia']
    ano_atual = date.today().year
    ano_garantia = ano_modelo + garantia
    prazo_garantia = ano_garantia - ano_atual

    status_garantia = ''
    if prazo_garantia < 0:
        status_garantia = 'Fora da Garantia'
    else:
        status_garantia = f'Garantia vai até {ano_garantia}'
    return status_garantia


def resposta(questions,id_pergunta):
    resposta = ''
    for question in questions:
        if question['question_id'] == id_pergunta:
            resposta = question['answer']
            break
    return resposta


