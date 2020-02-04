import numpy as np 
import matplotlib 

def running_mean(data, N):
    data = np.asarray(data)
    if N == 1:
        return data
    else:
        retArray = np.zeros(data.size)*np.nan
        padL = int(N/2)
        padR = N-padL-1
        retArray[padL:-padR] = np.convolve(data, np.ones((N,))/N, mode='valid')
        return retArray 

def get_color_value(value, minValue, maxValue):
    diff = maxValue-minValue
    cmap = matplotlib.cm.get_cmap('viridis')
    rgba = cmap((value-minValue)/diff)
    return rgba

def get_matlab_color(i):
    colors = np.asarray([ [0, 0.447000000000000, 0.741000000000000],
                          [0.850000000000000, 0.325000000000000, 0.098000000000000],
                          [0.929000000000000, 0.694000000000000, 0.125000000000000],
                          [0.494000000000000, 0.184000000000000, 0.556000000000000],
                          [0.466000000000000, 0.674000000000000, 0.188000000000000],
                          [0.301000000000000, 0.745000000000000, 0.933000000000000],
                          [0.635000000000000, 0.078000000000000, 0.184000000000000]])
    return colors[ i%len(colors) ]
