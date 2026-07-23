@st.cache_data
def carregar_dados():
    data = [
        # CAMISA SÃO PAULO 1997 - DENILSON #11 (LINKS RAW DO SEU GITHUB)
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
            "fotos": [
                "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/frente%201.jpeg",
                "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/verso/detalhes/verso1.jpeg",
                "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/verso/detalhe1.jpeg"
            ]
        },
        # CAMISA CUIABÁ (EXEMPLO)
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
                "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500"
            ]
        }
    ]
    return pd.DataFrame(data)
