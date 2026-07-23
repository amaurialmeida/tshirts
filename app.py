import streamlit as st
import pandas as pd

# Configuração da página em modo wide com o novo título
st.set_page_config(page_title="Camisas de Futebol Amauri ⚽", layout="wide", page_icon="⚽")

# --- NUMERO DO WHATSAPP OBTIDO DA SUA TAG ---
WHATSAPP_NUMERO = "5511942762908"

# --- CSS CUSTOMIZADO ---
st.markdown("""
    <style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Barra de busca arredondada */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 12px 20px !important;
        font-size: 0.95rem !important;
        background-color: #f8fafc !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #c026d3 !important;
        box-shadow: 0 0 0 2px rgba(192, 38, 211, 0.2) !important;
    }

    /* Container do Card do Produto */
    .product-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 10px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 20px;
        border: 1px solid #f1f5f9;
    }
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Estilo do Preço */
    .preco-atual {
        font-size: 1.15rem;
        font-weight: 700;
        color: #6b21a8;
        display: inline-block;
        margin-right: 6px;
    }
    .preco-original {
        font-size: 0.88rem;
        color: #94a3b8;
        text-decoration: line-through;
    }

    /* Tags estilo vitrine */
    .tag-barateou {
        background-color: #facc15;
        color: #0f172a;
        font-weight: 700;
        font-size: 0.72rem;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: lowercase;
        display: inline-block;
        margin-top: 6px;
        margin-bottom: 4px;
    }
    .tag-desconto {
        background-color: #e9d5ff;
        color: #6b21a8;
        font-weight: 700;
        font-size: 0.72rem;
        padding: 2px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-top: 6px;
        margin-bottom: 4px;
    }

    /* Título e detalhes da camisa */
    .titulo-camisa {
        font-size: 0.9rem;
        color: #334155;
        font-weight: 500;
        margin-top: 4px;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .subtitulo-camisa {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 8px;
    }

    /* Botão de WhatsApp Roxo */
    .btn-comprar {
        display: block;
        width: 100%;
        background-color: #c026d3;
        color: white !important;
        text-align: center;
        padding: 8px 0px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        text-decoration: none !important;
        transition: background-color 0.2s;
    }
    .btn-comprar:hover {
        background-color: #a21caf;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS ---
@st.cache_data
def carregar_dados():
    data = [
        # BRASIL
        {
            "id": 1,
            "titulo": "camisa sao paulo fc reebok 2006",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "reebok",
            "tamanho": "G",
            "preco_original": 280.0,
            "preco_atual": 220.0,
            "tag": "barateou",
            "imagem": "https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=500"
        },
        {
            "id": 2,
            "titulo": "camisa atletico mineiro le coq 2021",
            "pais": "Brasil",
            "time_regiao": "Minas Gerais",
            "marca": "le coq sportif",
            "tamanho": "GG",
            "preco_original": 250.0,
            "preco_atual": 200.0,
            "tag": "20% off",
            "imagem": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500"
        },
        {
            "id": 3,
            "titulo": "camisa cuiaba esporte clube 2023",
            "pais": "Brasil",
            "time_regiao": "Mato Grosso",
            "marca": "umbro",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 160.0,
            "tag": "barateou",
            "imagem": "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=500"
        },
        {
            "id": 4,
            "titulo": "camisa operario ms 2022",
            "pais": "Brasil",
            "time_regiao": "Mato Grosso do Sul",
            "marca": "walon",
            "tamanho": "G",
            "preco_original": 180.0,
            "preco_atual": 150.0,
            "tag": "barateou",
            "imagem": "https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=500"
        },
        
        # INGLATERRA
        {
            "id": 5,
            "titulo": "camisa liverpool nike 2022/23",
            "pais": "Inglaterra",
            "time_regiao": "Liverpool",
            "marca": "nike",
            "tamanho": "M",
            "preco_original": 350.0,
            "preco_atual": 280.0,
            "tag": "20% off",
            "imagem": "https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=500"
        },

        # ITÁLIA
        {
            "id": 6,
            "titulo": "camisa juventus turim adidas 2020",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "adidas",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 240.0,
            "tag": "barateou",
            "imagem": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500"
        },
        {
            "id": 7,
            "titulo": "camisa sampdoria genova macron 2021",
            "pais": "Itália",
            "time_regiao": "Gênova - Sampdoria",
            "marca": "macron",
            "tamanho": "M",
            "preco_original": 320.0,
            "preco_atual": 290.0,
            "tag": "9% off",
            "imagem": "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=500"
        },

        # GRÉCIA
        {
            "id": 8,
            "titulo": "camisa panathinaikos atenas kappa",
            "pais": "Grécia",
            "time_regiao": "Atenas - Panathinaikos",
            "marca": "kappa",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 310.0,
            "tag": "barateou",
            "imagem": "https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=500"
        },

        # ESPANHA
        {
            "id": 9,
            "titulo": "camisa ud ibiza eivissa 2022",
            "pais": "Espanha",
            "time_regiao": "Ibiza - Eivissa Ibiza",
            "marca": "puma",
            "tamanho": "M",
            "preco_original": 390.0,
            "preco_atual": 330.0,
            "tag": "barateou",
            "imagem": "https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=500"
        }
    ]
    return pd.DataFrame(data)

df = carregar_dados()

# --- BARRA LATERAL (SIDEBAR) PARA FILTROS ---
st.sidebar.markdown("## 🔍 **Filtros do Acervo**")

# 1. Filtro de País
paises_disponiveis = ["Todos"] + sorted(list(df["pais"].unique()))
pais_selecionado = st.sidebar.selectbox("🌎 **Selecionar País:**", paises_disponiveis)

# 2. Filtro Dinâmico de Time / Região
if pais_selecionado != "Todos":
    df_filtrado_pais = df[df["pais"] == pais_selecionado]
    times_disponiveis = ["Todos"] + sorted(list(df_filtrado_pais["time_regiao"].unique()))
else:
    times_disponiveis = ["Todos"] + sorted(list(df["time_regiao"].unique()))

time_selecionado = st.sidebar.selectbox("⚽ **Clube / Região:**", times_disponiveis)

# 3. Filtro por Tamanho
tamanhos_disponiveis = ["Todos"] + sorted(list(df["tamanho"].unique()))
tamanho_selecionado = st.sidebar.selectbox("📏 **Tamanho:**", tamanhos_disponiveis)


# --- CABEÇALHO DA PÁGINA ---
col_logo, col_search = st.columns([2, 3])

with col_logo:
    st.markdown("### ⚽ **Camisas de Futebol Amauri**")

with col_search:
    busca = st.text_input("", placeholder="🔍 busque por nome da camisa, marca, país ou time...", label_visibility="collapsed")

st.divider()

# --- LÓGICA DE FILTRAGEM DOS DADOS ---
df_exibicao = df.copy()

if busca:
    df_exibicao = df_exibicao[
        df_exibicao["titulo"].str.contains(busca, case=False) | 
        df_exibicao["marca"].str.contains(busca, case=False) |
        df_exibicao["pais"].str.contains(busca, case=False) |
        df_exibicao["time_regiao"].str.contains(busca, case=False)
    ]

if pais_selecionado != "Todos":
    df_exibicao = df_exibicao[df_exibicao["pais"] == pais_selecionado]

if time_selecionado != "Todos":
    df_exibicao = df_exibicao[df_exibicao["time_regiao"] == time_selecionado]

if tamanho_selecionado != "Todos":
    df_exibicao = df_exibicao[df_exibicao["tamanho"] == tamanho_selecionado]

# --- EXIBIÇÃO DOS CARDS ---
st.markdown(f"##### Exibindo {len(df_exibicao)} camisa(s)")
st.write("")

num_colunas = 4
cols = st.columns(num_colunas)

if df_exibicao.empty:
    st.info("Nenhuma camisa encontrada com os filtros selecionados.")
else:
    for idx, row in df_exibicao.reset_index(drop=True).iterrows():
        col = cols[idx % num_colunas]
        
        with col:
            # Imagem do manto
            st.image(row["imagem"], use_container_width=True)
            
            # Tags
            if row["tag"] == "barateou":
                st.markdown(f'<span class="tag-barateou">⚡ {row["tag"]}</span>', unsafe_allow_html=True)
            elif "off" in str(row["tag"]):
                st.markdown(f'<span class="tag-desconto">🏷️ {row["tag"]}</span>', unsafe_allow_html=True)
            
            # Preço
            if row["preco_original"] > 0:
                st.markdown(f'''
                    <div>
                        <span class="preco-atual">R$ {int(row["preco_atual"])}</span>
                        <span class="preco-original">R$ {int(row["preco_original"])}</span>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="preco-atual">R$ {int(row["preco_atual"])}</div>', unsafe_allow_html=True)
                
            # Título e Informações da camisa
            st.markdown(f'<div class="titulo-camisa">{row["titulo"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="subtitulo-camisa">{row["time_regiao"]} ({row["pais"]}) • tam {row["tamanho"]}</div>', unsafe_allow_html=True)
            
            # Lógica do Botão Roxo enviando direto para o WhatsApp +55 11 94276-2908
            msg_wa = f"Olá Amauri! Tenho interesse na camisa '{row['titulo']}' ({row['time_regiao']}) tamanho {row['tamanho']} por R$ {int(row['preco_atual'])}."
            link_wa = f"https://wa.me/{WHATSAPP_NUMERO}?text={msg_wa.replace(' ', '%20')}"
            
            st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-comprar">quero essa</a>', unsafe_allow_html=True)
            st.write("")
