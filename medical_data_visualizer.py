import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# Normalize data
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# Draw Categorical Plot
def draw_cat_plot():
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=[
        'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'])\
                   .size().reset_index(name='total')

    fig = sns.catplot(data=df_cat, x='variable', y='total', hue='value',
                      col='cardio', kind='bar').fig

    fig.savefig('catplot.png')
    return fig

# Draw Heat Map
def draw_heat_map():
    # Clean data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # Correlation matrix
    corr = df_heat.corr()

    # Generate mask
    mask = np.triu(corr)

    # Draw the heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f",
                center=0, linewidths=0.5, square=True, cbar_kws={"shrink": 0.5})

    fig.savefig('heatmap.png')
    return fig
if __name__ == '__main__':
    draw_cat_plot()
    draw_heat_map()