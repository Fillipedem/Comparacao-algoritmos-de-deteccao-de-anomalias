import numpy as np
from sklearn.metrics import precision_score
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

###                 ###
### Plot Anomalias  ###
###                 ###
def plot_anomalies(ts, windows=None, figsize=(20, 5)):
    ''' Plota a serie temporal **ts** e a respectiva
        região de anomalia **windows**'''
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    sns.lineplot(x=ts.index, y=ts, ax=ax)
    
    # plot anomaly window
    if windows is not None:
        for idx, window in windows.iterrows():
            xlim = ax.get_xlim()
            ax.axvspan(window['start'], window['end'], color='#EF9A9A', alpha=0.5)
        
    return fig, ax


###                                       ###
### Precision-Recall Curve helper methods ###
###                                       ###
def precision(X):
    ''' calcula a precision@k para todos os valores de X
        input: [1, 1, 0, 0]
        output: [1, 1, 0.66, 0.5]'''
    ans = np.zeros(len(X))
    for idx,x in enumerate(X):
        ans[idx] = precision_score(X[:idx + 1], np.ones(idx + 1))
    return ans


def top_k_precision(score, labels, k=5):
    ''' 
        input: 
            - score: Series, com DateTimeIndex
            - labels: DataFrame, seguindo o padrão da classe Dataset
        output:
            Acuracia dos top k scores:
              - 1 se o exemplo está dentro da janela de anomalia
              - 0 se o exemplo está fora da janela de anomalia'''
    ans = np.zeros(k)
    sorted_score = score.sort_values(ascending=False)
    used_labels = [False]*labels.shape[0]
    count = 0              
    # para cada exemplo checamos se a detecção
    # está dentro de uma janale de anomalia definida em labels    
    for timestamp in sorted_score.index:
        if count >= k:
            break
        
        # para cada janela de anomalia conhecida
        for label_idx, label in labels.iterrows():
            # checa se o o instante da detecção está dentro
            # da janela de anomalia
            if timestamp >= label['start'] and timestamp <= label['end']:
                if used_labels[label_idx]: 
                    count -= 1
                else:
                    ans[count] = 1
                    used_labels[label_idx] = True
                break
                  
        count += 1
            
    return precision(ans)


def plot_precision_recall_curve(df, figsize=(10, 5)):
    ''' plot precision recall curve '''
    df = df.copy()
    df.index=df.index/len(df.index) # recall index
    
    # plot
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    sns.lineplot(data=df, ax=ax)
        
    plt.title('Precision-Recall Curve', fontsize=20)
    plt.xlabel('Recall', fontsize=15)
    plt.ylabel('Precision', fontsize=15)
    
    return fig, ax