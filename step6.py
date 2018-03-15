import numpy as np
from utils import openImageFile, saveImageFile, applyOpening, applyClosing, applyGaussian, applySegmentation, applyOrientation, applyFrequency, applyGaborFilter, applySkeletonization
from skimage.morphology import skeletonize, disk
from skimage.util import invert

image = openImageFile('fingerprint.bmp')

image = applyClosing(image, disk(1))
image = applyOpening(image, disk(1))
image = applyGaussian(image)

# Assigned block size, which is divisive of 288 and 384
normImage, mask = applySegmentation(image, 12, 0.1)
orientImage = applyOrientation(normImage, 7, 1, 42, 7)
freqImage, meanFreq = applyFrequency(normImage, mask, orientImage, 24, 5, 5, 15)
gaborKernel, gaboredImage = applyGaborFilter(normImage, orientImage, meanFreq * mask, 0.5, 0.5)
thinnedImage = np.asarray(invert(skeletonize(gaboredImage)), dtype=int)
saveImageFile(thinnedImage, 'step6/skel.bmp')
