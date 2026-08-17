import streamlit as st
import urllib.parse
import io
import requests
from PIL import Image as PILImage

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Gerador de Etiquetas", page_icon="🏷️", layout="wide")

# Lista do catálogo de camisas (17 itens)
catalog = [
    {
        "id": 1,
        "titulo": "Operário MS Home #9 🇧🇷",
        "marca": "Champs", "tamanho": "M", "preco": "R$ 60,00",
        "link_br": "https://www.sofutebolbrasil.com/produto/569/camisa-oficial-operario-ms",
        "link_int": None
    },
    {
        "id": 2,
        "titulo": "Juventus da Mooca Azul 459 Anos #9 🇧🇷",
        "marca": "Superbolla", "tamanho": "M", "preco": "R$ 120,00",
        "link_br": "https://www.mercadolivre.com.br/camisa-juventus-da-mooca-especial-2015-azul/up/MLBU1726959953",
        "link_int": None
    },
    {
        "id": 3,
        "titulo": "Juventus 2007/2008 Scudetto 🇮🇹",
        "marca": "Nike", "tamanho": "M", "preco": "R$ 150,00",
        "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035",
        "link_int": None
    },
    {
        "id": 4,
        "titulo": "Juventus 2015/2016 Rosa 🇮🇹",
        "marca": "Adidas Climacool", "tamanho": "G", "preco": "R$ 350,00",
        "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035",
        "link_int": "https://www.ebay.com/itm/389084099014"
    },
    {
        "id": 5,
        "titulo": "Jaqueta Juventus 2009/2010 Treino 🇮🇹",
        "marca": "Nike", "tamanho": "G", "preco": "R$ 299,00",
        "link_br": None,
        "link_int": "https://www.ebay.com/itm/168192283231"
    },
    {
        "id": 6,
        "titulo": "São Paulo 2007 Adriano Imperador #10 🇧🇷",
        "marca": "Reebok", "tamanho": "G", "preco": "R$ 199,00",
        "link_br": "https://memoriasdoesporteoficial.com.br/produto/camisa-sao-paulo-reebok-2007-tricolor/",
        "link_int": "https://www.ebay.com/itm/175121591014"
    },
    {
        "id": 7,
        "titulo": "São Paulo 1997 Denilson #11 🇧🇷",
        "marca": "Adidas", "tamanho": "G", "preco": "R$ 450,00",
        "link_br": "https://pe.olx.com.br/grande-recife/esportes-e-lazer/roupas-esportivas/camisa-sao-paulo-adidas-1997-datacontrol-1508643853",
        "link_int": None
    },
    {
        "id": 8,
        "titulo": "Blusa Agasalho São Paulo 1993 🇧🇷",
        "marca": "Del-Lini Tricot", "tamanho": "G", "preco": "R$ 600,00",
        "link_br": None,
        "link_int": None
    },
    {
        "id": 9,
        "titulo": "Liverpool 2006/2007 Home 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "marca": "Adidas", "tamanho": "G", "preco": "R$ 350,00",
        "link_br": "https://www.mercadolivre.com.br/camisa-liverpool-2005-2006-adidas-teamgeist-original-epoca/up/MLBU3358810718",
        "link_int": "https://www.ebay.com/itm/197498583510"
    },
    {
        "id": 10,
        "titulo": "Sampdoria 2004/2005 ERG Azul 🇮🇹",
        "marca": "Kappa", "tamanho": "G", "preco": "R$ 320,00",
        "link_br": None,
        "link_int": "https://www.ebay.com/itm/267415041067"
    },
    {
        "id": 11,
        "titulo": "Panathinaikos 2010/2011 Home 🇬🇷",
        "marca": "Adidas", "tamanho": "M", "preco": "R$ 260,00",
        "link_br": "https://www.enjoei.com.br/p/camisa-panathinaikos-2010-11-home-original-143625516",
        "link_int": "https://www.ebay.com/itm/389490870451"
    },
    {
        "id": 12,
        "titulo": "Kaiserslautern Mobil Gel 🇩🇪",
        "marca": "Nike", "tamanho": "G", "preco": "R$ 260,00",
        "link_br": None,
        "link_int": "https://www.ebay.it/itm/286873950722"
    },
    {
        "id": 13,
        "titulo": "Itália Copa do Mundo 2014 Pirlo #21 🇮🇹",
        "marca": "Puma", "tamanho": "M", "preco": "R$ 300,00",
        "link_br": "https://www.futclassics.com.br/product-page/italia-2014-home-m-5-6",
        "link_int": "https://www.ebay.com/itm/128011480704"
    },
    {
        "id": 14,
        "titulo": "Itália Campione Del Mondo Comemorativa 🇮🇹",
        "marca": "Puma", "tamanho": "G", "preco": "R$ 240,00",
        "link_br": None,
        "link_int": "https://www.ebay.com/itm/226370114363"
    },
    {
        "id": 15,
        "titulo": "Inglaterra 2007 Home 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "marca": "Umbro", "tamanho": "M", "preco": "R$ 280,00",
        "link_br": "https://www.futclassics.com.br/product-page/inglaterra-2007-home-11",
        "link_int": None
    },
    {
        "id": 16,
        "titulo": "Ibiza Eivissa 2009 Vermelha 🇪🇸",
        "marca": "Champs", "tamanho": "M", "preco": "R$ 150,00",
        "link_br": "https://brechodofutebol.com/products/ibiza-eivissa-2009-segunda-camisa-tam-p",
        "link_int": None
    },
    {
        "id": 17,
        "titulo": "Itália Rugby 2007 - 2009 🇮🇹",
        "marca": "Kappa", "tamanho": "G", "preco": "R$ 150,00",
        "link_br": "https://www.enjoei.com.br/p/camisa-selecao-italia-rugby-111153794",
        "link_int": "https://www.ebay.co.uk/itm/282395881167"
    }
]

def get_qr_url(link):
    if not link:
        return None
    encoded = urllib.parse.quote(link)
    return f"https://quickchart.io/qr?text={encoded}&size=150"

def fetch_qr_image(url):
    """Baixa a imagem via HTTP de forma segura e converte para fluxo de memória"""
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

def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15,
        leftMargin=15,
        topMargin=15,
        bottomMargin=15
    )
    
    styles = getSampleStyleSheet()
    
    # Remove emojis dos títulos no PDF para evitar conflito de fontes
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading2'], fontSize=10, leading=12, fontName="Helvetica-Bold")
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=8, leading=10)
    price_style = ParagraphStyle('PriceStyle', parent=styles['Normal'], fontSize=10, leading=12, textColor=colors.HexColor('#2e7d32'), fontName="Helvetica-Bold")
    
    story = []
    card_data_list = []
    
    for item in catalog:
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
            Paragraph(f"Preço: {item['preco']}", price_style),
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

    # Organiza os cartões em 2 colunas por linha
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
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(main_grid)
    doc.build(story)
    
    buffer.seek(0)
    return buffer.getvalue()

# Interface do Streamlit
st.title("🏷️ Gerador de Etiquetas para Embalagens")
st.write("Gere o arquivo PDF pronto para impressão de forma segura.")

if st.button("📄 Gerar e Baixar PDF com Etiquetas", type="primary", use_container_width=True):
    with st.spinner("Baixando QR codes e montando o PDF..."):
        try:
            pdf_data = generate_pdf()
            st.download_button(
                label="📥 Clique aqui para salvar o PDF",
                data=pdf_data,
                file_name="etiquetas_camisas.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.success("PDF gerado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

st.divider()

# Exibição na tela (Web)
cols = st.columns(2)
for idx, item in enumerate(catalog):
    col = cols[idx % 2]
    with col:
        with st.container(border=True):
            st.subheader(f"#{item['id']} {item['titulo']}")
            st.caption(f"**Marca:** {item['marca']} | **Tamanho:** {item['tamanho']}")
            st.markdown(f"### **Preço:** :green[{item['preco']}]")
            
            c_br, c_int = st.columns(2)
            qr_br = get_qr_url(item['link_br'])
            qr_int = get_qr_url(item['link_int'])
            
            with c_br:
                if qr_br:
                    st.caption("🇧🇷 **BR**")
                    st.image(qr_br, width=110)
                else:
                    st.caption("🇧🇷 *Sem Link BR*")
                    
            with c_int:
                if qr_int:
                    st.caption("🌎 **INT**")
                    st.image(qr_int, width=110)
                else:
                    st.caption("🌎 *Sem Link INT*")
