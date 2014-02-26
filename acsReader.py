import numpy
import scipy
import matplotlib.pyplot as pyplot
import pyfits

datadir = './Data/'
filename = 'PSF_bkgsub.asc'

def readData(datadir, filename):
    df = open(datadir+filename, 'r')
    frames = []
    frame = []
    flag = False
    for line in df:
        l = line.split()
        if len(l) > 0:
            if flag:
                row = numpy.fromstring(line, dtype=float, sep=' ')
                frame.append(row)
            else:
                if l[0] == 'Time':
                    flag = True
        else:
            if flag:
                flag = False
                frames.append(numpy.array(frame))
                frame = []
    return numpy.array(frames)

data = readData(datadir,filename)
stacked = numpy.average(data, axis=0)
noise = numpy.std(data, axis=0)

hdu = pyfits.PrimaryHDU(data)
hdulist = pyfits.HDUList([hdu])
hdulist.writeto("PSF_bkgsub.fits")


fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.imshow(stacked)
#ax.imshow(noise)
fig.show()
