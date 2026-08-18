import streamlit as st
import urllib.parse
import io
import requests

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Gerador de Etiquetas & Catálogo", page_icon="🏷️", layout="wide")

# WhatsApp do Vendedor
PHONE_NUMBER = "5511942762908"

# Lista do catálogo de camisas (17 itens)
catalog = [
    {
        "id": 1,
        "titulo": "Operário MS Home #9 🇧🇷",
        "marca": "Champs", "tamanho": "M", "preco": "R$ 60,00",
        "link_br": "https://www.sofutebolbrasil.com/produto/569/camisa-oficial-operario-ms",
        "link_int": None,
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Operario+MS+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Operario+MS+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Operario+MS+-+Detalhes"
        }
    },
    {
        "id": 2,
        "titulo": "Juventus da Mooca Azul 459 Anos #9 🇧🇷",
        "marca": "Superbolla", "tamanho": "M", "preco": "R$ 120,00",
        "link_br": "https://www.mercadolivre.com.br/camisa-juventus-da-mooca-especial-2015-azul/up/MLBU1726959953",
        "link_int": None,
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Juventus+Mooca+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Juventus+Mooca+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Juventus+Mooca+-+Detalhes"
        }
    },
    {
        "id": 3,
        "titulo": "Juventus 2007/2008 Scudetto 🇮🇹",
        "marca": "Nike", "tamanho": "M", "preco": "R$ 150,00",
        "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035",
        "link_int": None,
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Juventus+07/08+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Juventus+07/08+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Juventus+07/08+-+Detalhes"
        }
    },
    {
        "id": 4,
        "titulo": "Juventus 2015/2016 Rosa 🇮🇹",
        "marca": "Adidas Climacool", "tamanho": "G", "preco": "R$ 350,00",
        "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035",
        "link_int": "https://www.ebay.com/itm/389084099014",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Juventus+Rosa+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Juventus+Rosa+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Juventus+Rosa+-+Detalhes"
        }
    },
    {
        "id": 5,
        "titulo": "Jaqueta Juventus 2009/2010 Treino 🇮🇹",
        "marca": "Nike", "tamanho": "G", "preco": "R$ 299,00",
        "link_br": None,
        "link_int": "https://www.ebay.com/itm/168192283231",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Jaqueta+Juve+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Jaqueta+Juve+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Jaqueta+Juve+-+Detalhes"
        }
    },
    {
        "id": 6,
        "titulo": "São Paulo 2007 Adriano Imperador #10 🇧🇷",
        "marca": "Reebok", "tamanho": "G", "preco": "R$ 199,00",
        "link_br": "https://memoriasdoesporteoficial.com.br/produto/camisa-sao-paulo-reebok-2007-tricolor/",
        "link_int": "https://www.ebay.com/itm/175121591014",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=SPFC+Adriano+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=SPFC+Adriano+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=SPFC+Adriano+-+Detalhes"
        }
    },
    {
        "id": 7,
        "titulo": "São Paulo 1997 Denilson #11 🇧🇷",
        "marca": "Adidas", "tamanho": "G", "preco": "R$ 450,00",
        "link_br": "https://pe.olx.com.br/grande-recife/esportes-e-lazer/roupas-esportivas/camisa-sao-paulo-adidas-1997-datacontrol-1508643853",
        "link_int": None,
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=SPFC+1997+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=SPFC+1997+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=SPFC+1997+-+Detalhes"
        }
    },
    {
        "id": 8,
        "titulo": "Blusa Agasalho São Paulo 1993 🇧🇷",
        "marca": "Del-Lini Tricot", "tamanho": "G", "preco": "R$ 600,00",
        "link_br": None,
        "link_int": None,
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Agasalho+SPFC+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Agasalho+SPFC+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Agasalho+SPFC+-+Detalhes"
        }
    },
    {
        "id": 9,
        "titulo": "Liverpool 2006/2007 Home 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "marca": "Adidas", "tamanho": "G", "preco": "R$ 350,00",
        "link_br": "https://www.mercadolivre.com.br/camisa-liverpool-2005-2006-adidas-teamgeist-original-epoca/up/MLBU3358810718",
        "link_int": "https://www.ebay.com/itm/197498583510",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Liverpool+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Liverpool+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Liverpool+-+Detalhes"
        }
    },
    {
        "id": 10,
        "titulo": "Sampdoria 2004/2005 ERG Azul 🇮🇹",
        "marca": "Kappa", "tamanho": "G", "preco": "R$ 320,00",
        "link_br": None,
        "link_int": "https://www.ebay.com/itm/267415041067",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Sampdoria+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Sampdoria+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Sampdoria+-+Detalhes"
        }
    },
    {
        "id": 11,
        "titulo": "Panathinaikos 2010/2011 Home 🇬🇷",
        "marca": "Adidas", "tamanho": "M", "preco": "R$ 260,00",
        "link_br": "https://www.enjoei.com.br/p/camisa-panathinaikos-2010-11-home-original-143625516",
        "link_int": "https://www.ebay.com/itm/389490870451",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Panathinaikos+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Panathinaikos+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Panathinaikos+-+Detalhes"
        }
    },
    {
        "id": 12,
        "titulo": "Kaiserslautern Mobil Gel 🇩🇪",
        "marca": "Nike", "tamanho": "G", "preco": "R$ 260,00",
        "link_br": None,
        "link_int": "https://www.ebay.it/itm/286873950722",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Kaiserslautern+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Kaiserslautern+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Kaiserslautern+-+Detalhes"
        }
    },
    {
        "id": 13,
        "titulo": "Itália Copa do Mundo 2014 Pirlo #21 🇮🇹",
        "marca": "Puma", "tamanho": "M", "preco": "R$ 300,00",
        "link_br": "https://www.futclassics.com.br/product-page/italia-2014-home-m-5-6",
        "link_int": "https://www.ebay.com/itm/128011480704",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Italia+Pirlo+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Italia+Pirlo+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Italia+Pirlo+-+Detalhes"
        }
    },
    {
        "id": 14,
        "titulo": "Itália Campione Del Mondo Comemorativa 🇮🇹",
        "marca": "Puma", "tamanho": "G", "preco": "R$ 240,00",
        "link_br": None,
        "link_int": "https://www.ebay.com/itm/226370114363",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Italia+Campione+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Italia+Campione+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Italia+Campione+-+Detalhes"
        }
    },
    {
        "id": 15,
        "titulo": "Inglaterra 2007 Home 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "marca": "Umbro", "tamanho": "M", "preco": "R$ 280,00",
        "link_br": "https://www.futclassics.com.br/product-page/inglaterra-2007-home-11",
        "link_int": None,
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Inglaterra+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Inglaterra+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Inglaterra+-+Detalhes"
        }
    },
    {
        "id": 16,
        "titulo": "Ibiza Eivissa 2009 Vermelha 🇪🇸",
        "marca": "Champs", "tamanho": "M", "preco": "R$ 150,00",
        "link_br": "https://brechodofutebol.com/products/ibiza-eivissa-2009-segunda-camisa-tam-p",
        "link_int": None,
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Ibiza+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Ibiza+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Ibiza+-+Detalhes"
        }
    },
    {
        "id": 17,
        "titulo": "Itália Rugby 2007 - 2009 🇮🇹",
        "marca": "Kappa", "tamanho": "G", "preco": "R$ 150,00",
        "link_br": "https://www.enjoei.com.br/p/camisa-selecao-italia-rugby-111153794",
        "link_int": "https://www.ebay.co.uk/itm/282395881167",
        "fotos": {
            "frente": "https://via.placeholder.com/400x500.png?text=Italia+Rugby+-+Frente",
            "verso": "https://via.placeholder.com/400x500.png?text=Italia+Rugby+-+Verso",
            "detalhes": "https://via.placeholder.com/400x500.png?text=Italia+Rugby+-+Detalhes"
        }
    }
]

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

def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, rightMargin=15, leftMargin=15, topMargin=15, bottomMargin=15
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading2'], fontSize=10, leading=12, fontName="Helvetica-Bold")
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=8, leading=10)
    price_style = ParagraphStyle('PriceStyle', parent=styles['Normal'], fontSize=10, leading=12, textColor=colors.HexColor('#2e7d32'), fontName="Helvetica-Bold")
    
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

# --- Interface Web (Streamlit) ---
st.title("🏷️ Gerador de Etiquetas & Catálogo de Camisas")
st.write("Visualize as fotos dos produtos, acesse os links de comparação e baixe o PDF para impressão.")

# Botão para geração do PDF de impressão
if st.button("📄 Gerar e Baixar PDF de Etiquetas", type="primary", use_container_width=True):
    with st.spinner("Preparando o arquivo PDF com as etiquetas..."):
        try:
            pdf_data = generate_pdf()
            st.download_button(
                label="📥 Clique aqui para salvar o arquivo PDF",
                data=pdf_data,
                file_name="etiquetas_camisas.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.success("PDF pronto para baixar!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

st.divider()

# Grade em 2 colunas para o catálogo
cols = st.columns(2)

for idx, item in enumerate(catalog):
    col = cols[idx % 2]
    with col:
        with st.container(border=True):
            st.subheader(f"#{item['id']} {item['titulo']}")
            st.caption(f"**Marca:** {item['marca']} | **Tamanho:** {item['tamanho']}")
            st.markdown(f"### **Preço:** :green[{item['preco']}]")
            
            # --- Seção de Fotos (Frente ▶️ Verso ▶️ Detalhes ▶️) ---
            with st.expander("📷 Ver Fotos do Produto"):
                tab_frente, tab_verso, tab_detalhes = st.tabs(["Frente ▶️", "Verso ▶️", "Detalhes ▶️"])
                
                with tab_frente:
                    st.image(item['fotos']['frente'], caption="Visão Frontal", use_container_width=True)
                with tab_verso:
                    st.image(item['fotos']['verso'], caption="Visão Traseira", use_container_width=True)
                with tab_detalhes:
                    st.image(item['fotos']['detalhes'], caption="Detalhes e Marcações", use_container_width=True)
            
            st.divider()
            
            # --- Seção de Links e QR Codes ---
            c_br, c_int = st.columns(2)
            qr_br = get_qr_url(item['link_br'])
            qr_int = get_qr_url(item['link_int'])
            
            with c_br:
                st.caption("🇧🇷 **LINK 🇧🇷**")
                if item['link_br']:
                    st.markdown(f"[Acessar anúncio BR 🔗]({item['link_br']})")
                    if qr_br:
                        st.image(qr_br, width=110)
                else:
                    st.caption("*Sem Link BR*")
                    
            with c_int:
                st.caption("🌎 **LINK 🌎**")
                if item['link_int']:
                    st.markdown(f"[Acessar anúncio INT 🔗]({item['link_int']})")
                    if qr_int:
                        st.image(qr_int, width=110)
                else:
                    st.caption("*Sem Link INT*")
            
            st.divider()
            
            # --- Botão WhatsApp Laranja ---
            wa_text = urllib.parse.quote(f"Olá! Tenho interesse na camisa: #{item['id']} {item['titulo']}")
            wa_link = f"https://wa.me/{PHONE_NUMBER}?text={wa_text}"
            
            st.markdown(
                f"""
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <button style="
                        background-color: #FF6600;
                        color: white;
                        border: none;
                        padding: 10px;
                        border-radius: 6px;
                        font-weight: bold;
                        width: 100%;
                        cursor: pointer;
                        font-size: 14px;
                    ">
                        💬 Me Interessei Por Essa
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
