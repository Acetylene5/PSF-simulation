import numpy as nu
import pyfits
import matplotlib.pyplot as plt

fig = plt.figure(0)
fig.clear()

#creating a circular wavefront

# Better to have a well-sampled beam -> large N
n=1000


def flat(radius):
  """ Creates a flat beam of a given radius """
  wavefront=nu.zeros([n,n], dtype=nu.float32)

  xcent = n/2.0
  ycent = n/2.0

  for a in range(0,n):
    for b in range(0,n):
       if ((a-xcent)**2+(b-ycent)**2)<=((radius)**2):
          wavefront[a,b]=1.0
  return wavefront

flat_beam = flat(90)

#adding a tilt to the wavefront (lowest order zernike polynomial?)

def tilt(wavefront, phase):
  wf = wavefront.copy()
  dphase = nu.arange(n)*phase/float(n)
  for a in range(len(wf)):
      wf[a,:] *= dphase[a]
  return wf

phase = 1.0
tilted_beam = tilt(flat_beam, phase)

#taking the fft

airy_flat = nu.fft.fft2(flat_beam)
airy_tilt = nu.fft.fft2(tilted_beam)

psf_flat = nu.log10(nu.abs(airy_flat*nu.conj(airy_flat)))
psf_tilt = nu.log10(nu.abs(airy_tilt*nu.conj(airy_tilt)))

#airy=nu.fft.fft2(tilt(400), s=None, axes=(0,1))

ax1 = fig.add_axes([0.1, 0.1, 0.4, 0.4])
ax2 = fig.add_axes([0.5, 0.5, 0.4, 0.4])
ax3 = fig.add_axes([0.1, 0.5, 0.4, 0.4])
ax4 = fig.add_axes([0.5, 0.1, 0.4, 0.4])
im1= ax1.imshow(nu.fft.fftshift(psf_flat))
im3= ax3.imshow(flat_beam)
im4= ax4.imshow(tilted_beam)
im2= ax2.imshow(nu.fft.fftshift(psf_tilt))

#seeing no result for different values of a1 : (

fig.show()
#fig.savefig("30,3,400.png")
