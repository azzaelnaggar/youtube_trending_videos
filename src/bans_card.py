import dash_bootstrap_components as dbc
from dash import html 
class bansCards :
    def __init__(self,catN,catV,vidN,vidv,regN,regV):
        print(regN)
        self.bansCard=dbc.Col(className="cards-row",style = {"width": "fit-content;"},children = [
            dbc.Col([html.Div(className='cpanel',children=[
                html.Div(className="icon-part", children=[
                    html.Div(className="icon-header", children=[
                        html.I(className="bx bx-category",children=[]),
                        html.H4(children="top Categorie")
                    ]),
                    html.P(id ="top_category",children=catN),
                    
                    html.P(id ="top_category_views",children=catV)
                ]),
            ])]),
            dbc.Col([html.Div(className='cpanel',children=[
                html.Div(className="icon-part", children=[
                    html.Div(className="icon-header", children=[
                        html.I(className="fa fa-eye",children=[]),
                        html.H4(children="top views")
                    ]),
                    html.P(id ="top_view",children=vidN),
                
                    html.P(id ="top_view_views",children=vidv)
                ]),
            ])]),
            dbc.Col([html.Div(className='cpanel',children=[
                html.Div(className="icon-part", children=[
                    html.Div(className="icon-header", children=[
                        html.I(className="bx bx-globe",children=[]),
                        html.H4(children="top region")
                    ]),
                    html.P(id ="top_region",children=regN),
                    
                    html.P(id ="top_region_views",children=regV)
                ]),
            ])])
        ])