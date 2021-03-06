# AUTOGENERATED! DO NOT EDIT! File to edit: 01_timeseries.ipynb (unless otherwise specified).

__all__ = ['factory_atype', 'moving_average', 'moving_average_score', 'twitter', 'twitter_score']

# Cell
import numpy as np
import pandas as pd

from .stats import MAD, Tukey #, ESD

# Cell
def factory_atype(atype='mad'):
    if atype == 'mad':
        return MAD()
    elif atype == 'tukey':
        return Tukey
    else:
        raise ValueError('Algoritmo de detecção de anomalia não implementado - \"{}\"'.format(atype))

# Cell
def moving_average(ts, window=12, atype='mad'):
    '''
    Detecção de anomalias com base no Moving Average da serie tempora(ts).
    ts = numpy array      - serie temporal
    window_size = [2..n]  - Tamanho da janela
    atype = ['mad', 'tukey'] - algoritmo para detecção de anomalias'''
    ts_ma = pd.Series(ts).rolling(window).mean()
    m = factory_atype(atype)
    m.fit(ts_ma)
    return m.predict(ts_ma)

# Cell
def moving_average_score(ts, window=12,  atype='mad'):
    '''
    Detecção de anomalias com base no Moving Average da serie tempora(ts).
    ts = numpy array      - serie temporal
    window_size = [2..n]  - Tamanho da janela
    atype = ['mad', 'tukey'] - algoritmo para detecção de anomalias'''
    ts_ma = pd.Series(ts).rolling(window).mean()
    m = factory_atype(atype)
    m.fit(ts_ma)
    return m.decision_function(ts_ma)

# Cell
from statsmodels.tsa.seasonal import STL

def twitter(x, period=None, seasonal=45):
    '''
        Retorna os index dos valores que são anomalias
        input precisa ser um Serie com DateTimeIndex'''
    # filtrando o componente seasonal
    if period is not None:
        stl = STL(x, period=period, seasonal=seasonal)
    else:
        stl = STL(x, seasonal=seasonal)

    res = stl.fit()
    # calculamos o residuo
    residuo = x - np.nanmedian(x) - res.seasonal
    # Procuramos outliers com MAD
    mad = MAD()
    mad.fit(residuo)
    index = mad.predict(residuo).index
    return x.loc[index]

# Cell
from statsmodels.tsa.seasonal import STL

def twitter_score(x, period=None, seasonal=45):
    '''
        Retorna os index dos valores que são anomalias
        input precisa ser um Serie com index temporal'''
    # filtrando o componente seasonal
    if period is not None:
        stl = STL(x, period=period, seasonal=seasonal)
    else:
        stl = STL(x, seasonal=seasonal)
    res = stl.fit()
    # calculamos o residuo
    residuo = x - np.nanmedian(x) - res.seasonal
    # Procuramos outliers com MAD
    mad = MAD()
    mad.fit(residuo)
    return mad.decision_function(residuo)