from typing import Any
from django.views.generic import TemplateView
from django.templatetags.static import static
import folium
from folium.plugins import Draw
import os

class MapView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        

        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')
        out_route = os.path.join(data_dir, 'out_route.geojson')
        return_route = os.path.join(data_dir, 'return_route.geojson')
        maker_route = os.path.join(data_dir, 'maker_route.geojson')

        m = folium.Map(location=(-10.439829, -45.16325), zoom_start=15)
        
        
        coordinates = [
            {"location": [-10.43029, -45.174006],
             "tooltip": "TRAJETO SAÍDA DO IFPI",
             "popup": "IFPI - Campus Corrente"},
            {"location": [-10.438866, -45.173230],
             "tooltip": "1ª Parada",
             "popup": "Posto Primavera"},
            {"location": [-10.454374, -45.171460],
             "tooltip": "2ª Parada",
             "popup": "Praça Principal do Vermelhão"},
            {"location": [-10.439672, -45.168913],
             "tooltip": "3ª Parada",
             "popup": "Supermercado Rocha"},
            {"location": [-10.443239, -45.160735],
             "tooltip": "4ª Parada",
             "popup": "Praça da Igreja Batista"},
            {"location": [-10.445506, -45.157068],
             "tooltip": "5ª Parada",
             "popup": "15ª Regional de Educação"},
            {"location": [-10.451376, -45.146146],
             "tooltip": "6ª Parada",
             "popup": "Posto de Combustível do Aeroporto"},
            {"location": [-10.454766, -45.137556],
             "tooltip": "7ª Parada",
             "popup": "Escola Municipal Orley Cavalcante Pacheco"},
            {"location": [-10.442140, -45.158292],
             "tooltip": "8ª Parada",
             "popup":"APAEB Corrente"},
            {"location": [-10.439274, -45.162402],
              "tooltip": "9ª Parada",
              "popup": "SAMU Corrente"},
            {"location": [-10.436220, -45.162002],
                "tooltip": "10ª Parada",
                "popup": "Proximo ao Coronel"},
            {"location": [-10.429860, -45.161559],
                "tooltip": "11ª Parada",
                "popup": "Proximo ao posto Varejão"},
            {"location": [-10.43029, -45.174006],
                "tooltip": "12ª Parada",
                "popup": "Retorno ao IFPI"},
                
            # Adicione mais coordenadas conforme necessário
        ]

        draw = Draw(export=True)
        draw.add_to(m)

        icon_url = static('bus.png')

        # Adicione as coordenadas ao mapa como marcadores
        for coord in coordinates:
            folium.Marker(
                location=coord["location"],
                tooltip=coord["tooltip"],
                popup=coord["popup"],
                icon=folium.DivIcon(html=f"""
                    <div>
                        <img src="{icon_url}" style="width: 20px; height: 20px;" />
                    </div>
                """),
            ).add_to(m)

        # Adicione a rota de saída ao mapa
        
        try:
            if os.path.exists(out_route):
                folium.GeoJson(out_route, name="Rota de Saída",
                               style_function=lambda x: {'color': 'green'}).add_to(m)
            else:
                print(f"Erro: O arquivo {out_route} não foi encontrado.")
        except Exception as e:
            print(f"Erro ao carregar GeoJSON {out_route}: {e}")

        # Adicione a rota de retorno ao mapa
        try:
            if os.path.exists(return_route):
                folium.GeoJson(return_route, name="Rota de Retorno",
                               style_function=lambda x: {'color': 'red'}).add_to(m)
            else:
                print(f"Erro: O arquivo {return_route} não foi encontrado.")
        except Exception as e:
            print(f"Erro ao carregar GeoJSON {return_route}: {e}")

        # Adicione a rota do fabricante ao mapa
        try:
            if os.path.exists(maker_route):
                folium.GeoJson(maker_route, name="Maker Router",
                               marker=folium.Marker(
                                   icon=folium.DivIcon(html=f"""
                                      <div>
                                         <img src="{icon_url}" style="width: 40px; height: 40px;" />
                                      </div>
                                      """),
                               )).add_to(m)
            else:
                print(f"Erro: O arquivo {maker_route} não foi encontrado.")
        except Exception as e:
            print(f"Erro ao carregar GeoJSON {maker_route}: {e}")

        # Adicione uma linha que conecta as coordenadas no mapa
        folium.PolyLine(
            locations=[coord["location"] for coord in coordinates],
            color='blue',
            weight=5,
            opacity=0.7,
        ).add_to(m)

        map_html = m._repr_html_()

        return {'map': map_html}


