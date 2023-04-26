from datetime import date
import numpy as np
import pandas as pd
def select_sort(dataframe,c_bar_relation="view_count", c_bar_regions="all world", c_bar_start_date="2020-8-12", c_bar_end_date='2030'):
    edit_dataframe = dataframe.loc[c_bar_start_date:c_bar_end_date]
    if c_bar_regions != 'all world':
        if c_bar_regions == "canada":
            c_bar_regions = "canda"
        edit_dataframe =edit_dataframe[edit_dataframe['regions']==c_bar_regions]
    
    if c_bar_relation != 'video_count':
        edit_dataframe.sort_values(c_bar_relation,ascending=False,inplace=True)
    else :
        edit_dataframe.sort_values('view_count',ascending=False,inplace=True)
    
    return edit_dataframe
def customize_dataframe(dataframe,graph,c_bar_relation="view_count"):
    
    
    if graph =='cat_bar':
        dataframe.drop_duplicates(subset=['video_id','regions'],keep='first',inplace=True)
        if c_bar_relation == 'video_count':
            dataframe = dataframe.pivot_table(index= 'category_name',columns='regions',values='video_id',aggfunc=np.size)
        else:
            dataframe = dataframe.pivot_table(index= 'category_name',columns='regions',values=c_bar_relation,aggfunc=np.sum)
        dataframe['sum']=dataframe.sum(axis=1)
        dataframe.sort_values('sum',ascending=True,inplace=True)
        
    elif graph =='table' :
        dataframe.drop_duplicates(subset='video_id',keep='first',inplace=True)#for best video in each catogry drop dublicate by categoryId
        # dataframe = dataframe.iloc[:10]
    # elif graph =='word_cloud':
    #     dataframe.drop_duplicates(subset=['video_id'],keep='first',inplace=True)
    #     dataframe = dataframe.pivot_table(index=["video_id","regions"],values='tags',aggfunc=np.sum)

    elif graph == "line_graph":
        if c_bar_relation == 'video_count':
            dataframe=dataframe.drop_duplicates(subset='video_id',keep='first')
            dataframe=dataframe.groupby([pd.Grouper(freq='D'),'regions'])['video_id'].count().reset_index(drop=False) # count no of rows
        else:
            dataframe=dataframe.drop_duplicates(subset='video_id',keep='first')
            dataframe=dataframe.groupby([pd.Grouper(freq='D'),'regions']).sum().reset_index(drop=False)

    return dataframe

def validate_date(start ,end):
    if start is not None :
        start_date_object = date.fromisoformat(start)
        if start_date_object >= date(2020, 8, 12):
            start_date_string = start_date_object.strftime('%B %d, %Y')
        else:
            start_date_string="2020-8-12"
    else:
        start_date_string="2020-8-12"
    if end is not None:
        end_date_object = date.fromisoformat(end)
        if end_date_object >= date.today():
            end_date_object = date.today()
        end_date_string = end_date_object.strftime('%B %d, %Y')
    else:
        end_date_string =  date.today().strftime('%B %d, %Y')
    return start_date_string,end_date_string