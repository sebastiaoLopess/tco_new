import streamlit as st
import requests
import streamlit.components.v1 as components
import pandas as pd
import json
import datetime
from datetime import date,datetime
import pickle
import re

def gera_token():
    url = 'https://apps-luke-dot-autoavaliar-apps.appspot.com/ego/syncService/refreshToken'
    headers = {
        'Content-Type': 'application/json',  # Tipo de conteúdo
        "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcHBzLWx1a2UtZG90LWF1dG9hdmFsaWFyLWFwcHMuYXBwc3BvdC5jb20iLCJpYXQiOjE3NDI3NTc2NDQsImp0aSI6IjgyN2Y3YzJhM2NhOWQzNjllYjQ0OGUyMzE3Yjg1ZjEyNzQ4NDJhMGMiLCJuYmYiOjE3NDI3NTc2NDQsImV4cCI6MTc3Mzg2MjI5NCwiZGF0YSI6eyJjb3VudHJ5X2lkIjoiNzYiLCJpbnN0YW5jZV9pZCI6MTMyNDkxLCJ0b2tlbl9pZCI6MjIyNjg2ODU1LCJ0eXBlIjoicmVmcmVzaCJ9fQ.7CVQO3Po3h7XrwjtpeL5h0R64_51-NtauTzm--e7BPE"
    }

    response = requests.post(url, headers=headers)
    data = response.json()
    token = data['data']['token']
    expires_in = data['data']['expires_in']

    meu_dict = {
        'expires_in': expires_in,
        'token': token
    }

    with open('historico_token.pickle', 'wb') as f:
        pickle.dump(meu_dict, f)

    return token

def atualiza_token():
    with open('historico_token.pickle', 'rb') as f:
        meu_dict = pickle.load(f)
        data_exp = meu_dict['expires_in']
        dt_split = data_exp.split()[0]
        data_expiracao = datetime.strptime(dt_split, "%Y-%m-%d")


    data_hoje = date.today()
    hoje = datetime.combine(data_hoje, datetime.min.time())

    check_data = hoje < data_expiracao

    token = ''

    if check_data:
        token = meu_dict['token']
        #print("verdadeiro")
        #print(meu_dict)
    
    else:
        token = gera_token()
        '''print("falso")
        with open('historico_token.pickle', 'rb') as f:
            meu_dict = pickle.load(f)
            data_exp = meu_dict['expires_in']
            dt_split = data_exp.split()[0]
            data_expiracao = datetime.strptime(dt_split, "%Y-%m-%d")
        print(meu_dict)
        '''
    return token

def consulta_auto_avaliar(placa,empresa):

    token = atualiza_token()

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

    if response.status_code == 200:
        try:
            # Tente decodificar a resposta como JSON
            data = response.json()
            avaliacao = data['data']
            return avaliacao
        except requests.exceptions.JSONDecodeError:
            print("Erro ao decodificar a resposta JSON. Resposta não está em formato JSON.")
            print(f"Conteúdo da resposta: {response.text}")
            return None
    else:
        print(f"Erro na requisição: {response.status_code}")
        print(response.status_code)
        return response.status_code



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
    data = datetime.fromtimestamp(dt_aval)
    nova_data = data.strftime('%d/%m/%Y')
    return nova_data

def ano_garantia(marca):
    tab_garantia = pd.read_csv('tab_garantia.csv',sep=';',index_col = 'marca')
    try:
        garantia = tab_garantia.loc[marca,'garantia']
    except KeyError:
        garantia = 0
    return garantia

def tem_garantia(marca,ano_modelo):
    tab_garantia = pd.read_csv('tab_garantia.csv',sep=';',index_col = 'marca')

    try:
        garantia = tab_garantia.loc[marca,'garantia']
    except KeyError:
        garantia = 0

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

def referencias_media(references,id_reference):
    referencia = ''
    for reference in references:
        if reference['id'] == id_reference:
            resposta = reference['avg_value']
            break
    return resposta

def referencias_min(references,id_reference):
    referencia = ''
    for reference in references:
        if reference['id'] == id_reference:
            resposta = reference['min_value']
            break
    else:
        resposta = 0
    return resposta


def referencias_max(references,id_reference):
    referencia = ''
    for reference in references:
        if reference['id'] == id_reference:
            resposta = reference['max_value']
            break
    return resposta

def trata_itens(data):
    df = pd.json_normalize(data)
    if df.empty:
        df = df
    else:
        columns = ['name','obs','expenses_value']
        df = df[columns]
        df.rename(columns={'name': 'Item', 'obs': 'Obs','expenses_value': 'Valor Despesa'},inplace=True)
    return df

def define_placa(placa):
    
    quinto_carac = placa[4].lower()
    placa_azul = re.findall("[a-z]", quinto_carac)
    placa_cinza = re.findall("[0-9]", quinto_carac)
    modelo_placa = ""

    if placa_azul:
        modelo_placa = "PLACA AZUL"
    else:
        modelo_placa = "PLACA CINZA"

    return modelo_placa
