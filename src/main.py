import pandas as pd
import numpy as np   
import arabic_reshaper  # font format(language) in wordcloud
from bidi.algorithm import get_display
from regex import D
import stylecloud 
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import callback_context, Dash , dash_table # couldnot get html , dcc Input and  Output from dash==0.38.0rc1
from dash import html  # import dash_html_components as html
from dash import dcc  # import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from datetime import date
import base64
#################
from customize import select_sort,customize_dataframe ,validate_date
from graphs import cat_bar,draw_line,draw_tags,homePage_table
from homePage import homePage
from chanel_videoPage import Chanel_videoPage ,video_card# channelVideosPage
from staticTemplate import sidbar 
from bans_card import bansCards
from channelPage import channelPage
#####################################

#read videos data
videos_df = pd.read_csv("../data/slef_getharing_data.csv")
videos_df.dropna(subset=['trending_date'],inplace=True)
videos_df['trending_date']= videos_df['trending_date'].astype('datetime64[ns]')
videos_df['publishedAt']= videos_df['publishedAt'].astype('datetime64[ns]')
videos_df = videos_df.set_index('trending_date')
#read channels data
channels_df = pd.read_csv("../data/slef_getharing_channel.csv"

# print(sortdata.head(1))

###############################
###############################
app = JupyterDash(__name__,
    external_stylesheets=[   dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
        "https://unpkg.com/boxicons@2.1.2/css/boxicons.min.css"],
        suppress_callback_exceptions=True,show_undo_redo=True,prevent_initial_callbacks=True
        )
# app.config['suppress_callback_exceptions']=True
home_section = html.Section(id="page-content",className="home-section", children="sdfa"),
app.layout = html.Div(
    [dcc.Store(id='memory-output'),
    dcc.Store(id='memory-output2'),
    dcc.Location(id="home",refresh=False),  # component represents the location or address bar in your web browser
    sidbar,
    html.Section(id="page-content",className="home-section", children=homePage(videos_df,"2022-3-29","2022-4-28").home_page),
    
    ]
)
#sidebar open
@app.callback(
    [Output("sidebar", "className"),
     Output("btn", "className")],
    [Input("btn", "n_clicks")],
)
def togle_className(btnn):
    if not (btnn % 2 == 0):

        return "sidebar open", "bx bx-menu-alt-right"
    else:
        return "sidebar", "bx bx-menu"


#move around pages
@app.callback(
    #  
    Output("/home","className"),
    Output("/second_page","className"),
    Output("/third_page","className"),
    Output("page-content", "children"),
    Input("/home", "n_clicks"),#Input("home", "pathname"),prevent_initial_call=True,
    Input("/second_page","n_clicks"),
    Input("/third_page","n_clicks"),
    Input("memory-output2", "data"),
    Input("memory-output", "data"),prevent_initial_call=True,
)
def display_page(hom,second,third,mem2,mem1):
    ctx = callback_context
    ctxall = ctx.triggered
    ctx = ctx.triggered[0]['prop_id'].split('.')[0]
    print(ctxall)
    if ctx == "/home":
        return "nav-link active", "nav-link" ,"nav-link", homePage(videos_df,"2022-3-29","2022-4-28").home_page
    elif ctx == "/second_page":
        return "nav-link" ,"nav-link active", "nav-link" ,\
            channelPage(channel_df=channels_df,df_videos=videos_df).channel_page
    elif ctx == "/third_page":
        chId="UCOA1y6Wu0kug8rbOpvHFZEQ"#"UCBR8-60-B28hp2BmDPdntcQ"
        return "nav-link" ,"nav-link ", "nav-link active" ,\
            Chanel_videoPage(channels_df,videos_df,chId).channelVideosPage#html.Div(html.H1("second page", style={"text-align": "center"}))
    elif ctx == "memory-output2":
        if ctxall[0]['value'] is not None:
            chId = ctxall[0]['value']
            return "nav-link" ,"nav-link ", "nav-link active" ,\
                Chanel_videoPage(channels_df,videos_df,chId).channelVideosPage
    elif ctx == "memory-output":
        if ctxall[0]['value'] is not None:
            chId = ctxall[0]['value'][0]
            videoid = ctxall[0]['value'][1]
            return "nav-link" ,"nav-link ", "nav-link active" ,\
                Chanel_videoPage(channels_df,videos_df,chId,videoid).channelVideosPage   

#########################
############################################################cards##################################################################
@app.callback(
    Output('tags-images','src'),
    Output("top_category","children"),Output("top_category_views","children")
    ,Output("top_view","children"),Output("top_view_views","children"),
    Output("top_region","children"),Output("top_region_views","children"),
    Input('my-date-picker-range', 'start_date'),Input('my-date-picker-range', 'end_date'),Input('country-dropdown', 'value'),)
def update(start_date,end_date,country_value):
#state vs input
    card_df = select_sort(videos_df,c_bar_regions=country_value,c_bar_start_date=start_date,c_bar_end_date=end_date)
    top_region =card_df.drop_duplicates(subset=['video_id','regions'],keep='first').pivot_table(index='regions',values='view_count',aggfunc='sum').sort_values(by= 'view_count',ascending=False)
    card_df.drop_duplicates(subset=['video_id'],keep='first',inplace=True)

    src= draw_tags(card_df)

    top_cat= card_df.pivot_table(index='category_name',values='view_count',aggfunc='sum').sort_values(by= 'view_count',ascending=False)
    return  src, \
     top_cat.index[0],str(f"{top_cat.iloc[0]['view_count']:,}") ,    \
     card_df.iloc[0]['title'],str(f"{card_df.iloc[0]['view_count']:,}") ,       \
     top_region.index[0],str(f"{top_region.iloc[0]['view_count']:,}"),           \

##################################################home page graph update##################################################
@app.callback(
    Output('cat_bar_graph', 'figure'),Output('table-graph-container', 'children'),Output('draw_line_graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),Input('my-date-picker-range', 'end_date'),Input('country-dropdown', 'value'),
    Input("relation-selector", "value"))
def home_page_update_output(start_date, end_date,country_value,relation_selector):#,table_relation_selector,line_relation_selector):
    #validate start and end date
    start_date_string,end_date_string = validate_date(start_date,end_date)
    sortdata=select_sort(videos_df,c_bar_relation=relation_selector, c_bar_regions=country_value, c_bar_start_date=start_date_string, c_bar_end_date=end_date_string)
    
    fig1 =cat_bar(sortdata,relation_selector)
    fig2 =  draw_line(sortdata,relation_selector)
    videosTable = homePage_table(sortdata,relation_selector)    
    
    return fig1,videosTable,fig2
##################################################home page graph update##################################################
##############################################channels page####################################################
@app.callback(
    Output("memory-output2", "data"),
    Input('videoCount_fig', 'clickData'),
    Input('description_fig', 'clickData'),
    Input('Treanding_count_fig', 'clickData'),
    Input('title_fig', 'clickData'),prevent_initial_call=True
    )
def display_click_data(g1,g2,g3,g4):
   
    ctx = callback_context
    ctx = ctx.triggered
    if ctx[0]['value'] is not None:
        chId = ctx[0]['value']['points'][0]['customdata'][0]
        return chId
    else:
        pass
@app.callback(Output('memory-output','data'),
Input('home-table_graph-id', 'active_cell'),prevent_initial_call=True)
def return_pathname(cell):
     if cell :
        row = videos_df[videos_df['video_id']==cell['row_id']].iloc[0]
        channel = row['channelId']
        video = row['video_id']
        return channel,video

@app.callback(  
    Output("video-card-id","children"),
    Input("channel-videos-table","active_cell"),prevent_initial_call=True
)
def update_video_card(active_cell):
    if active_cell :
        video = videos_df[videos_df['video_id']==active_cell['row_id']].iloc[0]
        return video_card(video)

if __name__ == "__main__":
    app.run_server(debug=True,port=8070)