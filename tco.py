import streamlit as st
import requests
import streamlit.components.v1 as components

def input(label,value):
    html_code = f"""
                    <style>
                        .custom-input {{
                            background-color: #F0F2F6;
                            color: #62666D;
                            font-size: 15px;
                            padding: 8px;
                            border: 1px solid #F0F2F6;
                            border-radius: 8px;
                            width: 100%;
                            box-sizing: border-box;
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        }}
                        .custom-label {{
                            font-size: 15px;
                            color: #62666D;
                            display: block;
                            margin-bottom: 4px;
                        }}
                    </style>
                    <div>
                        <label class="custom-label">{label}</label>
                        <input type="text" value="{value}" disabled class="custom-input"/>
                    </div>
                """
    return html_code

def request(placa,empresa):

    url = 'https://apps-luke-dot-autoavaliar-apps.appspot.com//usbi/syncService/getValuation'  # Substitua pela URL do endpoint
    headers = {
        'Content-Type': 'application/json',  # Tipo de conteúdo
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcHBzLWx1a2UtZG90LWF1dG9hdmFsaWFyLWFwcHMuYXBwc3BvdC5jb20iLCJpYXQiOjE3MjI4NzU0NTIsImp0aSI6IjgyN2Y3YzJhM2NhOWQzNjllYjQ0OGUyMzE3Yjg1ZjEyNzQ4NDJhMGMiLCJuYmYiOjE3MjI4NzU0NTIsImV4cCI6MTcyMjk2MTg1MiwiZGF0YSI6eyJjb3VudHJ5X2lkIjoiNzYiLCJpbnN0YW5jZV9pZCI6IjEzMjQ5MSIsInRva2VuX2lkIjoxODkxMzE0MjUsInR5cGUiOiJhdXRob3JpemF0aW9uIn19.Z-APQv9XfZlEjp3BG_TEen22bVa3uEX9FICTXf3bWKY",  # Cabeçalho de autorização, se necessário
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
    avaliacao = request(placa,emp_selecionada)
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("DADOS DA AVALIAÇÃO",divider="gray")
        st.markdown(input("Veiculo Avaliado",avaliacao['vehicle']['model']['name'] + " " + avaliacao['vehicle']['version']['name']),unsafe_allow_html=True)
        st.markdown(input("Veiculo de Interesse",value=avaliacao['interested_vehicle']),unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(input("KM",value=avaliacao['vehicle']['mileage']),unsafe_allow_html=True)
        with col2:
            st.markdown(input("Ano Fabricação",value=avaliacao['vehicle']['year']),unsafe_allow_html=True)


        col1, col2 = st.columns(2)
        with col1:
            st.markdown(input("Finalidade",value=avaliacao['goal_name']),unsafe_allow_html=True)
        with col2:
            st.markdown(input("Classificacao",value=classificacao[avaliacao['rating']]),unsafe_allow_html=True)
    with col4:

        st.subheader("REFERÊNCIAS DE GARANTIA",divider="gray")
        st.markdown(input("Marca",value=avaliacao['vehicle']['make']['name']),unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            st.markdown(input("Ano Fabricacao",value=avaliacao['vehicle']['assembly']),unsafe_allow_html=True)
        with col6:
            st.markdown(input("Anos de Garantia",value="3"),unsafe_allow_html=True)
    st.subheader("REFERÊNCIAS",divider="gray")

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
#st.text_input(label="Valor Avaliado",value=avaliacao['valuation_value'],disabled=True)