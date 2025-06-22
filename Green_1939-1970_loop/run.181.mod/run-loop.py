#! /home/awickert/anaconda3/envs/dakota-env/bin/python

"""
This is meant as a schematic example, using data from the Minnesota River at
Jordan (MN) stream gauge. Parameters are not calibrated to data, and are not
intended to fit real river-width measurements.
"""

import ottar

rw = ottar.RiverWidth.from_yaml('config-loop.yaml')

rw.initialize()
rw.run()
rw.finalize()

# Now, plot statistics, starting with 2032-01-02, which is the start of the
# fourth cycle, and when the result looks to have equilibrated

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

plt.ion()

# Shear stress
df = rw.df.copy()
Rh = df['Water depth [m]'] * df['Channel width [m]'] / \
        ( 2*df['Water depth [m]'] + df['Channel width [m]'] )
df['tau_b [Pa]'] = rw.rho * rw.g * Rh * rw.S
# Hm, but not giving changes in bf: depth constant

# Conveyance capacity
df['Q_bf [m^3/s]'] = 1./rw.channel_n * rw.h_banks**(5/3.) \
                                     * df['Channel width [m]'] \
                                     * rw.S**(1/2.)

# Clip series to equilibrium section
#df = df[ df['Timestamp'] >= pd.to_datetime('2032-01-02') ]
# More stringently
df = df[ df['Timestamp'] >= pd.to_datetime('2063-01-02') ]


# 1.5-year flood (and 1 and 2)
_Q = sorted( df['Q_bf [m^3/s]'] )
_rank_1p5 = int( round( len(_Q) + 1 ) / np.round( 365 * 1.5 ) )  
Q1p5 = _Q[-_rank_1p5]

_rank_1 = int( round( len(_Q) + 1 ) / np.round( 365 ) )  
Q1 = _Q[-_rank_1]

_rank_2 = int( round( len(_Q) + 1 ) / np.round( 365*2 ) )  
Q2 = _Q[-_rank_2]


# What RI flood does the channel hold?

def RI_days(Q):
    _tmp = np.abs( np.array(_Q) - Q)
    _tmp == np.min(_tmp)
    rank = len(_tmp) - (_tmp == np.min(_tmp)).nonzero()[0][0]
    RI = (len(_tmp) + 1) / rank
    # RI_years = RI / 365.25
    return RI

print( RI_days( np.min( df['Q_bf [m^3/s]'] ) ), ' days')
print( RI_days( np.mean( df['Q_bf [m^3/s]'] ) ), ' days')
print( RI_days( np.max( df['Q_bf [m^3/s]'] ) )/365.25, ' years')

print( np.percentile( df['Q_bf [m^3/s]'], 5 ), )
print( RI_days( np.percentile( df['Q_bf [m^3/s]'], 5 ) ), ' days, 5th %ile')
print( np.percentile( df['Q_bf [m^3/s]'], 50 ), )
print( RI_days( np.percentile( df['Q_bf [m^3/s]'], 50 ) ), ' days, 50th %ile')
print( np.percentile( df['Q_bf [m^3/s]'], 95 ), )
print( RI_days( np.percentile( df['Q_bf [m^3/s]'], 95 ) ), ' days, 95th %ile')

# Flow above and below the mean

plt.hist( df['Channel width [m]'], 100 )

# Variance about mean: 9.3%
( np.max(df['Channel width [m]']) - np.min(df['Channel width [m]']) ) / \
np.mean(df['Channel width [m]'])


# Patterns in this variance
from scipy import fft
sig = np.array(df['Channel width [m]'])
fourier = fft.rfft( sig )

# Get the frequency components of the spectrum
sampling_rate = 365.25 # days in year -- sample spacing
frequency_axis = fft.rfftfreq( len(sig), d=1.0/sampling_rate )
_normalize = len(sig)/2
norm_amplitude = np.abs(fourier)/_normalize

# Plot the results
plt.plot(frequency_axis, norm_amplitude)
plt.xlabel('Frequency [1/year]')
plt.ylabel('Amplitude')
plt.title('Spectrum')
plt.show()

# Period axis
period_axis = 1/frequency_axis
# Remove the DC
period_axis = period_axis[1:]
nap = norm_amplitude[1:]

plt.loglog(period_axis, nap)
plt.xlabel('Period [year]')
plt.ylabel('Amplitude')
plt.xlim( plt.xlim()[::-1] )
plt.title('Spectrum')
plt.show()

"""
_index = int( np.round( 365 * 1.5 ) )


Q1p5 = (len(_Q) + 1) / _Q[_index]

# Shields stress

df = rw.df[ rw.df['Timestamp'] >= pd.to_datetime('2032-01-02') ]
"""

