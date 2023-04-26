from customize import customize_dataframe
import plotly.express as px
import base64
import numpy as np
import stylecloud 
import pandas as pd
from dash import  dash_table
import arabic_reshaper  # font format(language) in wordcloud
from bidi.algorithm import get_display
#############################################
#title style
title_update={
        'y':0.92,
        'x':0.5,
        "font_family":"Bongola"
        ,"font_size":24,
  }
#category_bar graph
def cat_bar(dataframe,c_bar_relation):

    chart_df = customize_dataframe(dataframe,"cat_bar",c_bar_relation)
    fig = px.bar( chart_df,y=list(chart_df.index),x= list(chart_df.columns)[:-1],orientation='h',  height=445,
        labels={'value':'','y':' '}	)
    country =list(chart_df.columns)[:-1]
    #colors = ['#c90000', '#e82674','#d46ecc', '#a4a5fd','#8acfff','#adedff','#c90000', '#e82674','#d46ecc', '#a4a5fd','#8acfff','#adedff','#c90000', '#e82674','#d46ecc', '#a4a5fd','#8acfff','#adedff']
    colors = ['#c90000', '#f77b72', '#a4a5fd','#fada5e','#fb607f','#5E376D',	'#adedff','#db7093','#21abcd','#f6adc6',
            '#d46ecc', '#fcc200','#00cc99',"#fb607f"]    
    fig.for_each_trace(lambda trace: trace.update(
        marker=dict(color=colors[country.index(trace.name)],line=dict(color='rgb(248, 248, 249)', width=1)
        )
    ))
    annotations = [] 
    for yd,xd in zip(list(chart_df.index),chart_df.values):
    # labeling the y-axis (category name)
        annotations.append(dict(xref='paper', yref='y',x=0.14, y=yd,xanchor='right',text=str(yd),
                                font=dict(family='Arial', size=11,color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the first Likert scale (on the top)(country name)
        # if yd == chart_df.index[-1]:
        #     annotations.append(dict(xref='x', yref='paper',x=xd[0] / 2, y=1.1,text=country[0],
        #                         font=dict(family='Arial', size=14,color='rgb(67, 67, 67)'),showarrow=False))
        space = xd[0]
        spacel = xd[0]
        for i in range(1, len(xd)-1):
                # labeling the Likert scale
                # if yd == chart_df.index[-1]:
                #     annotations.append(dict(xref='x', yref='paper',
                #                             x=space + (xd[i]/2), y=1.1,
                #                             text=country[i],
                #                             font=dict(family='Arial', size=12,
                #                                     color='rgb(67, 67, 67)'),
                #                             showarrow=False))
                space += xd[i]
                spacel += xd[0]
                # labeling the rest of percentages for each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',  
                        x=chart_df.values[-1,-1]+chart_df.values[-1,-1]/20  , y=yd,
                        text=str(round((xd[-1]/chart_df['sum'].sum())*100,1)) + '%',
                        font=dict(family='Arial', size=12,color='rgb(67, 67, 67)'),showarrow=False))

    fig.update_layout(annotations=annotations)
    fig.update_layout(
    xaxis=dict(showgrid=False,showline=False,showticklabels=False,tickprefix=False,zeroline=False,domain=[0.15, 1]),
    yaxis=dict(showgrid=False,showline=False,showticklabels=False,zeroline=False,),
        barmode='stack',paper_bgcolor='rgb(248, 248, 255)',plot_bgcolor='rgb(248, 248, 255)',margin=dict(l=50, r=40, t=60, b=5),
    showlegend=True, title_text="Category relationship with "+c_bar_relation ,
    #title = {'x':0.5,'y':0.94,'xanchor':'center','yanchor':'top',"font_color":"black"},
    )
    fig.update_layout(title=title_update)
    return fig
#line graph
def draw_line(dataframe,c_bar_relation):
    df2=customize_dataframe(dataframe,"line_graph",c_bar_relation)
    relation=c_bar_relation
    if c_bar_relation == 'video_count':
        c_bar_relation = 'video_id'
        relation= "Videos Count"
    # +" for "+ c_bar_regions+"Distribution"
    fig = px.line(df2, x="trending_date", y=c_bar_relation,color="regions", title=relation+ " Distribution" ,
    labels={'trending_date':'Date',c_bar_relation:relation})
    fig.update_layout(title=title_update)
    return fig
#tags image graph
def draw_tags(dataframe):
  #remove duplicate titles
    tags = dataframe
    tags = tags.loc[tags['tags']!='[None]']
    tags = tags[:100]
    # #we'll ignore videos without tags and join tags with space using '-'
    tags = tags['tags'].str.replace(' ','-').to_frame()
    tags = tags['tags'].str.replace('|',' ')
    textStr = tags.str.cat(sep=' ')
    # text = str(set(tags))        #prepare the tags for word processing
    words = arabic_reshaper.reshape(textStr)
    words = get_display(words)
    # print((textStr[:10]))
    stylecloud.gen_stylecloud(text = words,icon_name='fab fa-youtube',
    collocations=False,font_path='times.ttf',output_name='stylecloud.jpg')

    image_filename =r"stylecloud.jpg" 
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    src = 'data:image/png;base64,{}'.format(encoded_image.decode())
    return src
#data table graph
def data_table(dataframe,id_col,Id):
  
    dataframe['id']=dataframe[id_col]
    Data_Table =dash_table.DataTable(columns=[{"name": i, "id": i} for i in dataframe.columns[1:-1]],
    data=dataframe.to_dict('records'),
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    column_selectable="single",
    selected_columns=[],
    selected_rows=[],
    page_size=20,
    fixed_rows={'headers': True},
    style_table={"background-color":"white","width":"100%","max-width":"100%",'height': '100%', 'overflowY': 'auto',"font_family":"Bongola","border-collapse":"collapse"},
    
    style_cell={'minWidth': 15, 'maxWidth': 20, 'textAlign': 'left',
                'overflow': 'hidden', 'textOverflow': 'ellipsis',"border-width":"0" },
    style_header={
    'backgroundColor': 'rgb(245 50 50)', 'color': 'white',"text-align":"left","border":" 0px solid #ddd","border-bottom":" 1px solid #ddd",
    "padding":"8px","padding-bottom":"12px","padding-top":"12px","font-weight":"600"},
    # 'whiteSpace': 'normal','height': '10px',
    style_data={'lineHeight': '35px',
                'backgroundColor': 'white', 'color': 'black',"font_family":"Bongola","border":" 0px solid #ddd","border-bottom":" 1px solid #ddd",
                "padding":"8px"},
    tooltip_data=[
    {column: {'value': str(value), 'type': 'markdown'}
    for column, value in row.items()
    } for row in dataframe.to_dict('records')],
    tooltip_duration=None,
    style_cell_conditional=[{'if': {'column_id': 'title'}, 'minWidth': 40}], id=Id)
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f2f2f2',
        }
    ],
    return Data_Table
def homePage_table(dataframe,c_bar_relation):
    table=customize_dataframe(dataframe,'table',c_bar_relation).iloc[:100]
    # 'view_count' 'comment_count'
    if c_bar_relation != 'video_count':
        table = table[['video_id','title','category_name','publishedAt',c_bar_relation]]
        table[c_bar_relation] = table[c_bar_relation].map('{:,}'.format)
    else:
        table = table[['video_id','title','category_name','publishedAt','view_count']]
        table['view_count'] = table['view_count'].map('{:,}'.format)
        table = table.rename(columns={'view_count':'video count'})
    videosTable=data_table(table,'video_id','home-table_graph-id')
    return videosTable
# def channel_video_table(dataframe)

######################################################channel videos page#################################################
def channl_videos(dataframe,color_graph="Hot"):#,channel_id
    #df=dataframe[dataframe['channelId']==channel_id]
    fig = px.scatter(dataframe, x="publishedAt", y="view_count", hover_data=['title',"regions"],
                 size="view_count",color="view_count", color_continuous_scale=color_graph,size_max=40,
                           title=" Views Count for Channel Distribution")
    fig.update_layout(title=title_update)
    
    return fig

######################################################channel page##################################################################
def videoCount_fig(dataframe,color_graph="Hot"):
    df1 =dataframe.sort_values("publishedAt")
    df1=df1.iloc[1:]
    videoCount_fig = px.scatter(df1, x="publishedAt", y="videoCount", hover_data=['title'],custom_data=["channelId"],
                    size="videoCount",color="videoCount", color_continuous_scale=color_graph,size_max=35,
                     title="Videos Count For Each Channel")
    videoCount_fig.update_layout(title=title_update)
    return videoCount_fig
def Correlation_fig(dataframe,color_graph="Hot"):
    
    
    Correlation_fig=px.imshow(dataframe.corr(),
                    text_auto=True,color_continuous_scale=color_graph,
    title="Correlation Matrix of Numerical Features")
    Correlation_fig.update_layout(title=title_update)
    return Correlation_fig
def description_fig(dataframe,color_graph="Hot"):
    df_na=dataframe.dropna(subset=["description"])
    description_fig=px.scatter(df_na, y=df_na.description.apply(len),x="viewCount",hover_data=["title"],labels={"y":"description"}
                            ,color="viewCount",color_continuous_scale=color_graph,custom_data=["channelId"],
                           title="Views According to Description Length")
    description_fig.update_layout(title=title_update)
    return description_fig
def title_fig(dataframe,color_graph="Hot"):
    title_fig=px.scatter(dataframe, y=dataframe.title.apply(len),x="viewCount",hover_data=["title"],labels={"y":"Title"},custom_data=["channelId"],
                     color="viewCount",color_continuous_scale=color_graph,title="Views According to Title Length")
    title_fig.update_layout(title=title_update)
    return title_fig
def Treanding_count_fig(dataframe,dataframe_videos,color_graph="Hot"):
    df_trend=dataframe_videos.drop_duplicates("video_id").pivot_table(index=["channelId"],aggfunc=np.size).reset_index()
    df_trend=df_trend.sort_values("categoryId",ascending=False).iloc[:20]
    df_merge=df_trend[["categoryId","channelId"]].merge(dataframe[["channelId","title","country"]],how="inner",on="channelId")
    Treanding_count_fig=px.bar(df_merge,y="title",x="categoryId",labels={"categoryId":"T-V-count"},custom_data=["channelId"],
                           color="categoryId",color_continuous_scale=color_graph,
                           title=" Videos Count for Top Trending Channels")
    Treanding_count_fig.update_layout(title=title_update)
    return Treanding_count_fig