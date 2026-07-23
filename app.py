import streamlit as st
import pandas as pd
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium
import plotly.graph_objects as go
import json
import os

# Configuração da página profissional
st.set_page_config(
    page_title="Patagonia Expedition 2024 · Elétrico vs Combustão",
    page_icon="🚗",
    layout="wide"
)

# ============================================================
# SISTEMA DE TRADUÇÕES UNIFICADO (PT / EN / ES)
# ============================================================
translations = {
    "PT": {
        "badge": "PESQUISA DE CAMPO · AUTOMOTIVO & ENERGIA · 2024–2026",
        "title": "Expedição Patagônia:",
        "title2": "Elétrico vs Combustão",
        "subtitle": "De São Paulo (Mooca) ao Fim do Mundo (Ushuaia & Puerto Williams). Um trajeto real de ~5.000 km cruzando 4 países, comparando um Tesla Model 3 elétrico contra um Hyundai Tucson a combustão.",
        "vehicle_specs": "Especificações dos Veículos",
        "route_map": "Mapa de Rotas, Carregadores (Tesla) & Postos de Gasolina (Tucson)",
        "route_map_hint": "▶ O marcador do Tesla percorre o trajeto real da expedição, ponto a ponto.",
        "comparison": "Comparativo de Custo (Estimativa USD)",
        "tesla_range": "Autonomia Tesla (Est.):",
        "tucson_range": "Autonomia Tucson (Est.):",
        "total_dist": "Distância Total Aprox.:",
        "details": "Detalhamento das Coordenadas e Pontos de Parada",
        "why_go": "Por que ir para a Patagônia?",
        "motivation": "A Patagônia oferece paisagens únicas no mundo. Viajar de carro permite uma conexão profunda com a natureza, cruzando fronteiras e desafiando limites tecnológicos.",
        "tab1": "🗺️ Rotas & Pontos de Parada (Tesla vs Tucson)",
        "tab2": "🔬 Especificações & Custos",
        "footer": "Projeto desenvolvido para Portfólio - Amauri Almeida",
        "stat1": "km percorridos",
        "stat2": "países cruzados",
        "stat3": "pontos mapeados",
        "stat4": "menor custo EV"
    },
    "EN": {
        "badge": "FIELD RESEARCH · AUTOMOTIVE & ENERGY · 2024–2026",
        "title": "Patagonia Expedition:",
        "title2": "Electric vs Combustion",
        "subtitle": "From São Paulo (Mooca) to the End of the World (Ushuaia & Puerto Williams). A real ~5,000 km route crossing 4 countries, comparing an electric Tesla Model 3 against a combustion Hyundai Tucson.",
        "vehicle_specs": "Vehicle Specifications",
        "route_map": "Route Map, Chargers (Tesla) & Gas Stations (Tucson)",
        "route_map_hint": "▶ The Tesla marker travels the expedition's real route, point by point.",
        "comparison": "Trip Cost Comparison (Estimated USD)",
        "tesla_range": "Tesla Range (Est.):",
        "tucson_range": "Tucson Range (Est.):",
        "total_dist": "Total Approx. Distance:",
        "details": "Route Coordinates & Stop Points Breakdown",
        "why_go": "Why go to Patagonia?",
        "motivation": "Patagonia offers unique landscapes. Traveling by car allows a deep connection with nature, crossing borders and challenging technological limits.",
        "tab1": "🗺️ Routes & Stop Points (Tesla vs Tucson)",
        "tab2": "🔬 Specs & Financial Analysis",
        "footer": "Project developed for Portfolio - Amauri Almeida",
        "stat1": "km traveled",
        "stat2": "countries crossed",
        "stat3": "mapped points",
        "stat4": "lower EV cost"
    },
    "ES": {
        "badge": "INVESTIGACIÓN DE CAMPO · AUTOMOTOR & ENERGÍA · 2024–2026",
        "title": "Expedición Patagonia:",
        "title2": "Eléctrico vs Combustión",
        "subtitle": "De São Paulo (Mooca) al Fin del Mundo (Ushuaia & Puerto Williams). Un trayecto real de ~5.000 km cruzando 4 países, comparando un Tesla Model 3 eléctrico contra un Hyundai Tucson a combustión.",
        "vehicle_specs": "Especificaciones de los Vehículos",
        "route_map": "Mapa de Ruta, Cargadores (Tesla) y Estaciones de Servicio (Tucson)",
        "route_map_hint": "▶ El marcador del Tesla recorre el trayecto real de la expedición, punto a punto.",
        "comparison": "Comparativa de Costo (Estimación USD)",
        "tesla_range": "Autonomía Tesla (Est.):",
        "tucson_range": "Autonomía Tucson (Est.):",
        "total_dist": "Distancia Total Aprox.:",
        "details": "Detalles de Coordenadas y Puntos de Parada",
        "why_go": "¿Por qué ir a la Patagonia?",
        "motivation": "La Patagonia ofrece paisajes únicos en el mundo. Viajar en auto permite una conexión profunda con la naturaleza, cruzando fronteras y desafiando límites tecnológicos.",
        "tab1": "🗺️ Rutas y Puntos de Parada (Tesla vs Tucson)",
        "tab2": "🔬 Especificaciones y Costos",
        "footer": "Proyecto desarrollado para Portafolio - Amauri Almeida",
        "stat1": "km recorridos",
        "stat2": "países cruzados",
        "stat3": "puntos mapeados",
        "stat4": "menor costo EV"
    }
}

# Seleção de idioma na barra lateral
lang = st.sidebar.selectbox("Language / Idioma", ["PT", "EN", "ES"])
t = translations[lang]

# ── INJEÇÃO DE ESTILOS CSS CUSTOMIZADOS (DESIGN PREMIUM · PADRÃO PORTFÓLIO) ─
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.hero-wrap {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #17324A 0%, #1A3A6E 55%, #143C6B 100%);
  border-radius: 20px; padding: 2.6rem 3rem; margin-bottom: 1.6rem; color: white;
  border: 1px solid rgba(255,255,255,0.08);
}
.hero-badge {
  display: inline-block; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25);
  color: #CFE0FF; font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 1.5px;
  padding: 0.35rem 0.8rem; border-radius: 999px; margin-bottom: 1rem;
}
.hero-title { font-family: 'Playfair Display', serif; font-size: 2.5rem; font-weight: 900; line-height: 1.2; max-width: 65%; }
.hero-title .accent { color: #6FA8FF; }
.hero-subtitle { font-size: 1.02rem; opacity: 0.85; margin-top: 0.9rem; max-width: 62%; line-height: 1.5; }

.hero-car-icon {
  position: absolute; top: 50%; right: 2.5rem; transform: translateY(-50%);
  width: 190px; height: 190px; opacity: 0.9;
}

.chip-row { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 1.4rem; }
.chip {
  background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.22);
  color: #E7EEFB; font-size: 0.78rem; padding: 0.4rem 0.85rem; border-radius: 999px;
  font-family: 'DM Mono', monospace;
}

.metric-box {
  background: white; border-radius: 16px; padding: 1.2rem; border-top: 4px solid #3A7ACA;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06); text-align: center; margin-bottom: 1rem;
}
.metric-val { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 900; color: #1A3A6E; }
.metric-label { font-size: 0.75rem; color: #6A7888; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem;}

.stat-card {
  background: white; border-radius: 14px; padding: 1.1rem 0.5rem; text-align: center;
  border-top: 3px solid #1A3A6E; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.stat-card .stat-val { font-family: 'Playfair Display', serif; font-size: 1.7rem; font-weight: 900; color: #17324A; }
.stat-card .stat-lbl { font-size: 0.7rem; color: #6A7888; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 0.15rem; }

.map-hint { font-family: 'DM Mono', monospace; font-size: 0.8rem; color: #3A7ACA; margin-bottom: 0.6rem; }

@media (max-width: 900px) {
  .hero-title, .hero-subtitle { max-width: 100%; }
  .hero-car-icon { display: none; }
}
</style>
""", unsafe_allow_html=True)

# Cabeçalho Principal (Hero Section) — padrão bee-colony-collapse, ícone de carro no lugar da abelha
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-badge">{t['badge']}</div>
    <div class="hero-title">{t['title']} <span class="accent">{t['title2']}</span></div>
    <div class="hero-subtitle">{t['subtitle']}</div>
    <div class="chip-row">
        <div class="chip">🔋 Tesla Model 3</div>
        <div class="chip">⛽ Hyundai Tucson</div>
        <div class="chip">🇧🇷🇺🇾🇦🇷🇨🇱 4 países</div>
        <div class="chip">~5.000 km</div>
    </div>
    <svg class="hero-car-icon" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 38 L10 26 Q12 21 18 21 H46 Q52 21 54 26 L58 38" stroke="white" stroke-width="2" fill="rgba(255,255,255,0.08)"/>
        <path d="M4 38 H60 V44 Q60 47 57 47 H7 Q4 47 4 44 Z" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="2"/>
        <rect x="20" y="24" width="24" height="10" rx="2" fill="rgba(255,255,255,0.22)" stroke="white" stroke-width="1.5"/>
        <circle cx="16" cy="47" r="6" fill="#17324A" stroke="white" stroke-width="2"/>
        <circle cx="48" cy="47" r="6" fill="#17324A" stroke="white" stroke-width="2"/>
        <circle cx="16" cy="47" r="2" fill="white"/>
        <circle cx="48" cy="47" r="2" fill="white"/>
        <path d="M4 38 Q4 34 8 34 H12" stroke="#6FA8FF" stroke-width="2"/>
        <path d="M50 30 L54 30 L50 36 L54 36" stroke="#6FA8FF" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
</div>
""", unsafe_allow_html=True)

# Cartões de estatísticas rápidas
sc1, sc2, sc3, sc4 = st.columns(4)
with sc1:
    st.markdown(f'<div class="stat-card"><div class="stat-val">~5.000</div><div class="stat-lbl">{t["stat1"]}</div></div>', unsafe_allow_html=True)
with sc2:
    st.markdown(f'<div class="stat-card"><div class="stat-val">4</div><div class="stat-lbl">{t["stat2"]}</div></div>', unsafe_allow_html=True)
with sc3:
    st.markdown(f'<div class="stat-card"><div class="stat-val">13</div><div class="stat-lbl">{t["stat3"]}</div></div>', unsafe_allow_html=True)
with sc4:
    st.markdown(f'<div class="stat-card"><div class="stat-val">2.7×</div><div class="stat-lbl">{t["stat4"]}</div></div>', unsafe_allow_html=True)

st.write("")

# Informações de Motivação na Barra Lateral
st.sidebar.markdown(f"### {t['why_go']}")
st.sidebar.write(t["motivation"])

# Menu de Abas Simplificado (Aba de fotos removida)
tab1, tab2 = st.tabs([t["tab1"], t["tab2"]])

# ── ABA 1: MAPAS E TRAJETOS SIMULTÂNEOS ─────────────────────
with tab1:
    st.markdown(f"### {t['route_map']}")
    st.markdown(f'<div class="map-hint">{t["route_map_hint"]}</div>', unsafe_allow_html=True)

    if os.path.exists('route_data.json'):
        with open('route_data.json', 'r') as f:
            route_data = json.load(f)

        # Gerar mapa interativo
        m = folium.Map(location=[-38, -60], zoom_start=4, tiles='CartoDB positron')

        # Linha do trajeto unificado (Mooca -> Uruguaiana -> Sul)
        points = [[c['lat'], c['lon']] for c in route_data]

        # Trajeto de base (linha sólida discreta)
        folium.PolyLine(points, color="#1A3A6E", weight=2, opacity=0.35).add_to(m)

        # Trajeto "formiga" — dá a sensação de movimento constante ao longo da rota
        AntPath(
            points,
            color="#3A7ACA",
            weight=4,
            opacity=0.9,
            delay=800,
            dash_array=[12, 20],
            pulse_color="#FFFFFF",
            tooltip="Trajeto Geral da Expedição"
        ).add_to(m)

        # Mapeamento dinâmico de ícones por tipo de parada no JSON
        for city in route_data:
            icon_type = "info-sign"
            color_type = "orange"
            prefix_type = "glyphicon"

            if city['type'] == "Start":
                icon_type, color_type = "play", "green"
            elif "End" in city['type']:
                icon_type, color_type = "flag", "red"
            elif city['type'] in ["Tesla Charging", "Eletroposto"]:
                icon_type, color_type = "flash", "blue"
            elif city['type'] in ["Gas Station", "Posto Gasolina", "Posto", "Gas"]:
                icon_type, color_type = "gas-pump", "cadetblue"
                prefix_type = "fa"  # Ativa suporte para ícone de bomba de combustível
            elif city['type'] == "Tesla/Gas":
                icon_type, color_type = "refresh", "purple"

            folium.Marker(
                [city['lat'], city['lon']],
                popup=f"<b>{city['name']}</b><br>Tipo: {city['type']}",
                tooltip=f"{city['name']} ({city['type']})",
                icon=folium.Icon(color=color_type, icon=icon_type, prefix=prefix_type)
            ).add_to(m)

        # ── CARRO TESLA ANIMADO PERCORRENDO O TRAJETO REAL ──────
        # Ícone de carro (emoji-based DivIcon) que se desloca via JS entre os
        # waypoints reais do route_data.json, ponto a ponto, em loop.
        route_js_points = json.dumps(points)
        car_animation_js = f"""
        <script>
        (function() {{
            function initCarAnimation() {{
                var mapContainer = null;
                var mapKeys = Object.keys(window).filter(function(k) {{ return k.indexOf('map_') === 0; }});
                for (var i = 0; i < mapKeys.length; i++) {{
                    if (window[mapKeys[i]] && window[mapKeys[i]]._container) {{
                        mapContainer = window[mapKeys[i]];
                    }}
                }}
                if (!mapContainer) {{ setTimeout(initCarAnimation, 300); return; }}

                var routePoints = {route_js_points};
                var carIcon = L.divIcon({{
                    html: '<div style="font-size:26px; transform: translate(-50%,-50%); filter: drop-shadow(0 2px 3px rgba(0,0,0,0.45));">🚗</div>',
                    className: 'tesla-car-icon',
                    iconSize: [26, 26],
                    iconAnchor: [13, 13]
                }});
                var carMarker = L.marker(routePoints[0], {{icon: carIcon, zIndexOffset: 1000}}).addTo(mapContainer);

                var segIndex = 0;
                var steps = 60;
                var stepCount = 0;

                function lerp(a, b, t) {{ return a + (b - a) * t; }}

                function animate() {{
                    var start = routePoints[segIndex];
                    var end = routePoints[(segIndex + 1) % routePoints.length];
                    var progress = stepCount / steps;
                    var lat = lerp(start[0], end[0], progress);
                    var lon = lerp(start[1], end[1], progress);
                    carMarker.setLatLng([lat, lon]);

                    stepCount++;
                    if (stepCount > steps) {{
                        stepCount = 0;
                        segIndex = (segIndex + 1) % routePoints.length;
                    }}
                    setTimeout(function() {{ requestAnimationFrame(animate); }}, 40);
                }}
                animate();
            }}
            setTimeout(initCarAnimation, 500);
        }})();
        </script>
        """
        m.get_root().html.add_child(folium.Element(car_animation_js))

        st_folium(m, width=1200, height=550)

        # Listagem estruturada das coordenadas do trajeto
        st.markdown(f"### {t['details']}")
        df_route = pd.DataFrame(route_data)
        st.dataframe(df_route[['name', 'lat', 'lon', 'type']], use_container_width=True)
    else:
        st.error("Arquivo 'route_data.json' não encontrado no diretório do projeto.")

# ── ABA 2: ESPECIFICAÇÕES TÉCNICAS & ANÁLISE DE CUSTOS ──────────
with tab2:
    st.markdown(f"### {t['vehicle_specs']}")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-val">Tesla Model 3</div>
            <div class="metric-label">2024 Long Range (100% Elétrico)</div>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://www.tesla.com/sites/default/files/model3new/social/model-3-main.jpg", use_container_width=True)
        st.write(f"**{t['tesla_range']}** 550 km")
        st.write("**Bateria:** 78.1 kWh")
        st.write("**Infraestrutura:** Rede de Eletropostos / Conectores CCS2")

    with col_v2:
        st.markdown("""
        <div class="metric-box" style="border-top-color: #8B2515;">
            <div class="metric-val" style="color: #8B2515;">Hyundai Tucson</div>
            <div class="metric-label">2024 Engine (Combustão Interna)</div>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://www.hyundai.com/content/dam/hyundai/ww/en/images/find-a-car/tucson/highlights/hyundai-tucson-nx4-highlights-exterior-pc.jpg", use_container_width=True)
        st.write(f"**{t['tucson_range']}** 750 km")
        st.write("**Tanque de Combustível:** 54 L")
        st.write("**Infraestrutura:** Redes de Postos (Ipiranga, YPF, Copec)")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(f"### {t['comparison']}")

    # Gráfico comparativo Plotly
    fig = go.Figure(data=[
        go.Bar(name='Tesla Model 3 (Charging)', x=['São Paulo ➔ Ushuaia'], y=[450], marker_color='#2D7A3A'),
        go.Bar(name='Hyundai Tucson (Gasoline)', x=['São Paulo ➔ Ushuaia'], y=[1200], marker_color='#8B2515')
    ])
    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Cost in USD ($)",
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# Rodapé unificado para portfólio
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6A7888; font-size: 0.85rem; padding: 1rem;">
    {t['footer']} |
    <a href="https://github.com/amaurialmeida" target="_blank" style="color: #3A7ACA; text-decoration: none;">GitHub</a>
</div>
""", unsafe_allow_html=True)
