import plotly.graph_objects as go
import plotly
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")
from time import *
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, 'en_IN')
import plotly.express as px
cord={'Spain': [-4, 39], 'Nigeria': [7, 9], 'Hungary': [19, 47], 'Chile': [-71, -31], 'Iceland': [-18, 64], 'Australia': [134, -24], 'Morocco': [-7, 31], 'Sweden': [14, 59], 'United States': [-100, 39], 'Uruguay': [-56, -32], 'Switzerland': [8, 46], 'Finland': [25, 63], 'Indonesia': [117, -2], 'Italy': [12, 42], 'Romania': [24, 45], 'Afghanistan': [66, 33], 'Belgium': [4, 50], 'Germany': [10, 51], 'Peru': [-75, -6], 'Bolivia': [-64, -17], 'Sri Lanka': [80, 7], 'Portugal': [-7, 40], 'Ukraine': [31, 49], 'United Kingdom': [-3, 55], 'Cambodia': [104, 13], 'Iran': [54, 32], 'Mexico': [-100, 22], 'Tunisia': [9, 33], 'Brazil': [-53, -10], 'India': [78, 22], 'Montenegro': [19, 42], 'Japan': [139, 36], 'Austria': [13, 47], 'Dominican Republic': [-70, 19], 'Croatia': [17, 45], 'Moldova': [28, 47], 'Armenia': [44, 40], 'Iraq': [44, 33], 'Algeria': [2, 28], 'Argentina': [-64, -34], 'Philippines': [122, 12], 'Norway': [9, 60], 'China': [104, 35], 'Canada': [-107, 61], 'Ecuador': [-79, -1]}
df=pd.read_csv('file3.csv')
mapbox_accesstoken='pk.eyJ1Ijoic3VkaGFuMjQ3IiwiYSI6ImNrOWZ3OHFzNjA2eDYzZGxpdjhteGk5aHAifQ.rgLrTsuLxjeMS9LbXJMxWA'
px.set_mapbox_access_token(mapbox_accesstoken)
def strv(arg):
    return locale.format("%d", arg, grouping=True)
def globe(df):
    argdf=df
    argdf.rename(columns={'Continent':'O'},inplace=True)
    fig = px.scatter_geo(df, lat='Latitude',lon='Longtitude',
                      color='O',
                     hover_name="Country", # column added to hover information
                     size="Confirmed",
                     text="City",
                     height=800,width=1800
                     )
    fig.update_geos(projection_type="orthographic",
                    showcountries=True, countrycolor="Red",
                    showland=True, landcolor="lime",
        showocean=True, oceancolor="midnightblue",lakecolor="Blue"
        )

    fig.update_layout(
        title_text='Global Spread of Corono',
        titlefont=dict(
            size=40,
            color='Red'
        )
    )
    return fig
def author(df):
    argdf=df.loc[:700,:]
    argdf.rename(columns={'Continent':'O'},inplace=True)
    fig = px.scatter_mapbox(argdf, lat='Latitude',lon='Longtitude',
                          color='O',
                          hover_name='City',
                         size="Confirmed",
                         height=870
                         )
    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_accesstoken,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=46,
                lon=2
            ),
            pitch=0,
            zoom=1.45
        ),hoverlabel=dict(
            bgcolor="Red", 
            font_size=16, 
            font_family="Rockwell"
        )
    )
    fig.update_layout(
    annotations=[dict(text='Global Spread of COVID-19', x=0.5, y=0.99,
                      font=dict(family='Rockwell',color="Red",size=23), showarrow=False),
                 dict(text='Confirmed', x=0.95, y=0.99,
                      font=dict(family='Georgia',color="midnightblue",size=23), showarrow=False),
                 dict(text='Recovered', x=0.95, y=0.90,
                      font=dict(family='Georgia',color="midnightblue",size=23), showarrow=False),
                 dict(text='Deaths', x=0.928, y=0.81,
                      font=dict(family='Georgia',color="midnightblue",size=23), showarrow=False),
                 dict(text=strv(df.Confirmed.sum()), x=0.95, y=0.95,
                      font=dict(family='Droid Serif',color="Red",size=23), showarrow=False),
                 dict(text=strv(df.Recovered.sum()), x=0.95, y=0.85,
                      font=dict(family='Droid Serif',color="Red",size=23), showarrow=False),
                 dict(text=strv(df.Deaths.sum()), x=0.95, y=0.76,
                      font=dict(family='Droid Serif',color="Red",size=23), showarrow=False)
                 ])
    
    return fig
def createmap(arg):
    fig = make_subplots(
    rows=3, cols=2,
    column_widths=[0.6,0.4],
    row_heights=[0.4, 0.3,0.3],
    specs=[[{"type": "scattermapbox", "rowspan": 3}, {"type": "Table"}],
           [None , {'type':'domain'}],
           [None , {'type':'domain'}]])
    argdf=df.loc[df['Country'] == arg]
    argdf.sort_values(by='Confirmed', ascending=False,inplace=True)
    fig.add_trace(
    go.Table(
        header=dict(
            values=["Country", "City", "Confirmed",
                    "Recovered", "Deaths"],
            font=dict(size=10),line_color='darkslategray',fill_color='lightskyblue',
            align="left"
        ),
        cells=dict(
            values=[argdf.Country,argdf.City,argdf.Confirmed,argdf.Recovered,argdf.Deaths],
            align = "left",line_color='darkslategray',fill_color='lightcyan')
    ),
    row=1, col=2
    )
    fig.add_trace(
    go.Scattermapbox(lat=argdf["Latitude"],
                  lon=argdf["Longtitude"],
                     mode='markers',name=arg,
        marker=go.scattermapbox.Marker(
            size=argdf['Confirmed'],sizeref=2.*max(argdf['Confirmed'])/(40.**2),sizemode="area"
        ),text=argdf['City']+','+argdf['Confirmed'].astype(str),hoverinfo="text")
    ,row=1, col=1
    )
    fig.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_accesstoken,
        bearing=0,style='satellite-streets',
        pitch=0, center=dict(lat=cord[arg][1],lon=cord[arg][0]),
        zoom=3.5
    ),height=870
    )
    types=['Confirmed','Recovered','Deaths']
    typev=[argdf.Confirmed.sum(),argdf.Recovered.sum(),argdf.Deaths.sum()]
    colors=['Red','rgb(26, 196, 91)','Yellow']
    fig.add_trace(go.Pie(labels=argdf.City, values=argdf.Confirmed,textposition='inside'),row=2, col=2)
    crd=go.Pie(labels=types,hole=.7, values=typev,
                         marker=dict(colors=colors),textposition='inside')
    fig.add_trace(crd,row=3, col=2)
    fig.update_layout(
    annotations=[dict(text='Stay', x=0.83, y=0.12,
                      font=dict(color="Green",size=20), showarrow=False),
                 dict(text='Safe',x=0.84, y=0.08,
                      font=dict(color="Green",size=20), showarrow=False),
                 dict(text='Proportion of Confirmed,Recovered,Deaths',x=0.915, y=0.26,
                      font=dict(color="Green",size=20), showarrow=False),
                 dict(text='Proportion of Cites',x=0.76, y=0.63,
                      font=dict(color="Green",size=20),align='left',showarrow=False),
                 dict(text='Confirmed',x=0.96, y=0.63,
                      font=dict(color="Red",size=20), showarrow=False),
                 dict(text='Recovered',x=0.96, y=0.52,
                      font=dict(color="Red",size=20), showarrow=False),
                 dict(text='Deaths',x=0.94, y=0.41,
                      font=dict(color="Red",size=20), showarrow=False),
                 dict(text=strv(typev[0]),x=0.96, y=0.58,
                      font=dict(color="midnightblue",size=20), showarrow=False),
                 dict(text=strv(typev[1]),x=0.96, y=0.46,
                      font=dict(color="midnightblue",size=20), showarrow=False),
                 dict(text=strv(typev[2]),x=0.96, y=0.36,
                      font=dict(color="midnightblue",size=20), showarrow=False)
                 ])
    
    return fig
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

countries=['Afghanistan', 'Algeria', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Belgium', 'Bolivia', 'Brazil', 'Cambodia', 'Canada', 'Chile', 'China', 'Croatia', 'Dominican Republic', 'Ecuador', 'Finland', 'Germany', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Italy', 'Japan', 'Mexico', 'Moldova', 'Montenegro', 'Morocco', 'Nigeria', 'Norway', 'Pakistan', 'Peru', 'Philippines', 'Portugal', 'Romania', 'Slovakia', 'South Korea', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Tunisia', 'Ukraine', 'United Kingdom', 'United States', 'Uruguay']
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in sorted(list(set(df['Country'].to_list())))]+
                [{'label':'3d View', 'value': 'globe'}],
                value=None,placeholder='Select country'
            )
        ],
        style={'width': '15%', 'display': 'inline-block'}),
    ]),
    dcc.Graph(id='indicator-graphic'),
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value')])
def update_graph(xaxis_column_name='India'):
    if xaxis_column_name=='globe':
        return globe(df)
    elif xaxis_column_name:
        if xaxis_column_name not in cord.keys():
            cord[xaxis_column_name]=getaddress(xaxis_column_name)
        return createmap(xaxis_column_name)
    else:
        return author(df)
def run():
    app.run_server(debug=True,use_reloader=False)
import pandas as pd
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim,GoogleV3
from selenium import webdriver
from time import *
import datetime
import requests, json
import pycountry
import pycountry_convert as pc
def getcontinent(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name
def getcode(arg):
    try:
        return ((pycountry.countries.search_fuzzy(arg)[0].alpha_3))
    except:
        return 'KR'
def get_locations():
    data=pd.read_csv('Locations.csv')
    dic=dict()
    for row in data.to_dict(orient="row"):
        dic[(row['Country'],row['City'])]=[row['Latitude'],row['Longtitude']]
    return dic
def getaddress(address):
    url = 'http://photon.komoot.de/api/?q='
    resp = requests.get(url=url+address)
    data = json.loads(resp.text)
    return(data['features'][0]['geometry']['coordinates'])
def intnew(arg):
    s='0'
    for i in arg:
        if i.isdigit():
            s+=i
    return int(s)
st=time()
def eta(seconds):
    sec=seconds-st
    return "ETA: "+str(datetime.timedelta(seconds=sec))
def retrivestates(inp,country):
    soup = BeautifulSoup(inp, 'html.parser')
    mydivs = soup.findAll("div", {"class": "BLWS2"})
    cities=[]
    for i in mydivs:
        cities.append(i.text)
    mydivs = soup.findAll("div", {"class": "QM7g5b"})
    lis=[]
    for i in mydivs:
        lis.append(intnew(i.text))
    lis=[lis[i:i+3] for i in range(0, len(lis),3)]
    final=[]
    for i in range(len(cities)):
        final.append([country]+[cities[i]]+lis[i])
    return final
def prep():
    countries=['Afghanistan', 'Algeria', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Belgium', 'Bolivia', 'Brazil', 'Cambodia', 'Canada', 'Chile', 'China', 'Croatia', 'Dominican Republic', 'Ecuador', 'Finland', 'Germany', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Italy', 'Japan', 'Mexico', 'Moldova', 'Montenegro', 'Morocco', 'Nigeria', 'Norway', 'Pakistan', 'Peru', 'Philippines', 'Portugal', 'Romania', 'Slovakia', 'South Korea', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Tunisia', 'Ukraine', 'United Kingdom', 'United States', 'Uruguay']
    driver = webdriver.Chrome()
    data=[['Country','City','Confirmed','Recovered','Deaths','Latitude','Longtitude','Codes','Continent']]
    codes=dict()
    conts=dict()
    for i in range(len(countries)):
        url="https://www.google.com/search?q=covid+stats+"+countries[i]
        driver.get(url)
        if url!=driver.current_url:
            driver.close()
            sleep(3)
            driver = webdriver.Chrome()
            driver.get(url)
        retrieved=retrivestates(driver.page_source,countries[i])
        data.extend(retrieved)
        print(countries[i],'Cities:',len(retrieved),eta(time()))
    print('Total Records',len(data))
    driver.close()
    #print(df.to_string())
    locations=get_locations()
    upd=[]
    for i in range(1,len(data)):
        arg=data[i][:2]
        if locations.get((arg[0],arg[1]),'Not')=='Not':
            arg=','.join(arg)
            print(i,arg)
            try:
                geolocator = Nominatim()
                location = geolocator.geocode(arg)
                data[i]+=[location.latitude, location.longitude]
            except:
                data[i]+=getaddress(arg)
            upd.append(data[i][:2]+data[i][-2:])
        else:
            data[i]+=locations[(arg[0],arg[1])]
    for i in range(1,len(data)):
        if codes.get(data[i][0],'Not')=='Not':
            codes[data[i][0]]=getcode(data[i][0])
            data[i]+=[codes[data[i][0]]]
        else:
            data[i]+=[codes[data[i][0]]]
    for i in range(1,len(data)):
        if conts.get(data[i][0],'Not')=='Not':
            conts[data[i][0]]=getcontinent(data[i][0])
            data[i]+=[conts[data[i][0]]]
        else:
            data[i]+=[conts[data[i][0]]]
    df = pd.DataFrame(data[1:],columns=data[0])
    upd =pd.DataFrame(upd,columns=['Country','City','Latitude','Longtitude'])
    upd.to_csv('Locations.csv', mode='a', header=False)
    df.to_csv('file3.csv')

run()
    
