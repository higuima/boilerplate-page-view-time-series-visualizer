import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from calendar import month_name
from IPython.display import display
import matplotlib.ticker as mticker


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('freeCodeCamp/Page-View-Time-Series-Visualizer/fcc-forum-pageviews.csv')
df["date"] = pd.to_datetime(df["date"])
df = df.set_index('date')
# Clean data
df = df.loc[(df['value'] > df['value'].quantile(0.025)) & (df['value']< df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5))
    
    sns.lineplot(data=df, legend=False, palette=['r']).set(title = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019',xlabel = 'Date', ylabel = 'Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['months'] = df.index.strftime('%B')
    df_bar['years'] = df.index.strftime('%Y')
    df_bar = pd.DataFrame(df_bar.groupby(['years','months'],sort=False)['value'].mean().round().astype(int))
    df_bar = df_bar.reset_index()
    months_2016 = {
        'years': ['2016', '2016', '2016', '2016'],
        'months': ['January', 'February', 'March', 'April'],
        'value': [0, 0, 0, 0]
    }
    new_df = pd.concat([pd.DataFrame(months_2016), df_bar]).reset_index(drop=True)

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(7,6))

    new_df = new_df.rename(columns={'value' : 'Average Page Views', 'years':'Years', 'months': 'Months'})
    bar_graph = sns.barplot(data=new_df, x='Years', y='Average Page Views', hue='Months', palette='tab10')
    bar_graph.set_xticklabels(bar_graph.get_xticklabels(), rotation=90, horizontalalignment='center')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2,figsize=(16,6))

    sns.boxplot(data=df_box, x='year',y='value', ax=ax[0]).set(xlabel ='Year', ylabel = 'Page Views', title ='Year-wise Box Plot (Trend)',ylim=(0,200000))

    sns.boxplot(data=df_box, x='month',y='value',ax=ax[1],order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']).set(xlabel ='Month', ylabel = 'Page Views', title ='Month-wise Box Plot (Seasonality)',ylim=(0,200000))

    # Save image and return fig (don't change this part)
    y_ticks = ['0', '20000', '40000', '60000', '80000', '100000', '120000', '140000', '160000', '180000', '200000']
    ax[0].yaxis.set_major_locator(mticker.FixedLocator([int(s) for s in y_ticks]))
    ax[0].set_yticklabels(y_ticks)
    ax[1].yaxis.set_major_locator(mticker.FixedLocator([int(s) for s in y_ticks]))
    ax[1].set_yticklabels(y_ticks)
    fig.savefig('box_plot.png')
    return fig
