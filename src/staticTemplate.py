import dash_bootstrap_components as dbc
from dash import html 

sidbar_content = [
    html.Div(className='logo-details', children=[
        html.I(className='bx bxl-youtube icon', ),
        html.H4(className='logo_name', children='Youtube_trending'),
        html.I(className='bx bx-menu', id="btn",
                n_clicks=0,),
    ]),
    html.Ul([
            html.Li([
                dbc.NavLink([
                    html.I(className='fa fa-home',
                           ),
                    html.Span(children="Home", className="links_name")
                ], href="/",id="/home",className="nav-link active"),
                html.Span(children="Home", className="tooltip")]),
            html.Li([
                dbc.NavLink([
                    html.I(className='bx bx-tv',
                           ),
                    html.Span(children="Channels", className="links_name")
                ], href="/second_page",id="/second_page"),
                html.Span(children="Channels", className="tooltip")]),
            html.Li([
                dbc.NavLink([
                    html.I(className='bx bxs-videos',
                           ),
                    html.Span(children="Channel Videos", className="links_name")
                ], href="/third_page",id="/third_page"),
                html.Span(children="Channel Videos", className="tooltip")])
            ], className="nav_list")

]

sidbar = dbc.Nav(sidbar_content, vertical=True,
                 pills=True, fill=True, className="sidebar", id="sidebar")
# home_section = html.Section(id="page-content",className="home-section", children=[])