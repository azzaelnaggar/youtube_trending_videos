from bans_card import bansCards
import dash_bootstrap_components as dbc
from dash import html 
from dash import dcc 
from datetime import datetime,date
from customize import select_sort
from graphs import cat_bar,draw_line,homePage_table,draw_tags
import base64
#build radiobuttons list
def radio_items(id):
    select_relation= dbc.RadioItems(
                options = [
                    {'label': 'views ', 'value': 'view_count'},{'label': 'likes', 'value': 'likes'},
                    {'label': 'comments', 'value': 'comment_count'},{'label': 'videos', 'value': 'video_count'}
                    ],value = 'view_count',
                id=id,
                labelClassName="selector-item_label",
                className="selector",
                inputClassName="selector-item_radio",
            )
    return select_relation



#page control unit
class homePage:
    def __init__(self,videos_df,startDate,endDate):
        sortdata=select_sort(videos_df,c_bar_start_date=startDate,c_bar_end_date=endDate)

        videosTable = homePage_table(sortdata.copy(),"view_count")  
        fig1 =cat_bar(sortdata.copy(),"view_count")
        fig2 =  draw_line(sortdata.copy(),"view_count")
        # print(sortdata.head())
        card_df=sortdata.copy()
        top_region =card_df.drop_duplicates(subset=['video_id','regions'],keep='first').pivot_table(index='regions',values='view_count',aggfunc='sum').sort_values(by= 'view_count',ascending=False)
        card_df.drop_duplicates(subset=['video_id'],keep='first',inplace=True)


        top_cat= card_df.pivot_table(index='category_name',values='view_count',aggfunc='sum').sort_values(by= 'view_count',ascending=False)
        imgsrc= draw_tags(card_df)

        control_cell =html.Div([dcc.Dropdown(['all world','egypt', 'Saudi', 'uae', 'Algeria', 'morocco', 'usa', 'birtain', 'canada', 'russia', 'ukraine']
        , 'all world', id='country-dropdown'),dcc.DatePickerRange(
            minimum_nights=5,
            clearable=True,
            # with_portal=True,
            display_format='D-M-Y',
            start_date=date(2022, 3, 29),#date.fromisoformat(date.today().strftime("%Y-%m-%d")) ,#date(2020, 8, 12),
            end_date=date(2022, 4, 28),#date.fromisoformat(date.today().strftime("%Y-%m-%d")),
            id = 'my-date-picker-range'
        )],className="select-cell")

        first_row=dbc.Row([
            dbc.Col(className = "logoClass",children=[html.Img(src="/assets/logo.png")]),
            dbc.Col(
                bansCards(top_cat.index[0],str(f"{top_cat.iloc[0]['view_count']:,}"),card_df.iloc[0]['title'],
                str(f"{card_df.iloc[0]['view_count']:,}") ,top_region.index[0],str(f"{top_region.iloc[0]['view_count']:,}")).bansCard
            ,className="cards-col-row"),
            dbc.Col(control_cell,className="select_cell",style= {"flex":"0 0 0%;"})
            ])

        
        cat_bar_dash = dcc.Graph(id='cat_bar_graph',figure=fig1)


        table_dash = html.Div(className="table_dash"
            ,id= "table-graph-container",children=videosTable),

        line_dash =dcc.Graph(id='draw_line_graph',figure=fig2)

        self.home_page=html.Div([first_row,dbc.Row(dbc.Container(radio_items("relation-selector"))),
            dbc.Row([html.Div(cat_bar_dash,style={"margin-left":"8px","width":"55%"}),
                html.Div(html.Div([html.H4(children=["Most Populer tags"],style={"font-family":"Bongola"
        ,"font-size":24,'color':'#2a3f5f'}),html.Img(src=imgsrc,id='tags-images',
                )],className="tags_image_div"),style={"margin-right":"8px","width":"43%"})]),
            dbc.Row([html.Div(table_dash,style={"margin-left":"8px","width":"49%"}),html.Div(line_dash,style={"margin-right":"8px","width":"49%"})])
        ])

