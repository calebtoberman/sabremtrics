import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pybaseball as pbb 
from plotly.subplots import make_subplots
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
        yaxis = dict(title='Spin Rate')
    )
    return figre

yu = graphPitchers('Yu','Darvish','2022-04-07','2022-10-05')
yu.show()

sho = statcast_lookup("shohei","ohtani","2022-06-01","2022-07-01")
PosNeg(sho)



p = make_subplots(
    rows=2, cols=3,
    subplot_titles=("4-Seam Fastball", "Sweeper", "Cutter", "Slider",
                    "Curveball", "Split-Finger"),
    shared_xaxes = True,
    shared_yaxes= True)

currpitch = sho[sho['pitch_name'] == '4-Seam Fastball']
p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                        mode = 'markers'),
                        row=1, col=1)

currpitch = sho[sho['pitch_name'] == 'Sweeper']
p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers'),
              row=1, col=2)

currpitch = sho[sho['pitch_name'] == 'Cutter']
p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers'),
              row=1, col=3)


currpitch = sho[sho['pitch_name'] == 'Slider']
p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers'),
              row=2, col=1)

currpitch = sho[sho['pitch_name'] == 'Curveball']
p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers'),
              row=2, col=2)

currpitch = sho[sho['pitch_name'] == 'Split-Finger']
p.add_trace(go.Scatter(x=currpitch['release_speed'], y=currpitch['release_spin_rate'],
                       mode = 'markers'),
              row=2, col=3)

p.update_layout(height=500, width=700,
                  title_text="Shohei Ohtani Pitches")

p.show()