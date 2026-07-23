import streamlit as st
import pandas as pd
import urllib.parse

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Camisas de Futebol Amauri ⚽",
    layout="wide",
    page_icon="⚽"
)

# --- NÚMERO DO WHATSAPP DO AMAURI ---
WHATSAPP_NUMERO = "5511942762908"

# --- ESTILIZAÇÃO CSS CUSTOMIZADA ---
st.markdown("""
    <style>
    /* Estilização dos badges de preço e tag */
    .price-tag {
        font-size: 1.4rem;
        font-weight: bold;
        color: #2e7d32;
    }
    .old-price {
        text-decoration: line-through;
        color: #757575;
        font-size: 0.9rem;
        margin-left: 8px;
    }
    .badge-barateou {
        background-color: #ffeb3b;
        color: #000;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .shirt-title {
        font-weight: 600;
        font-size: 1.1rem;
        margin-top: 5px;
        text-transform: lowercase;
    }
    .shirt-sub {
        color: #616161;
        font-size: 0.85rem;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# --- DADOS DAS CAMISAS ---
@st.cache_data
def carregar_dados():
    data = [
        {
            "id": 1,
            "titulo": "camisa sao paulo adidas 1997 denilson #11 data control",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "adidas",
            "tamanho": "G",
            "preco_original": 500.0,
            "preco_atual": 450.0,
            "tag": "barateou",
            "link_comparacao": "https://pe.olx.com.br/grande-recife/esportes-e-lazer/roupas-esportivas/camisa-sao-paulo-adidas-1997-datacontrol-1508643853?utm_medium=shared_link&utm_source=direct",
            "fotos": [
                "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/frente%201.jpeg",
                "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/verso/detalhes/verso1.jpeg",
                "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/verso/detalhe1.jpeg"
            ]
        },
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
            "link_comparacao": None,
            "fotos": [
                "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=500",
                "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500"
            ]
        }
    ]
    return pd.DataFrame(data)


# --- INICIALIZAÇÃO E ESTADO ---
df = carregar_dados()

# Título Principal
st.title("⚽ Camisas de Futebol Amauri")

# Barra de busca
busca = st.text_input("🔍 busca", placeholder="busque por nome da camisa, marca, país ou time", label_visibility="collapsed")

# Filtragem de busca
if busca:
    termo = busca.lower()
    df_filtrado = df[
        df['titulo'].str.lower().str.contains(termo) |
        df['marca'].str.lower().str.contains(termo) |
        df['pais'].str.lower().str.contains(termo) |
        df['time_regiao'].str.lower().str.contains(termo)
    ]
else:
    df_filtrado = df

st.divider()

# --- EXIBIÇÃO DOS CARDS DE CAMISAS ---
for _, camisa in df_filtrado.iterrows():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Carrossel / Navegador de Fotos
        fotos = camisa["fotos"]
        key_foto = f"foto_idx_{camisa['id']}"
        
        if key_foto not in st.session_state:
            st.session_state[key_foto] = 0
            
        foto_atual_idx = st.session_state[key_foto]
        
        # Exibe a foto atual
        st.image(fotos[foto_atual_idx], use_column_width=True)
        
        # Botões de controle das fotos se houver mais de uma
        if len(fotos) > 1:
            btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
            
            with btn_col1:
                if st.button("📷", key=f"foto_icon_{camisa['id']}"):
                    pass
            with btn_col2:
                st.caption(f"{foto_atual_idx + 1}/{len(fotos)}")
            with btn_col3:
                if st.button("▶️", key=f"next_{camisa['id']}"):
                    st.session_state[key_foto] = (foto_atual_idx + 1) % len(fotos)
                    st.rerun()

    with col2:
        # Tag de Desconto / Destaque
        if camisa["tag"]:
            st.markdown(f'<span class="badge-barateou">⚡ {camisa["tag"]}</span>', unsafe_allow_html=True)
            
        # Preços
        preco_fmt = f"R$ {camisa['preco_atual']:.2f}".replace('.', ',')
        if camisa['preco_original'] > camisa['preco_atual']:
            preco_orig_fmt = f"R$ {camisa['preco_original']:.2f}".replace('.', ',')
            st.markdown(f'<div style="margin-top: 10px;"><span class="price-tag">{preco_fmt}</span><span class="old-price">{preco_orig_fmt}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="margin-top: 10px;"><span class="price-tag">{preco_fmt}</span></div>', unsafe_allow_html=True)
            
        # Título e Subtítulo
        st.markdown(f'<div class="shirt-title">{camisa["titulo"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="shirt-sub">{camisa["time_regiao"]} ({camisa["pais"]}) • tam {camisa["tamanho"]}</div>', unsafe_allow_html=True)
        
        # Botão "Quero Essa" (WhatsApp)
        msg_whatsapp = urllib.parse.quote(f"Olá Amauri, tenho interesse na {camisa['titulo']} (R$ {camisa['preco_atual']:.2f})!")
        link_whatsapp = f"https://wa.me/{WHATSAPP_NUMERO}?text={msg_whatsapp}"
        st.link_button("quero essa", link_whatsapp, use_container_width=True, type="primary")
        
        # Botão "$ COMPARE $" (Link de comparação/OLX)
        if camisa.get("link_comparacao"):
            st.link_button("💲 COMPARE 💲", camisa["link_comparacao"], use_container_width=True)

    st.divider()
