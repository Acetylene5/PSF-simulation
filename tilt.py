import numpy as nu
import pyfits
import matplotlib.pyplot as plt

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

flat_beam = flat(200)

#adding a tilt to the wavefront (lowest order zernike polynomial?)

def tilt(wavefront, phase):
  wf = wavefront.copy()
  dphase = nu.arange(n)*phase/float(n)
  for a in range(len(wf)):
      wf[a,:] *= dphase[a]
  return wf

def tip(wavefront, phase):
  wf = wavefront.copy()
  dphase = nu.arange(n)*phase/float(n)
  for a in range(len(wf[0])):
      wf[:,a] *= dphase[a]
  return wf

phase = 1.0
tilted_beam = tilt(flat_beam, phase)
tipped_beam = tip(flat_beam, phase)
tiptilt = tip(tilted_beam, phase)

#taking the fft

airy_flat = nu.fft.fft2(flat_beam)
airy_tilt = nu.fft.fft2(tilted_beam)
airy_tip = nu.fft.fft2(tipped_beam)
airy_tiptilt = nu.fft.fft2(tiptilt)

psf_flat = nu.log10(nu.abs(airy_flat*nu.conj(airy_flat)))
psf_tilt = nu.log10(nu.abs(airy_tilt*nu.conj(airy_tilt)))
psf_tip = nu.log10(nu.abs(airy_tip*nu.conj(airy_tip)))
psf_tiptilt = nu.log10(nu.abs(airy_tiptilt*nu.conj(airy_tiptilt)))

#airy=nu.fft.fft2(tilt(400), s=None, axes=(0,1))

f1 = plt.figure(0)
f1.clear()
f2 = plt.figure(1)
f2.clear()

ax11 = f1.add_axes([0.1, 0.1, 0.4, 0.4])
ax12 = f1.add_axes([0.5, 0.5, 0.4, 0.4])
ax13 = f1.add_axes([0.1, 0.5, 0.4, 0.4])
ax14 = f1.add_axes([0.5, 0.1, 0.4, 0.4])
im11= ax11.imshow(nu.fft.fftshift(psf_flat))
im13= ax13.imshow(flat_beam)
im14= ax14.imshow(tilted_beam)
im12= ax12.imshow(nu.fft.fftshift(psf_tilt))

ax21 = f2.add_axes([0.1, 0.1, 0.4, 0.4])
ax22 = f2.add_axes([0.5, 0.5, 0.4, 0.4])
ax23 = f2.add_axes([0.1, 0.5, 0.4, 0.4])
ax24 = f2.add_axes([0.5, 0.1, 0.4, 0.4])
im21= ax21.imshow(nu.fft.fftshift(psf_tip))
im23= ax23.imshow(tipped_beam)
im24= ax24.imshow(tiptilt)
im22= ax22.imshow(nu.fft.fftshift(psf_tiptilt))
#seeing no result for different values of a1 : (

f1.show()
f2.show()
#fig.savefig("30,3,400.png")
