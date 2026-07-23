import streamlit as st
import pandas as pd

# Configuração da página em modo wide
st.set_page_config(page_title="Camisas de Futebol Amauri ⚽", layout="wide", page_icon="⚽")

# --- NÚMERO DO WHATSAPP ---
WHATSAPP_NUMERO = "5511942762908"

# --- CSS CUSTOMIZADO (MANTENDO A ESTRUTURA ANTERIOR) ---
st.markdown("""
    <style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Input de busca estilo Enjoei */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 12px 20px !important;
        font-size: 0.95rem !important;
        background-color: #f8fafc !important;
    }

    /* Container do Card do Produto */
    .product-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 20px;
        border: 1px solid #f1f5f9;
    }

    /* Preço Roxo e Riscado */
    .preco-atual {
        font-size: 1.2rem;
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

    /* Tag Amarela Barateou / Tag Desconto */
    .tag-barateou {
        background-color: #facc15;
        color: #0f172a;
        font-weight: 700;
        font-size: 0.72rem;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: lowercase;
        display: inline-block;
        margin-top: 6px;
        margin-bottom: 6px;
    }
    .tag-desconto {
        background-color: #e9d5ff;
        color: #6b21a8;
        font-weight: 700;
        font-size: 0.72rem;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-top: 6px;
        margin-bottom: 6px;
    }

    /* Título e detalhes */
    .titulo-camisa {
        font-size: 0.92rem;
        color: #334155;
        font-weight: 600;
        margin-top: 4px;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .subtitulo-camisa {
        font-size: 0.82rem;
        color: #64748b;
        margin-bottom: 12px;
    }

    /* Botão Roxo WhatsApp */
    .btn-comprar {
        display: block;
        width: 100%;
        background-color: #c026d3;
        color: white !important;
        text-align: center;
        padding: 10px 0px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        text-decoration: none !important;
        transition: background-color 0.2s;
    }
    .btn-comprar:hover {
        background-color: #a21caf;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS COM LISTA DE FOTOS ---
@st.cache_data
def carregar_dados():
    BASE_URL = "https://raw.githubusercontent.com/amaurialmeida/tshirts/main"
    
    data = [
        # SÃO PAULO 1997 - DENILSON #11 (EXEMPLO DO SEU REPOSITÓRIO)
        {
            "id": 1,
            "titulo": "camisa sao paulo adidas 1997 denilson #11",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "adidas",
            "tamanho": "G",
            "preco_original": 500.0,
            "preco_atual": 450.0,
            "tag": "barateou",
            "fotos": [
                f"{BASE_URL}/spfc_1997_frente.jpg",
                f"{BASE_URL}/spfc_1997_verso.jpg",
                f"{BASE_URL}/spfc_1997_detalhes.jpg"
            ]
        },
        # CUIABÁ
        {
            "id": 2,
            "titulo": "camisa cuiaba esporte clube 2023",
            "pais": "Brasil",
            "time_regiao": "Mato Grosso",
            "marca": "umbro",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 160.0,
            "tag": "barateou",
            "fotos": [
                "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=500",
                "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500",
                "https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=500"
            ]
        },
        # LIVERPOOL
        {
            "id": 3,
            "titulo": "camisa liverpool nike 2022/23",
            "pais": "Inglaterra",
            "time_regiao": "Liverpool",
            "marca": "nike",
            "tamanho": "M",
            "preco_original": 350.0,
            "preco_atual": 280.0,
            "tag": "20% off",
            "fotos": [
                "https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=500",
                "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500",
                "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=500"
            ]
        },
        # JUVENTUS
        {
            "id": 4,
            "titulo": "camisa juventus turim adidas 2020",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "adidas",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 240.0,
            "tag": "barateou",
            "fotos": [
                "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500",
                "https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=500",
                "https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=500"
            ]
        }
    ]
    return pd.DataFrame(data)

df = carregar_dados()

# --- BARRA LATERAL (SIDEBAR FILTROS) ---
st.sidebar.markdown("## 🔍 **Filtros do Acervo**")

paises_disponiveis = ["Todos"] + sorted(list(df["pais"].unique()))
pais_selecionado = st.sidebar.selectbox("🌎 **Selecionar País:**", paises_disponiveis)

if pais_selecionado != "Todos":
    df_filtrado_pais = df[df["pais"] == pais_selecionado]
    times_disponiveis = ["Todos"] + sorted(list(df_filtrado_pais["time_regiao"].unique()))
else:
    times_disponiveis = ["Todos"] + sorted(list(df["time_regiao"].unique()))

time_selecionado = st.sidebar.selectbox("⚽ **Clube / Região:**", times_disponiveis)

tamanhos_disponiveis = ["Todos"] + sorted(list(df["tamanho"].unique()))
tamanho_selecionado = st.sidebar.selectbox("📏 **Tamanho:**", tamanhos_disponiveis)

# --- CABEÇALHO ---
col_logo, col_search = st.columns([2, 3])

with col_logo:
    st.markdown("### ⚽ **Camisas de Futebol Amauri**")

with col_search:
    busca = st.text_input("", placeholder="🔍 busque por nome da camisa, marca, país ou time...", label_visibility="collapsed")

st.divider()

# --- LÓGICA DE FILTRAGEM ---
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

# --- EXIBIÇÃO EM GRADE ---
num_colunas = 4
cols = st.columns(num_colunas)

if df_exibicao.empty:
    st.info("Nenhuma camisa encontrada com os filtros selecionados.")
else:
    for idx, row in df_exibicao.reset_index(drop=True).iterrows():
        col = cols[idx % num_colunas]
        
        with col:
            # --- LÓGICA DO BOTÃO ▶️ PARA TROCAR A FOTO (Frente -> Verso -> Detalhes) ---
            key_foto = f"foto_index_{row['id']}"
            if key_foto not in st.session_state:
                st.session_state[key_foto] = 0
            
            # Recupera a foto atual da lista
            fotos_list = row["fotos"]
            idx_foto = st.session_state[key_foto] % len(fotos_list)
            
            # 1. Foto principal em destaque
            st.image(fotos_list[idx_foto], use_container_width=True)
            
            # 2. Botão ▶️ posicionado à direita logo abaixo da foto
            c_label, c_btn = st.columns([3, 1])
            with c_label:
                # Indicador de qual foto está sendo vista (Ex: 1/3, 2/3, 3/3)
                st.caption(f"📷 Foto {idx_foto + 1} de {len(fotos_list)}")
            with c_btn:
                # Botão ▶️ que avança para a próxima foto ao ser clicado
                if st.button("▶️", key=f"btn_next_{row['id']}"):
                    st.session_state[key_foto] = (st.session_state[key_foto] + 1) % len(fotos_list)
                    st.rerun()

            # 3. Tag (barateou / desconto)
            if row["tag"] == "barateou":
                st.markdown(f'<span class="tag-barateou">⚡ {row["tag"]}</span>', unsafe_allow_html=True)
            elif "off" in str(row["tag"]):
                st.markdown(f'<span class="tag-desconto">🏷️ {row["tag"]}</span>', unsafe_allow_html=True)
            
            # 4. Bloco de Preços
            if row["preco_original"] > 0:
                st.markdown(f'''
                    <div>
                        <span class="preco-atual">R$ {int(row["preco_atual"])}</span>
                        <span class="preco-original">R$ {int(row["preco_original"])}</span>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="preco-atual">R$ {int(row["preco_atual"])}</div>', unsafe_allow_html=True)
                
            # 5. Título e Informações da camisa
            st.markdown(f'<div class="titulo-camisa">{row["titulo"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="subtitulo-camisa">{row["time_regiao"]} ({row["pais"]}) • tam {row["tamanho"]}</div>', unsafe_allow_html=True)
            
            # 6. Botão Roxo "quero essa"
            msg_wa = f"Olá Amauri! Tenho interesse na camisa '{row['titulo']}' ({row['time_regiao']}) tamanho {row['tamanho']} por R$ {int(row['preco_atual'])}."
            link_wa = f"https://wa.me/{WHATSAPP_NUMERO}?text={msg_wa.replace(' ', '%20')}"
            
            st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-comprar">quero essa</a>', unsafe_allow_html=True)
            st.write("")
