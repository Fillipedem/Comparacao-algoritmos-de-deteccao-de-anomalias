import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

def plot_anomalies(ts, windows=None, figsize=(20, 5)):
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    sns.lineplot(x=ts.index, y=ts, ax=ax)
    
    # plot anomaly window
    if windows is not None:
        for idx, window in windows.iterrows():
            xlim = ax.get_xlim()
            ax.axvspan(window['start'], window['end'], color='#EF9A9A', alpha=0.5)
        
    return fig, ax