"""
Simple example of pulling Billboard chart data. The documentation at
https://github.com/guoguo12/billboard-charts is excellent; check it out! 
Run as 'python billboardExample.py' in the Terminal. 

"""

from billboard import ChartData
import pdb
import numpy as np 

chartname = 'hot-100'
date = '2015-11-28'
data = ChartData(chartname, date = date)

previous = data.previousDate
data2 = ChartData(chartname, date = previous)

#print title of each track 
print [x.title for x in data]

#this also prints the spotifyID, making things very easy!!!!
print [x.spotifyID for x in data]

#write to a csv file 
f = open('billboard_data.csv', 'wb')
[f.write(x.spotifyID + '\t' + x.title + '\t'  + x.artist + '\t' + np.str(x.peakPos) + '\t' + 
    np.str(x.lastPos) + '\t' + np.str(x.weeks) + '\t' + np.str(x.rank) + '\t'  + np.str(x.change)
    + '\t' + x.spotifyLink + '\n')
    for x in data]
f.close()
    