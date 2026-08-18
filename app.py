import streamlit as st
import pandas as pd
import urllib.parse
import io
import requests

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Camisas de Futebol Amauri ⚽",
    layout="wide",
    page_icon="⚽"
)

# --- NÚMERO DO WHATSAPP DO AMAURI ---
WHATSAPP_NUMERO = "5511942762908"

# --- BASE DE DADOS COMPLETA DO ACERVO (17 CAMISAS COM FOTOS CORRETAS DO GITHUB) ---
@st.cache_data
def carregar_dados():
    RAW_BASE = "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/verso"
    
    data = [
        # 1. OPERÁRIO MS #9
        {
            "id": 1,
            "titulo": "Camisa Operário Mato Grosso do Sul / MS Home #9, Champs",
            "pais": "Brasil",
            "time_regiao": "Mato Grosso do Sul - Operário MS",
            "marca": "Champs",
            "tamanho": "M",
            "preco_original": 160.0,
            "preco_atual": 60.0,
            "tag": "barateou",
            "link_br": "https://www.sofutebolbrasil.com/produto/569/camisa-oficial-operario-ms",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/operario-frente.jpg",
                f"{RAW_BASE}/operario-verso.jpg"
            ]
        },
        # 2. JUVENTUS DA MOOCA
        {
            "id": 2,
            "titulo": "Camisa Juventus da Mooca Azul Aniversário 459 Anos #9, Superbolla",
            "pais": "Brasil",
            "time_regiao": "São Paulo - Mooca",
            "marca": "Superbolla",
            "tamanho": "M",
            "preco_original": 270.0,
            "preco_atual": 120.0,
            "tag": "barateou",
            "link_br": "https://www.mercadolivre.com.br/camisa-juventus-da-mooca-especial-2015-azul/up/MLBU1726959953",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/juve-azul-frente.jpg",
                f"{RAW_BASE}/juve-azul-verso.jpg"
            ]
        },
        # 3. JUVENTUS 2007/2008
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
            "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/juve-frente.jpg",
                f"{RAW_BASE}/juve-verso.jpg"
            ]
        },
        # 4. JUVENTUS ROSA 2015/2016
        {
            "id": 4,
            "titulo": "Camisa Juventus 2015/2016 Rosa Jeep, Adidas Climacool",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "Adidas",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 350.0,
            "tag": "raridade",
            "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035",
            "link_int": "https://www.ebay.com/itm/389084099014",
            "fotos": [
                f"{RAW_BASE}/juve-rosa-frente.jpg",
                f"{RAW_BASE}/juve-rosa-verso.jpg",
                f"{RAW_BASE}/juve-rosa-detalhes.jpg"
            ]
        },
        # 5. JAQUETA JUVENTUS 2009/2010
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
                f"{RAW_BASE}/blusajuve-frente.jpg",
                f"{RAW_BASE}/blusajuve-verso.jpg",
                f"{RAW_BASE}/blusajuve-detalhes.jpg"
            ]
        },
        # 6. SÃO PAULO REEBOK 2007
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
            "link_int": "https://www.ebay.com/itm/175121591014",
            "fotos": [
                f"{RAW_BASE}/spfc2-frente.jpg",
                f"{RAW_BASE}/spfc2-verso.jpg",
                f"{RAW_BASE}/spfc2-detalhes.jpg"
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
            "link_br": "https://pe.olx.com.br/grande-recife/esportes-e-lazer/roupas-esportivas/camisa-sao-paulo-adidas-1997-datacontrol-1508643853",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/spfc-1997-frente.jpg",
                f"{RAW_BASE}/spfc-1997-verso.jpg"
            ]
        },
        # 8. BLUSA SÃO PAULO 1993
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
                f"{RAW_BASE}/blusasp-frente.jpg",
                f"{RAW_BASE}/blusasp-verso.jpg"
            ]
        },
        # 9. LIVERPOOL 2006/2007
        {
            "id": 9,
            "titulo": "Camisa Liverpool 2006/2007 Home, Adidas, Carlsberg, Item de Colecionador",
            "pais": "Inglaterra",
            "time_regiao": "Liverpool",
            "marca": "Adidas",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 350.0,
            "tag": "raridade",
            "link_br": "https://www.mercadolivre.com.br/camisa-liverpool-2005-2006-adidas-teamgeist-original-epoca/up/MLBU3358810718",
            "link_int": "https://www.ebay.com/itm/197498583510",
            "fotos": [
                f"{RAW_BASE}/liverpool-frente.jpg",
                f"{RAW_BASE}/liverpool-verso.jpg",
                f"{RAW_BASE}/liverpool-detalhes.jpg"
            ]
        },
        # 10. SAMPDORIA ERG
        {
            "id": 10,
            "titulo": "Camisa Sampdoria ERG Itália Azul, Kappa",
            "pais": "Itália",
            "time_regiao": "Sampdoria",
            "marca": "Kappa",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 320.0,
            "tag": "raridade",
            "link_br": None,
            "link_int": "https://www.ebay.com/itm/267415041067",
            "fotos": [
                f"{RAW_BASE}/samp-frente.jpg",
                f"{RAW_BASE}/samp-verso.jpg",
                f"{RAW_BASE}/samp-detalhes.jpg"
            ]
        },
        # 11. PANATHINAIKOS 2010/2011
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
            "link_int": "https://www.ebay.com/itm/389490870451",
            "fotos": [
                f"{RAW_BASE}/panathinaikos-frente.jpg",
                f"{RAW_BASE}/panathinaikos-verso.jpg",
                f"{RAW_BASE}/panathinaikos-detalhes.jpg"
            ]
        },
        # 12. KAISERSLAUTERN
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
            "link_int": "https://www.ebay.it/itm/286873950722",
            "fotos": [
                f"{RAW_BASE}/kaiser-frente.jpg",
                f"{RAW_BASE}/kaiser-verso.jpg",
                f"{RAW_BASE}/kaiser-detalhes.jpg"
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
            "link_int": "https://www.ebay.com/itm/128011480704",
            "fotos": [
                f"{RAW_BASE}/italia-frente.jpg",
                f"{RAW_BASE}/italia-verso.jpg"
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
                f"{RAW_BASE}/italiacampione-frente.jpg",
                f"{RAW_BASE}/italiacampione-verso.jpg",
                f"{RAW_BASE}/italiacampione-detalhes.jpg"
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
                f"{RAW_BASE}/inglaterra-frente.jpg",
                f"{RAW_BASE}/inglaterra-detalhes.jpg"
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
            "link_br": "https://brechodofutebol.com/products/ibiza-eivissa-2009-segunda-camisa-tam-p",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/ibiza-frente.jpg",
                f"{RAW_BASE}/ibiza-verso.jpg",
                f"{RAW_BASE}/ibiza-detalhes.jpg"
            ]
        },
        # 17. ITÁLIA RUGBY 2007-2009
        {
            "id": 17,
            "titulo": "Camisa Seleção Itália Rugby 2007 - 2009, Kappa",
            "pais": "Itália",
            "time_regiao": "Seleção Italiana",
            "marca": "Kappa",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 150.0,
            "tag": "especial",
            "link_br": "https://www.enjoei.com.br/p/camisa-selecao-italia-rugby-111153794",
            "link_int": "https://www.ebay.co.uk/itm/282395881167",
            "fotos": [
                f"{RAW_BASE}/italiarugby-frente.jpg",
                f"{RAW_BASE}/italiarugby-verso.jpg"
            ]
        }
    ]
    return pd.DataFrame(data)

def get_qr_url(link):
    if not link:
        return None
    encoded = urllib.parse.quote(link)
    return f"https://quickchart.io/qr?text={encoded}&size=150"

def fetch_qr_image(url):
    if not url:
        return None
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            img_data = io.BytesIO(response.content)
            return Image(img_data, width=55, height=55)
    except Exception:
        pass
    return None

def generate_pdf(df_items):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, rightMargin=15, leftMargin=15, topMargin=15, bottomMargin=15
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading2'], fontSize=10, leading=12, fontName="Helvetica-Bold")
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=8, leading=10)
    price_style = ParagraphStyle('PriceStyle', parent=styles['Normal'], fontSize=10, leading=12, textColor=colors.HexColor('#2e7d32'), fontName="Helvetica-Bold")
    
    card_data_list = []
    
    for _, item in df_items.iterrows():
        clean_title = item['titulo'].encode('ascii', 'ignore').decode('ascii').strip()
        if not clean_title:
            clean_title = f"Item #{item['id']}"
            
        qr_br_img = fetch_qr_image(get_qr_url(item['link_br']))
        qr_int_img = fetch_qr_image(get_qr_url(item['link_int']))
        
        br_cell = qr_br_img if qr_br_img else Paragraph("<i>Sem Link BR</i>", text_style)
        int_cell = qr_int_img if qr_int_img else Paragraph("<i>Sem Link INT</i>", text_style)
        
        qr_table = Table(
            [[Paragraph("<b>BR</b>", text_style), Paragraph("<b>INT</b>", text_style)],
             [br_cell, int_cell]],
            colWidths=[110, 110]
        )
        qr_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        
        card_content = [
            Paragraph(f"#{item['id']} {clean_title}", title_style),
            Spacer(1, 3),
            Paragraph(f"Marca: {item['marca']} | Tam: {item['tamanho']}", text_style),
            Spacer(1, 2),
            Paragraph(f"Preço: R$ {item['preco_atual']:.2f}".replace('.', ','), price_style),
            Spacer(1, 4),
            qr_table
        ]
        
        card_box = Table([[card_content]], colWidths=[250])
        card_box.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#666666')),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BACKGROUND', (0,0), (-1,-1), colors.white)
        ]))
        
        card_data_list.append(card_box)

    grid_data = []
    row = []
    for card in card_data_list:
        row.append(card)
        if len(row) == 2:
            grid_data.append(row)
            row = []
    if row:
        row.append("")
        grid_data.append(row)

    main_grid = Table(grid_data, colWidths=[260, 260])
    main_grid.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    
    doc.build([main_grid])
    buffer.seek(0)
    return buffer.getvalue()

# --- INICIALIZAÇÃO DA INTERFACE ---
df = carregar_dados()

st.title("⚽ Camisas de Futebol Amauri")

# Botão para geração do PDF de etiquetas
if st.button("📄 Gerar e Baixar PDF de Etiquetas", type="primary", use_container_width=True):
    with st.spinner("Preparando o PDF com as etiquetas..."):
        try:
            pdf_data = generate_pdf(df)
            st.download_button(
                label="📥 Clique aqui para salvar o PDF das Etiquetas",
                data=pdf_data,
                file_name="etiquetas_camisas.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.success("PDF pronto para baixar!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

st.divider()

# Busca
busca = st.text_input("🔍 Busca", placeholder="Busque por nome da camisa, marca, país ou time")

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

# --- VITRINE EM COLUNAS ---
cols = st.columns(2)

for idx, (_, camisa) in enumerate(df_filtrado.iterrows()):
    col = cols[idx % 2]
    with col:
        with st.container(border=True):
            st.subheader(f"#{camisa['id']} {camisa['titulo']}")
            st.caption(f"**Marca:** {camisa['marca']} | **Tamanho:** {camisa['tamanho']} | **Origem:** {camisa['pais']}")
            
            preco_fmt = f"R$ {camisa['preco_atual']:.2f}".replace('.', ',')
            st.markdown(f"### **Preço:** :green[{preco_fmt}]")
            
            # --- Seção de Fotos ---
            with st.expander("📷 Ver Fotos do Produto"):
                fotos = camisa["fotos"]
                if len(fotos) == 2:
                    t1, t2 = st.tabs(["Frente ▶️", "Verso ▶️"])
                    with t1:
                        st.image(fotos[0], use_container_width=True)
                    with t2:
                        st.image(fotos[1], use_container_width=True)
                elif len(fotos) >= 3:
                    t1, t2, t3 = st.tabs(["Frente ▶️", "Verso ▶️", "Detalhes ▶️"])
                    with t1:
                        st.image(fotos[0], use_container_width=True)
                    with t2:
                        st.image(fotos[1], use_container_width=True)
                    with t3:
                        st.image(fotos[2], use_container_width=True)
                else:
                    st.image(fotos[0], use_container_width=True)

            st.divider()
            
            # --- Links Clicáveis & QR Codes ---
            c_br, c_int = st.columns(2)
            qr_br = get_qr_url(camisa['link_br'])
            qr_int = get_qr_url(camisa['link_int'])
            
            with c_br:
                st.caption("🇧🇷 **LINK 🇧🇷**")
                if camisa['link_br'] and pd.notna(camisa['link_br']):
                    st.markdown(f"[Acessar anúncio BR 🔗]({camisa['link_br']})")
                    if qr_br:
                        st.image(qr_br, width=110)
                else:
                    st.caption("*Sem Link BR*")
                    
            with c_int:
                st.caption("🌎 **LINK 🌎**")
                if camisa['link_int'] and pd.notna(camisa['link_int']):
                    st.markdown(f"[Acessar anúncio INT 🔗]({camisa['link_int']})")
                    if qr_int:
                        st.image(qr_int, width=110)
                else:
                    st.caption("*Sem Link INT*")

            st.divider()
            
            # --- Botão Laranja do WhatsApp ---
            wa_text = urllib.parse.quote(f"Olá Amauri! Tenho interesse na camisa: #{camisa['id']} {camisa['titulo']} ({preco_fmt})")
            wa_link = f"https://wa.me/{WHATSAPP_NUMERO}?text={wa_text}"
            
            st.markdown(
                f"""
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <button style="
                        background-color: #FF6600;
                        color: white;
                        border: none;
                        padding: 12px;
                        border-radius: 6px;
                        font-weight: bold;
                        width: 100%;
                        cursor: pointer;
                        font-size: 15px;
                    ">
                        💬 Me Interessei Por Essa
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
