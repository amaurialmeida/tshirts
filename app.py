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
        # 1. OPERÁRIO MATO GROSSO DO SUL / MS #9
        {
            "id": 1,
            "titulo": "Camisa Operário Mato Grosso do Sul / MS Home #9, Champs",
            "pais": "Brasil",
            "time_regiao": "Mato Grosso do Sul - Operário MS",
            "marca": "Champs",
            "tamanho": "G",
            "preco_original": 160.0,
            "preco_atual": 60.0,
            "tag": "barateou",
            "link_br": "https://www.sofutebolbrasil.com/produto/569/camisa-oficial-operario-ms",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/operario-frente.jpeg",
                f"{RAW_BASE}/operario-verso.jpeg"
            ]
        },
        # 2. JUVENTUS DA MOOCA - ANIVERSÁRIO 459 ANOS
        {
            "id": 2,
            "titulo": "Camisa Juventus da Mooca Azul Aniversário 459 Anos #9, Superbolla",
            "pais": "Brasil",
            "time_regiao": "São Paulo - Mooca",
            "marca": "Superbolla",
            "tamanho": "G",
            "preco_original": 270.0,
            "preco_atual": 120.0,
            "tag": "barateou",
            "link_br": "https://www.mercadolivre.com.br/camisa-juventus-da-mooca-especial-2015-azul/up/MLBU1726959953?pdp_filters=item_id%3AMLB3312171725#origin=share&sid=share&wid=MLB3312171725&action=copy",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/juve-azul-frente.jpeg",
                f"{RAW_BASE}/juve-azul-verso.jpeg"
            ]
        },
        # 3. JUVENTUS 2007/2008 - NEW HOLLAND FIAT GROUP
        {
            "id": 3,
            "titulo": "Camisa Juventus 2007/2008, Nike, New Holland Fiat Group, Scudetto",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "Nike",
            "tamanho": "M",
            "preco_original": 220.0,
            "preco_atual": 150.0,
            "tag": "barateou",
            "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035#polycard_client=search-web-mobile&be_origin=backend&overlay_label=not_apply&search_layout=stack&position=2&type=product&tracking_id=7b617228-c264-44e0-8502-4d3938d259a5&wid=MLB4104645169&sid=search",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/juve-frente.jpeg",
                f"{RAW_BASE}/juve-verso.jpeg"
            ]
        },
        # 4. JUVENTUS ROSA JEEP 2015/2016
        {
            "id": 4,
            "titulo": "Camisa Juventus 2015/2016 Rosa Jeep, Adidas Climacool",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "Adidas",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 350.0,
            "tag": "barateou",
            "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035#polycard_client=search-web-mobile&be_origin=backend&overlay_label=not_apply&search_layout=stack&position=2&type=product&tracking_id=7b617228-c264-44e0-8502-4d3938d259a5&wid=MLB4104645169&sid=search",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/juve-rosa-frente.jpeg",
                f"{RAW_BASE}/juve-rosa-verso.jpeg",
                f"{RAW_BASE}/juve-rosa-detalhes.jpeg"
            ]
        },
        # 5. JAQUETA JUVENTUS 2009/2010 TREINO
        {
            "id": 5,
            "titulo": "Jaqueta Juventus 2009/2010 Treino, Nike",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "Nike",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 299.0,
            "tag": "raridade",
            "link_br": None,
            "link_int": "https://www.ebay.com/itm/168192283231",
            "fotos": [
                f"{RAW_BASE}/blusajuve-frente.jpeg",
                f"{RAW_BASE}/blusajuve-verso.jpeg",
                f"{RAW_BASE}/blusajuve-detalhes.jpeg"
            ]
        },
        # 6. SÃO PAULO REEBOK 2007 - ADRIANO IMPERADOR #10
        {
            "id": 6,
            "titulo": "Camisa São Paulo, Reebok 2007, Adriano Imperador #10, LG Fast, Patch Campeão",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "Reebok",
            "tamanho": "G",
            "preco_original": 250.0,
            "preco_atual": 199.0,
            "tag": "barateou",
            "link_br": "https://memoriasdoesporteoficial.com.br/produto/camisa-sao-paulo-reebok-2007-tricolor/",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/spfc2-frente.jpeg",
                f"{RAW_BASE}/spfc2-verso.jpeg",
                f"{RAW_BASE}/spfc2-detalhes.jpeg"
            ]
        },
        # 7. SÃO PAULO 1997 - DENILSON #11
        {
            "id": 7,
            "titulo": "Camisa São Paulo, Adidas 1997, Denilson #11, Data Control",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "Adidas",
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
        # 8. BLUSA SÃO PAULO 1993 - DEL-LINI TRICOT
        {
            "id": 8,
            "titulo": "Blusa Agasalho São Paulo, Del-Lini Tricot 1993, Relíquia Histórica",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "Del-Lini Tricot",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 600.0,
            "tag": "relíquia",
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/blusasp-frente.jpeg",
                f"{RAW_BASE}/blusasp-verso.jpeg"
            ]
        },
        # 9. LIVERPOOL 2006/2007 - TEAMGEIST
        {
            "id": 9,
            "titulo": "Camisa Liverpool 2006/2007, Adidas Teamgeist Original de Época",
            "pais": "Inglaterra",
            "time_regiao": "Liverpool",
            "marca": "Adidas",
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
        # 10. SAMPDORIA ERG
        {
            "id": 10,
            "titulo": "Camisa Sampdoria ERG Itália Azul, Asics",
            "pais": "Itália",
            "time_regiao": "Sampdoria",
            "marca": "Asics",
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
        # 11. PANATHINAIKOS COSMOTE 2010/2011
        {
            "id": 11,
            "titulo": "Camisa Panathinaikos 2010/2011 Home Cosmote, Adidas",
            "pais": "Grécia",
            "time_regiao": "Atenas",
            "marca": "Adidas",
            "tamanho": "M",
            "preco_original": 280.0,
            "preco_atual": 260.0,
            "tag": "importada",
            "link_br": "https://www.enjoei.com.br/p/camisa-panathinaikos-2010-11-home-original-143625516",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/panathinaikos-frente.jpeg",
                f"{RAW_BASE}/panathinaikos-verso.jpeg",
                f"{RAW_BASE}/panathinaikos-detalhes.jpeg",
                f"{RAW_BASE}/panathinaikos-detalhes2.jpeg"
            ]
        },
        # 12. KAISERSLAUTERN / KAISER
        {
            "id": 12,
            "titulo": "Camisa Kaiserslautern Mobil Gel Alemanha, Nike",
            "pais": "Alemanha",
            "time_regiao": "Kaiserslautern",
            "marca": "Nike",
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
        # 13. ITÁLIA COPA 2014 - PIRLO #21
        {
            "id": 13,
            "titulo": "Camisa Itália Copa do Mundo FIFA 2014 Home #21, Pirlo, Puma",
            "pais": "Itália",
            "time_regiao": "Seleção Italiana",
            "marca": "Puma",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 300.0,
            "tag": "barateou",
            "link_br": "https://www.futclassics.com.br/product-page/italia-2014-home-m-5-6",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/italia-frente.jpeg",
                f"{RAW_BASE}/italia-verso.jpeg"
            ]
        },
        # 14. ITÁLIA CAMPIONE DEL MONDO
        {
            "id": 14,
            "titulo": "Camisa Itália Campione Del Mondo Comemorativa, Puma",
            "pais": "Itália",
            "time_regiao": "Seleção Italiana",
            "marca": "Puma",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 240.0,
            "tag": "especial",
            "link_br": None,
            "link_int": "https://www.ebay.com/itm/226370114363",
            "fotos": [
                f"{RAW_BASE}/italiacampione-frente.jpeg",
                f"{RAW_BASE}/italiacampione-verso.jpeg",
                f"{RAW_BASE}/italiacampione-detalhes.jpeg"
            ]
        },
        # 15. INGLATERRA 2007 HOME
        {
            "id": 15,
            "titulo": "Camisa Seleção Inglaterra 2007 Home, Umbro",
            "pais": "Inglaterra",
            "time_regiao": "Seleção Inglesa",
            "marca": "Umbro",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 280.0,
            "tag": "barateou",
            "link_br": "https://www.futclassics.com.br/product-page/inglaterra-2007-home-11",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/inglaterra-frente.jpeg",
                f"{RAW_BASE}/inglaterra-detalhes.jpeg"
            ]
        },
        # 16. IBIZA EIVISSA 2009
        {
            "id": 16,
            "titulo": "Camisa Ibiza Eivissa 2009 Camisa 1 Vermelha, Champs",
            "pais": "Espanha",
            "time_regiao": "Ibiza",
            "marca": "Champs",
            "tamanho": "M",
            "preco_original": 180.0,
            "preco_atual": 150.0,
            "tag": "importada",
            "link_br": "https://brechodofutebol.com/products/ibiza-eivissa-2009-segunda-camisa-tam-p?srsltid=AfmBOooaZ5LOym7C_3sq2WOdXIBHKsP21kuJ4_aKrlHqjoTehlDttDkw",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/ibiza-frente.jpeg",
                f"{RAW_BASE}/ibiza-verso.jpeg",
                f"{RAW_BASE}/ibiza-detalhes1.jpeg",
                f"{RAW_BASE}/ibiza-detalhes21.jpeg"
            ]
        }
    ]
    return pd.DataFrame(data)


# --- INICIALIZAÇÃO E FILTROS ---
df = carregar_dados()

st.title("⚽ Camisas de Futebol Amauri")

busca = st.text_input("🔍 Busca", placeholder="Busque por nome da camisa, marca, país ou time", label_visibility="collapsed")

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
            st.markdown(f'<span class="badge-barateou">⚡ {camisa["tag"].upper()}</span>', unsafe_allow_html=True)
            
        # Preços
        preco_fmt = f"R$ {camisa['preco_atual']:.2f}".replace('.', ',')
        if camisa['preco_original'] > camisa['preco_atual']:
            preco_orig_fmt = f"R$ {camisa['preco_original']:.2f}".replace('.', ',')
            st.markdown(f'<div style="margin-top: 10px;"><span class="price-tag">{preco_fmt}</span><span class="old-price">{preco_orig_fmt}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="margin-top: 10px;"><span class="price-tag">{preco_fmt}</span></div>', unsafe_allow_html=True)
            
        # Título e Subtítulo
        st.markdown(f'<div class="shirt-title">{camisa["titulo"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="shirt-sub">{camisa["time_regiao"]} ({camisa["pais"]}) • Tam {camisa["tamanho"]}</div>', unsafe_allow_html=True)
        
        # 1. Botão Principal "Quero Essa"
        msg_whatsapp = urllib.parse.quote(f"Olá Amauri, tenho interesse na {camisa['titulo']} (R$ {camisa['preco_atual']:.2f})!")
        link_whatsapp = f"https://wa.me/{WHATSAPP_NUMERO}?text={msg_whatsapp}"
        st.link_button("QUERO ESSA", link_whatsapp, use_container_width=True, type="primary")
        
        # 2. Botões Lado a Lado de Comparação de Preço
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
