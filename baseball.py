import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pybaseball as pbb 
pbb.cache.enable()


#pitch_data = pbb.statcast(start_dt="2022-04-07", end_dt = "2022-10-5")
pitch_data = pbb.statcast(start_dt = "2022-06-01", end_dt = "2022-06-02")
f = pitch_data['description'].unique()
c = {f[i]:i for i in range(len(f))}

pitch_data['colors'] = pitch_data['description'].apply(lambda x: c[x])


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

'''
fig = px.scatter(pitch_data, x = 'release_speed', y = 'release_spin_rate', color = 'description')

fig.show()
'''

test = []
positive = ['called_strike','foul','swinging_strike','foul_tip','foul_bunt','swinging_strike_blocked','missed_bunt','bunt_foul_tip']
negative = ['ball','hit_into_play','hit_by_pitch','blocked_ball']
for r in pitch_data['description']:
    if r in positive:
        test.append('Positive')
    elif r in negative:
        test.append('Negative')
    else:
        test.append('N/A')

pitch_data['P/N?'] = test

fastball = pitch_data[pitch_data['pitch_name'] == "4-Seam Fastball"]

# spin rate, release velocity, lauunch speed

##fastball[['release_speed','release_spin_rate','launch_speed','P/N?']].groupby('P/N?').describe()


pitch_data[['release_speed','release_spin_rate','launch_speed','P/N?']].groupby('P/N?').describe()
stats = pitch_data.groupby('P/N?').describe()

#def pitchstats():
'''
I want this to produce what I did above, with descriptive statstics by pitch, but one for each indiviudal pitch. 

'''
    #for i in range(pitch_data['pitch_name']):

#print(stats.to_markdown())
'''
scatter = go.Scatter(
    x = fastball['release_speed'],
    y = fastball['release_spin_rate'],
    mode = 'markers',
    #name = pitch_data['description'],
    marker = dict(
        color = fastball['colors'],
        line_width=1
    )
)

layout = go.Layout(
    title = 'Pitch Velocity vs. Spin Rate by Outcome for 4-Seam Fastballs',
    xaxis = dict(title='Pitch Velocity'),
    yaxis = dict(title='Spin Rate')
)

fig = go.Figure(data=scatter, layout=layout)

fig.show()
'''

fig = px.scatter(fastball, x = 'release_speed', y = 'release_spin_rate', color = 'description')

fig.show()