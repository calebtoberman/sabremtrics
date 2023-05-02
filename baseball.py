import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pybaseball as pbb 
from plotly.subplots import make_subplots
import math
pbb.cache.enable()


#pitch_data = pbb.statcast(start_dt="2022-04-07", end_dt = "2022-10-5")
pitch_data = pbb.statcast(start_dt = "2022-06-01", end_dt = "2022-06-02")
f = pitch_data['description'].unique()
c = {f[i]:i for i in range(len(f))}

pitch_data['colors'] = pitch_data['description'].apply(lambda x: c[x])

def statcast_lookup(first, last, start_date, end_date):
    pldf = pbb.playerid_lookup(last, first)
    plid = (pldf.loc[0,'key_mlbam'])
    return pbb.statcast_pitcher(start_date, end_date, plid)

def PosNeg(df):
    #Adds Positive/Negative columns to a given data frame
    test = []
    positive = ['called_strike','foul','swinging_strike','foul_tip','foul_bunt','swinging_strike_blocked','missed_bunt','bunt_foul_tip']
    negative = ['ball','hit_into_play','hit_by_pitch','blocked_ball']
    for r in df['description']:
        if r in positive:
            test.append('Positive')
        elif r in negative:
            test.append('Negative')
        else:
            test.append('N/A')

    df['P/N?'] = test

    event = []
    p = ['strikeout', 'field_out', 'force_out', 'grounded_into_double_play','double_play','strikeout_double_play','caught_stealing_2b']
    n = ['home_run','single','sac_fly','walk','hit_by_pitch','double','sac_bunt','triple']
    for r in df['events']:
        if r in p:
            event.append("Positive")
        elif r in n:
            event.append("Negative")
        else:
            event.append("Neutral")

    df['Pos/Neg/Neu'] = event

PosNeg(pitch_data)

fastball = pitch_data[pitch_data['pitch_name'] == "4-Seam Fastball"]
slider = pitch_data[pitch_data['pitch_name'] == "Slider"]
change =  pitch_data[pitch_data['pitch_name'] == "Changeup"]
sink =  pitch_data[pitch_data['pitch_name'] == "Sinker"]
cut =  pitch_data[pitch_data['pitch_name'] == "Cutter"]
curve =  pitch_data[pitch_data['pitch_name'] == "Curveball"]
sweep =  pitch_data[pitch_data['pitch_name'] == "Sweeper"]
kc =  pitch_data[pitch_data['pitch_name'] == "Knuckle Curve"]
sffast =  pitch_data[pitch_data['pitch_name'] == "Split-Finger"]

##fastball[['release_speed','release_spin_rate','launch_speed','P/N?']].groupby('P/N?').describe()


s = pitch_data[['release_speed','release_spin_rate','launch_speed','P/N?']].groupby('P/N?').describe()
stats = pitch_data.groupby('P/N?').describe()

def graphPitchers(first, last, startdate, enddate):
    pitcher = statcast_lookup(first, last, startdate, enddate)
    PosNeg(pitcher)
    figre = go.Figure()

    for cat in ['Positive', 'Negative', 'Neutral']:
        curr = pitcher[pitcher['Pos/Neg/Neu'] == cat]

        figre.add_trace(go.Scatter(x = curr['release_speed'], y = curr['release_spin_rate'], 
                                                 mode = 'markers', 
                                                 name = cat))
    figre.update_layout(
        title = 'Pitch Velocity vs. Spin Rate by PA Result',
        xaxis = dict(title='Pitch Velocity'),
        yaxis = dict(title='Spin Rate'),
        width = 500,
        height = 800
    )
    return figre

yu = graphPitchers('Yu','Darvish','2022-04-07','2022-10-05')
yu.show()


##write function
ohtani = statcast_lookup('shohei','ohtani','2022-04-07','2022-10-05')
yudarvish = statcast_lookup('yu','darvish','2022-04-07','2022-10-05')
dylancease = statcast_lookup('dylan','cease','2022-04-07','2022-10-05')
coleirvin = statcast_lookup('cole','irvin','2022-04-07','2022-10-05')
joseberrios = statcast_lookup('José','Berríos','2022-04-07','2022-10-05')

finaldf = pd.concat([ohtani, yudarvish, dylancease, coleirvin, joseberrios])

h = finaldf[['pitch_name', 'release_speed']].groupby('pitch_name').describe()['release_speed','mean']
g = finaldf[['pitch_name', 'release_spin_rate']].groupby('pitch_name').describe()['release_spin_rate','mean']

def pitcher_subplots(first, last, avgspeed, avgspin):
    df = statcast_lookup(first, last, '2022-04-07','2022-10-05')
    PosNeg(df)
    speedminmax = df[['pitch_name','release_speed']].groupby('pitch_name').describe()['release_speed'][['min','max']]
    spinmax = df[['pitch_name','release_spin_rate']].groupby('pitch_name').describe()['release_spin_rate'][['min','max']]
    porder = df.groupby('pitch_name')['pitch_name'].count().sort_values(ascending = False)
    porder = porder[porder > 10].index
    nrows = int(math.ceil(len(porder)/3))
    sbplt = make_subplots(
            rows = nrows, cols = 3,
            subplot_titles = porder,
            shared_xaxes = False,
            shared_yaxes = False,
            x_title = "Pitch Speed (mph)",
            y_title = "Spin Rate (rpm)"
        )
    for i in range(len(porder)):
        pname = porder[i]
        r = (i // 3) + 1
        c = (i % 3) + 1        
        for cat in ['Negative','Positive']:
            curr = df[df['Pos/Neg/Neu'] == cat]
            currpitch = curr[curr['pitch_name'] == pname]
            sbplt.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                        mode = 'markers',
                        name = cat,
                        marker = dict(size = 3,opacity = 0.5 if cat == 'Positive' else 1, 
                        color = 'blue' if cat == 'Positive' else 'red'),
                        showlegend = False if i > 0 else True),
                    row=r, col=c)
            speedticks = list(range(int(speedminmax.loc[pname]['min'] - 2), int(speedminmax.loc[pname]['max'] + 2), 2))
            smax = int(spinmax.loc[pname]['max'])
            smin = int(spinmax.loc[pname]['min'])
            spingap = (smax - smin) // 4
            spinticks = list(range(smin - spingap, smax + spingap, spingap))
            #speedticks += [avgspeed.loc[pname]]
            #spinticks += [avgspin.loc[pname]]
            speedticks.sort()
            spinticks.sort()
            sbplt.update_xaxes(tickvals = speedticks, row = r, col = c)
            sbplt.update_yaxes(tickvals = spinticks, row = r, col = c)
        sbplt.add_trace(go.Scatter(x = [avgspeed.loc[pname]], y = [avgspin.loc[pname]], 
                                   showlegend = False, marker = dict(size = 10, opacity = 1,
                                                                     symbol = 'star-dot', color = 'black')),
                                   row = r, col = c)
    #sbplt.update_xaxes(range = [62, 103])
    #sbplt.update_yaxes(range=[700,3420])
    sbplt.update_layout(title_text = first.capitalize() + " " + last.capitalize() + " Pitches in 2022 Regular Season", height  = 1000, width = 1400)
    return sbplt


shohei = pitcher_subplots("Shohei","Ohtani", h , g)
shohei.show()

darvish = pitcher_subplots("Yu", "darvish", h, g)
darvish.show()

cease = pitcher_subplots("dylan", "cease", h, g)
cease.show()

irvin = pitcher_subplots("cole", "irvin", h, g)
irvin.show()

berrios = pitcher_subplots('José', 'Berríos', h, g)
berrios.show()
