import dash_bootstrap_components as dbc
from dash import html 
from dash import dcc
from graphs import videoCount_fig ,Correlation_fig ,description_fig,title_fig,Treanding_count_fig
class channelPage:
    def __init__(self,channel_df,df_videos) :
        self.channel_df = channel_df
        self.df_videos = df_videos
        self.row = html.Div([
            # first row
            dbc.Row([dbc.Col(
                dcc.Graph(
                    id="Correlation_fig",
                    figure=Correlation_fig(self.channel_df), className="corr_graph_style"), className='style_col1',),
                dbc.Col(
                dcc.Graph(id="Treanding_count_fig",
                        figure=Treanding_count_fig(self.channel_df,self.df_videos), className="trend_count_style"), className='style_col2',),
            ],),
            # secand row
            dbc.Row([dbc.Col(
                    dcc.Graph(
                        id='videoCount_fig',
                        figure=videoCount_fig(self.channel_df), className='style_border'), className='style_row2',),
            ]),

            # third row
            dbc.Row([dbc.Col(
                    dcc.Graph(
                        id='title_fig',
                        figure=title_fig(self.channel_df), className='style_border'
                    ), align="start",),
                dbc.Col(
                dcc.Graph(
                    id='description_fig',
                    figure=description_fig(self.channel_df), className='style_border'), align="end",),
            ],)

        ],
        )
        self.channel_page=html.Div([
             html.H2(children='CHANNELS STATISTICS OVER THE WORLD', style={'textAlign': 'center',
             "padding-top":"11px","font-weight":"700"}),
            self.row,html.Div(id="click-data")])
