import dash_bootstrap_components as dbc
from dash import html 
from dash import dcc
from graphs import channl_videos ,data_table
class Chanel_videoPage:
  def __init__(self,channeldataframe,videoDataframe,ChannelId="UCBR8-60-B28hp2BmDPdntcQ",videoId = None) :
    
    self.channel = channeldataframe[channeldataframe['channelId']==ChannelId].iloc[0]
    self.videos = videoDataframe[videoDataframe['channelId']==ChannelId]
    self.unique_videos = self.videos.sort_values(by=['view_count'],ascending=False).drop_duplicates(subset=['video_id'],keep='first')
    trand_videos_count=self.unique_videos.shape[0]
    if videoId is None:
      self.default_video=self.unique_videos.iloc[0]
    else:
      self.default_video=self.unique_videos[self.unique_videos['video_id']==videoId].iloc[0]
    self.channel_profile_card = html.Div( className="insta-wrapper",children = [
          html.Div( className="insta-banner",children = [
            html.Canvas(className="backgroun_canvas" ,style={"background-image": f"url({self.channel['cover_image']})"}
            ),
          ]),
          html.Div( className="insta-details",children = [
            html.Div( className="insta-dp",children = [
              html.Canvas(className="profilPic_canvas", style={"background-image": f"url({self.channel['thumbnails']})"}),
            ]),
            html.Div( className="insta-name",children = [
              html.H2([self.channel["title"]],id="channel-title"), #channel title #
              html.Span(["Front End Web Developer"])
            ]),
            #################bans#############################
            html.Div( className="insta-followers-wrap",children = [
              html.Div( className="insta-follow",children = [
                html.H2(f'{self.channel["subscriberCount"]:,}',id="subs-count"),
                html.Span("Subscribers"), #numberof subscribers "subscribers"
              ]),
              html.Div( className="insta-follow",children = [
                html.H2([html.H2(f'{self.channel["viewCount"]:,}',id = "views-count"),
                html.Span("views")]), #numberof view  "views"
              ]),
            ]),
            #####
            html.Div( className="insta-followers-wrap",children = [
              html.Div( className="insta-follow",children = [
                html.H2([html.H2(f'{self.channel["videoCount"]:,}',id= "video-count"),
                html.Span("video")]), #numberof subscribers "subscribers"
              ]),
              html.Div( className="insta-follow",children = [
                html.H2([html.H2(f'{trand_videos_count:,}',id= "trend-count"),
                html.Span("Trend video")]), #numberof view  "views"
              ]),
            ]),
            #####
            #################end bans#############################
            html.Div( className="insta-button",children = [
              html.A(href=f"https://www.youtube.com/channel/{self.channel['channelId']}",target="_blank",children = "open in youtube"),
            ]),
            html.Div( className="insta-bio",children = [html.H2("Description"),
              html.P(id = "channel-description",children=[self.channel["description"]])
            ]),
          ]),
        ]),
  # "image-video-id" 'channel-title'  "subs-count" "views-count" "video-count" "trend-count" channel-description
    ##################
   
    
    self.unique_videos['view_count'] = self.unique_videos['view_count'].map('{:,}'.format)
    self.second_frame = html.Section(className="right_page", children=[
        dbc.Row([
            html.Div([
                dbc.Row([dcc.Graph(figure=channl_videos(self.videos),id="channel-videos-graph",className="channel-graph-1")]),
                dbc.Row([html.Div(data_table(self.unique_videos[["video_id","title","category_name","view_count"]],
                "video_id","channel-videos-table"),className="channel-video-table-container"),]),
            ],className="video_left_div"),html.Div([html.Div(id="video-card-id",children=[
                video_card(self.default_video),])
            ],className="video_right_div")
        ])
    ])
    self.channelVideosPage = html.Div([
      html.Div(className="insta-main",children=self.channel_profile_card)
      ,self.second_frame
      ])

def video_card(default_video):
  video_profile_card = html.Main(className="main", children=[
      html.Section(className="top-card", children=[
          html.Img(src=default_video['thumbnail_link'], alt="video Picture",id = "image-video-id"),
          html.A(className="menu-icon",href=f"https://www.youtube.com/watch?v={default_video['video_id']}",target="_blank", children=[
              html.Div(className="menu item1", children=[]),
              html.Div(className="menu item2", children=[]),
          ]),
          html.Div(className="name", children=[
              html.P([default_video['title']],id = 'card-video-title'), #'card-video-title' 'video-card-Published'  "video-card-views-count"  "video-card-likes-count"  "video-card-comment-count" 'video-card-description'
          ]),
      ]),
      html.Section(className="middle-card", children=[
          #################bans#############################
          html.Div( className="insta-followers-wrap",children = [
            html.Div( className="insta-follow",children = [
              html.H2(default_video["publishedAt"],id="video-card-Published"),html.Span("Published At"), 
            ]),
            
          ]),
          #####
          html.Div( className="insta-followers-wrap",children = [
            html.Div( className="insta-follow",children = [
              html.H2([html.H2(f'{default_video["view_count"]:,}',id= "video-card-views-count"),html.Span("Views")]),
            ]),
            html.Div( className="insta-follow",children = [
              html.H2([html.H2(f'{default_video["likes"]:,}',id= "video-card-likes-count"),html.Span("Likes")]), #numberof view  "views"
            ]),
            html.Div( className="insta-follow",children = [
              html.H2([html.H2(f'{default_video["comment_count"]:,}',id = "video-card-comment-count"),html.Span("Comments")]), #numberof view  "views"
            ]),
          ]),
          #####
          #################end bans#############################
          html.H1("Description"),
          html.P(default_video["description"],id = 'video-card-description'),

      ]),
  ])
  return video_profile_card
    
      