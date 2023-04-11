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



'''
scatter = go.Scatter(
    x = pitch_data['release_speed'],
    y = pitch_data['release_spin_rate'],
    mode = 'markers',
    #name = pitch_data['description'],
    marker = dict(
        color = pitch_data['colors'],
        line_width=1
    )
)

layout = go.Layout(
    title = 'Pitch Velocity vs. Spin Rate by Outcome',
    xaxis = dict(title='Pitch Velocity'),
    yaxis = dict(title='Spin Rate')
)

fig = go.Figure(data=scatter, layout=layout)

fig.show()

fig = px.scatter(pitch_data, x = 'release_speed', y = 'release_spin_rate', color = 'description')

fig.show()
'''


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


# spin rate, release velocity, lauunch speed

##fastball[['release_speed','release_spin_rate','launch_speed','P/N?']].groupby('P/N?').describe()


s = pitch_data[['release_speed','release_spin_rate','launch_speed','P/N?']].groupby('P/N?').describe()
stats = pitch_data.groupby('P/N?').describe()

#def pitchstats():
'''
I want this to produce what I did above, with descriptive statstics by pitch, but one for each indiviudal pitch. 

'''
    #for i in range(pitch_data['pitch_name']):

#print(stats.to_markdown())
'''
fb = px.scatter(fastball, x = 'release_speed', y = 'release_spin_rate', color = 'Pos/Neg/Neu', title = "4-Seam Fastball")
slide = px.scatter(slider, x = 'release_speed', y = 'release_spin_rate', color = 'Pos/Neg/Neu', title = "Slider")
cha = px.scatter(change, x = 'release_speed', y = 'release_spin_rate', color = 'Pos/Neg/Neu', title = "Changeup")
sinker = px.scatter(sink, x = 'release_speed', y = 'release_spin_rate', color = 'Pos/Neg/Neu', title = "Sinker")
cutter =  px.scatter(cut, x = 'release_speed', y = 'release_spin_rate', color = 'Pos/Neg/Neu', title = "Cutter")
cb =  px.scatter(curve, x = 'release_speed', y = 'release_spin_rate', color = 'Pos/Neg/Neu', title = "Curveballs")
sweeper =  px.scatter(sweep, x = 'release_speed', y = 'release_spin_rate', color = 'Pos/Neg/Neu',title = "Sweeper")
knuckcurve =  px.scatter(kc, x = 'release_speed', y = 'release_spin_rate', color = 'Pos/Neg/Neu', title = "Knuckle-Curve")
sf =  px.scatter(sffast, x = 'release_speed', y = 'release_spin_rate', color = 'Pos/Neg/Neu', title = "Split-Finger Fastball")

fb.show()
slide.show()
cha.show()
sinker.show()
cutter.show()
cb.show()
sweeper.show()
knuckcurve.show()
sf.show()
'''

def statcast_lookup(first, last, start_date, end_date):
    pldf = pbb.playerid_lookup(last, first)
    plid = (pldf.loc[0,'key_mlbam'])
    return pbb.statcast_pitcher(start_date, end_date, plid)

sho = statcast_lookup("shohei","ohtani","2022-06-01","2022-07-01")
PosNeg(sho)
shograph = go.Figure()

for cat in ['Positive', 'Negative', 'Neutral']:
    curr = sho[sho['Pos/Neg/Neu'] == cat]

    shograph.add_trace(go.Scatter(x = curr['release_speed'], y = curr['release_spin_rate'],
                              mode = 'markers',
                              name = cat))
shograph.update_layout(
    title = 'Pitch Velocity vs. Spin Rate by PA Result',
    xaxis = dict(title='Pitch Velocity'),
    yaxis = dict(title='Spin Rate')
)

yu = statcast_lookup("yu","darvish","2022-06-01","2022-07-01")
PosNeg(yu)
yugraph = go.Figure()

for cat in ['Positive', 'Negative', 'Neutral']:
    curr = sho[sho['Pos/Neg/Neu'] == cat]

    yugraph.add_trace(go.Scatter(x = curr['release_speed'], y = curr['release_spin_rate'],
                              mode = 'markers',
                              name = cat))
yugraph.update_layout(
    title = 'Pitch Velocity vs. Spin Rate by PA Result',
    xaxis = dict(title='Pitch Velocity'),
    yaxis = dict(title='Spin Rate')
)

yugraph.show()


'''
def whatINeedToDo(first, last, startdate, enddate):
    pitcher = statcast_lookup(first, last, startdate, enddate)
    PosNeg(pitcher)
    figre = go.Figure

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

yu = whatINeedToDo('Yu','Darvish','2022-06-01','2022-07-01')
'''
###########################################
###########################################
'''
scatter = go.Scatter(
    x = sho['release_speed'],
    y = sho['release_spin_rate'],
    mode = 'markers',
    #name = pitch_data['description'],
    marker = dict(
        color = sho['Pos/Neg/Neu'] ,
        line_width=1
    )
)

layout = go.Layout(
    title = 'Pitch Velocity vs. Spin Rate by Outcome',
    xaxis = dict(title='Pitch Velocity'),
    yaxis = dict(title='Spin Rate')
)

fig = go.Figure(data=scatter, layout=layout)

fig.show()

#When looking at individual pitchers, you can start to see clusters forming from pitch type.
'''
yugraph = go.Figure()

for cat in ['Positive', 'Negative', 'Neutral']:
    curr = sho[sho['Pos/Neg/Neu'] == cat]

    yugraph.add_trace(go.Scatter(x = curr['release_speed'], y = curr['release_spin_rate'],
                              mode = 'markers',
                              name = cat))
yugraph.update_layout(
    title = 'Pitch Velocity vs. Spin Rate by PA Result',
    xaxis = dict(title='Pitch Velocity'),
    yaxis = dict(title='Spin Rate')
)

yugraph.show()

p = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))
p.add_trace(go.Scatter(x=sho['release_speed'], y=sho['release_spin_rate'],
                       mode = 'markers'),
              row=1, col=1)

p.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),
           row=1, col=2)

p.add_trace(go.Scatter(x=[300, 400, 500], y=[600, 700, 800]),
              row=2, col=1)

p.add_trace(go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000]),
              row=2, col=2)

p.update_layout(height=500, width=700,
                  title_text="Multiple Subplots with Titles")

p.show()