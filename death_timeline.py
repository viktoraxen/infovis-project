import pandas as pd

# Load the datasets
characters = pd.read_csv('data/characters.tsv', sep='\t')
episodes = pd.read_csv('data/episodes.tsv', sep='\t')
scenes = pd.read_csv('data/scenes.tsv', sep='\t')
scenes_characters = pd.read_csv('data/scenes_characters.tsv', sep='\t')
killers = pd.read_csv('data/killers.tsv', sep='\t')

importance_df = scenes.merge(scenes_characters, on='#sid', how="left")
# Calculate total duration for each character
character_importance = (
    importance_df.groupby(['uid'], as_index=False)['duration']
    .sum()
    .sort_values(by='duration', ascending=False)
)

# Calculate the normalized importance score (0-1) using min-max normalization
min_duration = character_importance['duration'].min()
max_duration = character_importance['duration'].max()

# Normalize the duration values
character_importance['importance_score'] = (character_importance['duration'] - min_duration) / (max_duration - min_duration)

deaths = scenes_characters[scenes_characters['killed'] == True]

deaths = deaths.merge(scenes, on='#sid', how='left')  # Add episode details

deaths = deaths.merge(episodes, left_on='eid', right_on='#eid', how='left')  # Add season details

deaths = deaths.merge(killers, left_on=['#sid', 'uid'], right_on=['sid', '#uid'], how='left')  # Add killer info

final_df = deaths.merge(character_importance, on='uid', how='left')  # Add importance info

death_timeline = final_df[['uid','season', 'episode',"title", 'name', 'killer', 'year','importance_score', 't_start']].copy()

###########################
### Main visualization
###########################

import numpy as np
import pandas as pd
import plotly.express as px  # Importing plotly.express

# Ensure 't_start' is numeric
death_timeline['t_start'] = pd.to_numeric(death_timeline['t_start'], errors='coerce')

# Combine Season-Episode with Title
death_timeline['season_episode'] = death_timeline['season'].astype(str) + '.' + death_timeline['episode'].astype(str)
death_timeline['eps_title'] = 'Eps ' + death_timeline['season_episode'] + ': ' + death_timeline['title']

# Tooltip information
death_timeline['tooltip'] = death_timeline.apply(
    lambda row: f"In Episode {row['season_episode']}, {row['name']} killed by {row['killer']}", axis=1
)

# Sort by season, episode, and t_start to ensure proper arrangement
death_timeline = death_timeline.sort_values(by=['season', 'episode', 't_start'])

# Assign evenly spaced jitter based on rank within the same episode
death_timeline['rank_within_eps'] = death_timeline.groupby(['season', 'episode']).cumcount()
death_timeline['jitter'] = death_timeline['rank_within_eps'] * 0.1  # Spacing of 0.1 between points

# Adjust season values by adding jitter to show multiple deaths in one episode
death_timeline['season_with_jitter'] = death_timeline['season'] + death_timeline['jitter']

# Create scatter plot
fig = px.scatter(
    death_timeline,
    x='eps_title',  # Episode title for x-axis
    y='season_with_jitter',  # Add jitter to avoid overlap in the same episode
    color='importance_score',  # Color by importance score
    hover_data={'tooltip': True},  # Tooltip for detailed information
    size=[10] * len(death_timeline),  # Uniform point size
    title="Death Timeline of Characters Across All Seasons",
    labels={'importance_score': 'Importance'},
    color_continuous_scale='YlOrRd',  # Color scale for importance
)

# Update hover template to display the tooltip content
fig.update_traces(
    hovertemplate="<br>".join([
        "%{customdata[0]}"
    ])
)

# Adjust the size of the dots
fig.update_traces(
    marker=dict(size=15)  # Adjust the size of the dots
)

# Update layout for better readability
fig.update_layout(
    xaxis_title="Episode: Title",
    yaxis_title="Season",
    legend_title="Importance",
    height=600,
    width=1200,  # Ensure there's enough space to visualize episodes
    template="plotly_white",
)

# Show the plot
fig.show()
