import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pybaseball as pbb 
from plotly.subplots import make_subplots
pbb.cache.enable()

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
        yaxis = dict(title='Spin Rate')
    )
    return figre

sho = statcast_lookup("shohei","ohtani","2022-06-01","2022-07-01")
PosNeg(sho)

#Broken Subplot code
p = make_subplots(
    rows=3, cols=3,
    subplot_titles=("4-Seam Fastball", "Sweeper", "Cutter", "Slider",
                    "Curveball", "Split-Finger"),
    shared_xaxes = True,
    shared_yaxes= True)

for cat in ['Positive', 'Negative', 'Neutral']:
    curr = sho[sho['Pos/Neg/Neu'] == cat]

    currpitch = curr[curr['pitch_name'] == '4-Seam Fastball']
    p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                        mode = 'markers',
                        name = cat),
                    row=1, col=1)

    currpitch = curr[curr['pitch_name'] == 'Sweeper']
    p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers',
                       name = cat),
                    row=1, col=2)

    currpitch = curr[curr['pitch_name'] == 'Cutter']
    p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers',
                       name = cat),
                    row=1, col=3)


    currpitch = curr[curr['pitch_name'] == 'Slider']
    p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers',
                       name = cat),
                    row=3, col=1)

    currpitch = curr[curr['pitch_name'] == 'Curveball']
    p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers',
                       name = cat),
                    row=3, col=2)

    currpitch = curr[curr['pitch_name'] == 'Split-Finger']
    p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers',
                       name = cat),
                    row=3, col=3)

p.update_layout(height=500, width=700,
                  title_text="Shohei Ohtani Pitches")

p.show()