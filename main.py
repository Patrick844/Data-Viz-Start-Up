
from plotly.subplots import make_subplots
import numpy as np
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly
import random
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_ctr = pd.read_csv("countries_startup.csv", delimiter=',')
df_cities = pd.read_csv("cities_startup.csv", delimiter=',')


df_ctr=df_ctr.rename(columns={'ranking ': 'ranking'})
df_ctr=df_ctr.iloc[:-1]
df_ctr_15=df_ctr.iloc[:15]



fig = px.bar(df_ctr_15, x="country", y="total score", barmode="group")


df_chg_pos=df_ctr[(df_ctr["change in position from 2020"] !='new entry') & (df_ctr["change in position from 2020"] !='new  entry') ]
(df_chg_pos["change in position from 2020"])
df_chg_pos=df_chg_pos[pd.to_numeric(df_chg_pos["change in position from 2020"]) > 0]
df_chg_pos=df_chg_pos.sort_values(by=["change in position from 2020"],ascending=False)
df_new=df_chg_pos[['country','change in position from 2020',"ranking"]]


previous_ranking=[]
df_chg_pos["change in position from 2020"]=df_chg_pos["change in position from 2020"].astype(int)
df_chg_pos=df_chg_pos.sort_values(by=["change in position from 2020"],ascending=False)
df_chg_pos=df_chg_pos[["change in position from 2020","change in position sign ","ranking","country"]]
[previous_ranking.append(df_chg_pos["change in position from 2020"].iloc[i].astype(int) + df_chg_pos["ranking"].iloc[i].astype(int) ) if df_chg_pos["change in position sign "].iloc[i] == "+" else previous_ranking.append(df_chg_pos["ranking"].iloc[i].astype(int) - df_chg_pos["change in position from 2020"].iloc[i].astype(int)  )for i in range(df_chg_pos["ranking"].size)]
previous_ranking=np.array(previous_ranking)


df_chg_pos["previous ranking"]= previous_ranking


df_previous=df_chg_pos[["change in position from 2020","country","previous ranking"]]
df_previous=df_previous.rename(columns={'previous ranking': 'ranking'})
df_previous["change in position from 2020"]=df_previous["change in position from 2020"].astype(int)
df_previous=df_previous.sort_values(by=["change in position from 2020"],ascending=False)
df_previous["year"]=2019

print(df_previous)

ids=df_previous.index
ids=ids+97


df_new["change in position from 2020"]=df_new["change in position from 2020"].astype(int)
df_new=df_new.sort_values(by=["change in position from 2020"],ascending=False)
df_new.set_index(ids,inplace=True)
df_new["year"]=2020

df_year=pd.concat([df_new,df_previous])
df_year=df_year.sort_values(by="country")
df_year_15=df_year.iloc[:30]
df_year_15=df_year_15.sort_values(by=["year","ranking"])



fig2 = px.bar(df_year_15, x="country", y="ranking", color="country",animation_frame="year", animation_group="country")






categories = ['business score','quality score',
              'quantity score']

fig3 = make_subplots(
    rows=1, cols=3,
    column_widths=[0.3, 0.3,0.3],
    row_heights=[1],
    specs=[[{"type": "Scatterpolar"}, {"type": "Scatterpolar"},{"type": "Scatterpolar"}]]

)



fig3.add_trace(go.Scatterpolar(
      r=[df_ctr["business score"].iloc[0] * 100,df_ctr["quality score"].iloc[0]*10,df_ctr["quantity score"].iloc[0]*10],
      theta=categories,
      fill='toself',
      name=df_ctr["country"].iloc[0]),
row=1, col=1
)

fig3.add_trace(go.Scatterpolar(
      r=[df_ctr["business score"].iloc[1]* 100,df_ctr["quality score"].iloc[1]*10,df_ctr["quantity score"].iloc[1] * 10],
      theta=categories,
      fill='toself',
      name=df_ctr["country"].iloc[1]),
row=1, col=2
)
fig3.add_trace(go.Scatterpolar(
      r=[df_ctr["business score"].iloc[2] * 100,df_ctr["quality score"].iloc[2]*10,df_ctr["quantity score"].iloc[2] * 10],
      theta=categories,
      fill='toself',
      name=df_ctr["country"].iloc[2]),
row=1, col=3
)

fig3.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,


    )),
  showlegend=False
)


df = pd.read_csv('cities_startup.csv')
# print(df["position"])


fig4 = px.treemap(df.sort_values(by="position", ascending=True).head(20), path=['country','city'], values='total score')
fig4.update_traces(root_color="lightgrey")



df["country"]=df["country"].str.lstrip()
df_continents=pd.read_csv('Continents.csv')
df=df.join(df_continents.set_index('Entity'), on='country')
fig5 = px.scatter_geo(df[~df['Continent'].isnull()], locations="Code", color="Continent",
                     hover_name="country", size="total score",
                     projection="natural earth")









with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": float})

df_fip=pd.read_csv("uscities.csv")
df_fip["city"]=df_fip["city"].str.strip()
df_cities=df_cities.join(df_fip.set_index("city"), on="city")
df_us=df_cities[df_cities["country"]==" United States"]

df_fipss=df_us[["county_fips","city","total score"]]
df_fipss=df_fipss.dropna()
df_fipss.sort_values(by="county_fips")
df=df.join(df_fipss.set_index("county_fips"),on="fips")
df['total score'] = df['total score'].fillna(0)



fig6 = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='total score',
                           color_continuous_scale="Viridis",
                           range_color=(0, 3),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'total score':'total score'}
                          )
fig6.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
score_max=int(df_cities["total score"].max())
print(score_max)
df_cities["total score"]=df_cities["total score"]/score_max*100
df_cities=df_cities.sort_values("total score", ascending=False)[:30]
fig7=go.Figure(data=go.Scatter(x=[random.random() for i in range(30)],
                y=[random.random() for i in range(30)],
                textfont={'size': df_cities["total score"], 'color': colors},
                #hoverinfo='text',
                #hovertext=['{0}{1}'.format(w, f) for w, f in zip(df_cities["city"], df_cities["total score"])],
                mode='text',
                text=df_cities["city"]
                ))


app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H2(children='Ranking by Total Score'),

        html.Div(children='''
            Bar Chart (Total Score)
        '''),

        dcc.Graph(
            id='graph1',
            figure=fig
        ),
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H2(children='Countries that changed ranking position from 2019 to 2020'),

        html.Div(children='''
        
        Interactive Bar Chart (Change in rank)
            
        '''),

        dcc.Graph(
            id='graph2',
            figure=fig2
        ),
    ]),

    html.Div([
        html.H2(children='''
         Comparison in business score, quality score and quantity score of the 3 country with higher rank
           (Scale change from one country to another)
         '''),

        html.Div(children='''
        Radar Chart (3 types of score)
    '''),

        dcc.Graph(
            id='graph3',
            figure=fig3
        ),
    ]),

    html.Div([
        html.H2(children='The score of each city by country'),

        html.Div(children='''
    Tree Map (Total Score by city)
'''),

        dcc.Graph(
            id='graph4',
            figure=fig4
        ),
    ]),

    html.Div([
        html.H2(children='Total score distributed on continent'),

        html.Div(children='''
    World Map 
'''),

        dcc.Graph(
            id='graph5',
            figure=fig5
        ),
    ]),

    html.Div([
        html.H2(children='Total score by cities in the USA'),

        html.Div(children='''
    USA Map
'''),

        dcc.Graph(
            id='graph6',
            figure=fig6
        ),
    ]),

    html.Div([
        html.H1(children='Ok Google ! What is the best city to open a company ?'),

        html.Div(children='''
    Scatter World Map 
'''),

        dcc.Graph(
            id='graph7',
            figure=fig7
        ),
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)
    print(df_previous.head())









