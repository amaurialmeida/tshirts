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


# --- BASE DE DADOS COMPLETA DO ACERVO ---
@st.cache_data
def carregar_dados():
    RAW_BASE = "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/verso"
    
    data = [
        # 1. SÃO PAULO 1997 - DENILSON #11
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
            "link_br": "https://pe.olx.com.br/grande-recife/esportes-e-lazer/roupas-esportivas/camisa-sao-paulo-adidas-1997-datacontrol-1508643853?utm_medium=shared_link&utm_source=direct",
            "link_int": None,
            "fotos": [
                "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/frente%201.jpeg",
                f"{RAW_BASE}/detalhes/verso1.jpeg",
                f"{RAW_BASE}/detalhe1.jpeg"
            ]
        },
        # 2. LIVERPOOL 2006/2007 - TEAMGEIST
        {
            "id": 2,
            "titulo": "camisa liverpool 2006/2007 adidas teamgeist original epoca",
            "pais": "Inglaterra",
            "time_regiao": "Liverpool",
            "marca": "adidas",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 350.0,
            "tag": "raridade",
            "link_br": "https://www.mercadolivre.com.br/camisa-liverpool-2005-2006-adidas-teamgeist-original-epoca/up/MLBU3358810718",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/liverpool-frente.jpeg",
                f"{RAW_BASE}/liverpool-verso.jpeg",
                f"{RAW_BASE}/liverpool-detalhes21.jpeg"
            ]
        },
        # 3. BLUSA JUVENTUS
        {
            "id": 3,
            "titulo": "blusa agasalho juventus adidas",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "adidas",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 280.0,
            "tag": "raridade",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/blusajuve-frente.jpeg",
                f"{RAW_BASE}/blusajuve-verso.jpeg",
                f"{RAW_BASE}/blusajuve-detalhes.jpeg"
            ]
        },
        # 4. BLUSA SÃO PAULO
        {
            "id": 4,
            "titulo": "blusa agasalho sao paulo tam #10",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "penalty",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 300.0,
            "tag": "raridade",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/blusasp-frente.jpeg",
                f"{RAW_BASE}/blusasp-verso.jpeg"
            ]
        },
        # 5. GALO / ATLÉTICO MINEIRO
        {
            "id": 5,
            "titulo": "camisa regata atletico mineiro galo",
            "pais": "Brasil",
            "time_regiao": "Minas Gerais - Galo",
            "marca": "outra",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 150.0,
            "tag": "barateou",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/galo-frente.jpeg",
                f"{RAW_BASE}/galo-verso.jpeg",
                f"{RAW_BASE}/galo-detalhes.jpeg"
            ]
        },
        # 6. IBIZA
        {
            "id": 6,
            "titulo": "camisa ibiza espanha vermelha",
            "pais": "Espanha",
            "time_regiao": "Ibiza",
            "marca": "outra",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 180.0,
            "tag": "importada",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/ibiza-frente.jpeg",
                f"{RAW_BASE}/ibiza-verso.jpeg",
                f"{RAW_BASE}/ibiza-detalhes1.jpeg",
                f"{RAW_BASE}/ibiza-detalhes21.jpeg"
            ]
        },
        # 7. INGLATERRA
        {
            "id": 7,
            "titulo": "camisa selecao inglaterra umbro",
            "pais": "Inglaterra",
            "time_regiao": "Seleção Inglesa",
            "marca": "umbro",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 200.0,
            "tag": "barateou",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/inglaterra-frente.jpeg",
                f"{RAW_BASE}/inglaterra-detalhes.jpeg"
            ]
        },
        # 8. ITÁLIA CAMPIONE
        {
            "id": 8,
            "titulo": "camisa italia campione comemorativa",
            "pais": "Itália",
            "time_regiao": "Seleção Italiana",
            "marca": "puma",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 190.0,
            "tag": "especial",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/italiacampione-frente.jpeg",
                f"{RAW_BASE}/italiacampione-verso.jpeg",
                f"{RAW_BASE}/italiacampione-detalhes.jpeg"
            ]
        },
        # 9. ITÁLIA PIRLO #21
        {
            "id": 9,
            "titulo": "camisa italia pirlo #21 puma azul",
            "pais": "Itália",
            "time_regiao": "Seleção Italiana",
            "marca": "puma",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 240.0,
            "tag": "barateou",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/italia-frente.jpeg",
                f"{RAW_BASE}/italia-verso.jpeg"
            ]
        },
        # 10. JUVENTUS AZUL SUPERGA #9
        {
            "id": 10,
            "titulo": "camisa juventus azul superga #9 retro",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "kappa",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 270.0,
            "tag": "raridade",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/juve-azul-frente.jpeg",
                f"{RAW_BASE}/juve-azul-verso.jpeg"
            ]
        },
        # 11. JUVENTUS TRADICIONAL JEEP
        {
            "id": 11,
            "titulo": "camisa juventus listrada jeep adidas",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "adidas",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 220.0,
            "tag": "barateou",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/juve-frente.jpeg",
                f"{RAW_BASE}/juve-verso.jpeg"
            ]
        },
        # 12. JUVENTUS ROSA JEEP
        {
            "id": 12,
            "titulo": "camisa juventus rosa jeep adidas",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "adidas",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 250.0,
            "tag": "barateou",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/juve-rosa-frente.jpeg",
                f"{RAW_BASE}/juve-rosa-verso.jpeg",
                f"{RAW_BASE}/juve-rosa-detalhes.jpeg"
            ]
        },
        # 13. KAISERSLAUTERN / KAISER
        {
            "id": 13,
            "titulo": "camisa kaiserslautern mobil gel alemanha",
            "pais": "Alemanha",
            "time_regiao": "Kaiserslautern",
            "marca": "nike",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 260.0,
            "tag": "raridade",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/kaiser-frente.jpeg",
                f"{RAW_BASE}/kaiser-verso.jpeg",
                f"{RAW_BASE}/kaiser-detalhes.jpeg"
            ]
        },
        # 14. OPERÁRIO #9
        {
            "id": 14,
            "titulo": "camisa operario #9 listrada preto e branco",
            "pais": "Brasil",
            "time_regiao": "Paraná",
            "marca": "outra",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 160.0,
            "tag": "barateou",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/operario-frente.jpeg",
                f"{RAW_BASE}/operario-verso.jpeg"
            ]
        },
        # 15. PANATHINAIKOS COSMOTE
        {
            "id": 15,
            "titulo": "camisa panathinaikos cosmote grecia verde",
            "pais": "Grécia",
            "time_regiao": "Atenas",
            "marca": "adidas",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 280.0,
            "tag": "importada",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/panathinaikos-frente.jpeg",
                f"{RAW_BASE}/panathinaikos-verso.jpeg",
                f"{RAW_BASE}/panathinaikos-detalhes.jpeg",
                f"{RAW_BASE}/panathinaikos-detalhes2.jpeg"
            ]
        },
        # 16. SAMPDORIA ERG
        {
            "id": 16,
            "titulo": "camisa sampdoria erg italia azul",
            "pais": "Itália",
            "time_regiao": "Sampdoria",
            "marca": "asics",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 320.0,
            "tag": "raridade",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/samp-frente.jpeg",
                f"{RAW_BASE}/samp-verso.jpeg",
                f"{RAW_BASE}/samp-detalhes.jpeg"
            ]
        },
        # 17. SÃO PAULO LG #10 TRICOLOR
        {
            "id": 17,
            "titulo": "camisa sao paulo lg #10 tricolor reebok",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "reebok",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 290.0,
            "tag": "barateou",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/spfc2-frente.jpeg",
                f"{RAW_BASE}/spfc2-verso.jpeg",
                f"{RAW_BASE}/spfc2-detalhes.jpeg"
            ]
        }
    ]
    return pd.DataFrame(data)


# --- INICIALIZAÇÃO E FILTROS ---
df = carregar_dados()

st.title("⚽ Camisas de Futebol Amauri")

busca = st.text_input("🔍 busca", placeholder="busque por nome da camisa, marca, país ou time", label_visibility="collapsed")

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

# --- EXIBIÇÃO DA VITRINE DE CAMISAS ---
for _, camisa in df_filtrado.iterrows():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        fotos = camisa["fotos"]
        key_foto = f"foto_idx_{camisa['id']}"
        
        if key_foto not in st.session_state:
            st.session_state[key_foto] = 0
            
        foto_atual_idx = st.session_state[key_foto]
        
        # Exibe imagem ativa
        st.image(fotos[foto_atual_idx], use_column_width=True)
        
        # Carrossel de Fotos
        if len(fotos) > 1:
            btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
            
            with btn_col1:
                st.caption("📷")
            with btn_col2:
                st.caption(f"{foto_atual_idx + 1}/{len(fotos)}")
            with btn_col3:
                if st.button("▶️", key=f"next_{camisa['id']}"):
                    st.session_state[key_foto] = (foto_atual_idx + 1) % len(fotos)
                    st.rerun()

    with col2:
        # Tag de Destaque
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
        
        # 1. Botão Principal "Quero Essa"
        msg_whatsapp = urllib.parse.quote(f"Olá Amauri, tenho interesse na {camisa['titulo']} (R$ {camisa['preco_atual']:.2f})!")
        link_whatsapp = f"https://wa.me/{WHATSAPP_NUMERO}?text={msg_whatsapp}"
        st.link_button("quero essa", link_whatsapp, use_container_width=True, type="primary")
        
        # 2. Botões Lado a Lado de Comparação de Preço (com checagem segura de valores nulos/None)
        col_comp1, col_comp2 = st.columns(2)
        
        link_br = camisa.get("link_br")
        link_int = camisa.get("link_int")
        
        with col_comp1:
            if link_br and pd.notna(link_br):
                st.link_button("💲 COMPARE 🇧🇷", link_br, use_container_width=True)
            else:
                st.button("💲 COMPARE 🇧🇷", disabled=True, use_container_width=True, key=f"dis_br_{camisa['id']}")
                
        with col_comp2:
            if link_int and pd.notna(link_int):
                st.link_button("💲 COMPARE 🌐", link_int, use_container_width=True)
            else:
                st.button("💲 COMPARE 🌐", disabled=True, use_container_width=True, key=f"dis_int_{camisa['id']}")

    st.divider()
