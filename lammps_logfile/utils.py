import numpy as np 
import matplotlib 

def running_mean(data, N):
    """Calculate running mean of an array-like dataset.

    Parameters
    ----------
    data : array_like
        The array.
    N : int
        Width of the averaging window.

    Returns
    -------
    numpy.ndarray
        The running mean of the input data.

    """
    
    data = np.asarray(data)
    if N == 1:
        return data
    else:
        retArray = np.zeros(data.size)*np.nan
        padL = int(N/2)
        padR = N-padL-1
        retArray[padL:-padR] = np.convolve(data, np.ones((N,))/N, mode='valid')
        return retArray 

def get_color_value(value, minValue, maxValue, cmap='viridis'):
    """Get color from colormap.

    Parameters
    ----------
    value : float
        Value used to get color from colormap.
    minValue : float
        Minimum value in colormap. Values below this value will saturate on the lower color of the colormap.
    maxValue : float
        Maximum value in colormap. Values above this value will saturate on the upper color of the colormap.
    cmap : str, optional
        Name of the colormap to use. Default is 'viridis'.

    Returns
    -------
    tuple
        4-vector containing colormap values.

    Notes
    -----
    This is useful if you are plotting data from several simulations, and want to color them based on some parameters changing between the simulations. For example, you may want the color to gradually change along a colormap as the temperature increases.

    """
    diff = maxValue-minValue
    cmap = matplotlib.cm.get_cmap(cmap)
    rgba = cmap((value-minValue)/diff)
    return rgba

def get_matlab_color(i):
    """Get colors from matlabs standard color order. 

    Parameters
    ----------
    i : int
        Index. Cycles with a period of 7, so calling with 1 returns the same color as calling with 8.

    Returns
    -------
    numpy.ndarray
        Color as 3-vector.

    """
    colors = np.asarray([ [0, 0.447000000000000, 0.741000000000000],
                          [0.850000000000000, 0.325000000000000, 0.098000000000000],
                          [0.929000000000000, 0.694000000000000, 0.125000000000000],
                          [0.494000000000000, 0.184000000000000, 0.556000000000000],
                          [0.466000000000000, 0.674000000000000, 0.188000000000000],
                          [0.301000000000000, 0.745000000000000, 0.933000000000000],
                          [0.635000000000000, 0.078000000000000, 0.184000000000000]])
    return colors[ i%len(colors) ]
