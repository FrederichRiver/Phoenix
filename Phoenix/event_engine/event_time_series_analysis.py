#!/usr/bin/python3

# stock data is a DataFrame with columns: date, open, high, low, close, volume
# stock data is sorted by date in ascending order
# stock data is indexed by date

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.finance as mpf
from scipy.fftpack import fft

# read in the data

df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

# using scipy to calculate the fft of df['close']

# This code takes the Fourier transform of the closing prices of a stock.
# The Fourier transform is used to analyze the frequency content of a signal.
# The function names are fft and df.

d2 = fft(df['close'])
# d2 is a complex array, we want the absolute value of the complex numbers
# q: method of complex calculation
# a: use np.absolute(d2)
# q: how to get the real part and the image part of the complex number?
# a: use d2.real and d2.imag

# q: how to get the frequency of the fft?
# a: the frequency is the index of the fft array
# q: how to associate the frequency with the time?
# a: the frequency is the number of cycles per unit time
# q: how to calculate the per unit time?
# a: the per unit time is the number of data points divided by the time span


# q: how to get the amplitude of the fft?
# a: the amplitude is the absolute value of the complex number
# q: how to get the phase of the fft?
# a: the phase is the angle of the complex number
# q: how to decrpyt the fft?
# a: the fft is a complex array, we want the absolute value of the complex numbers