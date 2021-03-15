# -*- coding: utf-8 -*-
"""PSET1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F-U9rF63XlNN3l69N88Iw4vLlI09XkDf
"""

from google.colab import drive
drive.mount('/content/drive')

"""# PSET 1

These are some of the libraries/modules you will require for this homework.
"""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import copy
import os

path = '/content/drive/MyDrive/Colab Notebooks/CS188cv/homework 1/Data'

"""These are some functions which will be useful throught the homework to (1) display a single grayscale image, (2) display multiple images using subplots, (3) computing the relative absolute distance between two images."""

def display_gray(x: np.array, normalized:bool = False):
    if not normalized:
        plt.imshow(x,cmap='gray',vmin=0,vmax=1)
    else:
        plt.imshow(x/x.max(),cmap='gray',vmin=0,vmax=1)

def display_axis(ax: plt.axis, x: np.array, title: str, normalized:bool = False):
    if not normalized:
        ax.imshow(x,cmap='gray',vmin=0,vmax=1)
    else:
        ax.imshow(x/x.max(),cmap='gray',vmin=0,vmax=1)
    ax.set_title(title,size=18)

def rel_l1_dist(x1: np.array, x2: np.array):
    return np.abs(x1-x2).sum()/np.abs(x1).sum()

"""Load the house image from `Data/Singles` using Pillow (PIL) into a 2D-array `img_data`. Normalize the image by dividing it with 255. """

image = Image.open(os.path.join(path,'Singles/house.png'))
img_data = np.asarray(image)/255

"""Display the image using `display_gray` defined above."""

display_gray(img_data)

"""Print the size of the image"""

print(f'Image size: {img_data.shape[0]}x{img_data.shape[1]}')

"""# Question 2

### 2D-Convolution

Here you will be implementing the 2D convolution operation using `for` loops. You have to complete the function `conv2D(image, kernel)`.  

For this homework assume that you are given a grayscale `image` (house) and you want to convolve it with a `kernel` (for example, identity, average or gaussian) such that the output image has the same size as the input `image` (you will need to zero pad the `image` appropriately on all the sides before performing the convolution). The function should return convolution of `image` and `kernel`. 

*Note:* The origin of the kernel should be the center pixel of the filter, while the origin for the image should be the top left pixel of the image before zero padding. For this homework we will assume that all the filters are `square` and `odd-sized`.

### **Answer 2:**

Copy paste your solution in the cell below on overleaf for Question 2.
"""

# Write your answer in this cell. Then copy paste the code into the overleaf file corresponding to Question 2.
def conv2D(image: np.array, kernel: np.array = None) -> np.array:
  # get the shape of the kernel
  krow, kcol = kernel.shape
  assert(krow == kcol)

  # get shape of image
  irow, icol = image.shape

  # pad the image
  pad_image = np.pad(image, krow//2, mode='constant')

  # make output image
  out = np.zeros(image.shape)

  # flip the kernel
  flipped_kernel = np.flipud(np.fliplr(kernel))

  # loop through and compute the convolution
  for i in range(irow):
    for j in range(icol):
      # dot product between kernel and sub image
      out[i][j] = np.sum(pad_image[i:i+krow,j:j+krow] * flipped_kernel)
  return out

"""One easy way to verify the correctness of the implementation is to make sure that convolving with an identity filter returns the same image. Make sure that you dont get an assertion error."""

def identity_filter(size: int):
    assert size%2 == 1
    iden_filt = np.zeros((size,size))
    iden_filt[size//2,size//2]=1
    return iden_filt

iden_filt = identity_filter(5)
conv_iden = conv2D(img_data, iden_filt)
assert np.abs(img_data-conv_iden).sum() == 0.0

"""# Question 3

### Image Blurring and Denoising

In this question you will be using convolution to perform image blurring and denoising.

Average/Box Filter: This is the standard box filter which computes the mean of all the pixels inside the filter.
"""

def average_filter(size: int):
    assert size%2 == 1
    return 1.0 * np.ones((size,size))/(size**2)

"""## (1) 

### Gaussian Filter

The formula for the distribution of a 2-D isotropic gaussian distribution with variance $\sigma^2$ and mean $= [\mu_x, \mu_y]$ is given by

$p(x,y) = \dfrac{1}{2\pi\sigma^2}\exp{\big(-\dfrac{(x-\mu_x)^2+(y-\mu_y)^2}{2\sigma^2}\big)}$

Using the equation above, complete the function `gaussian_filter(size, sigma)` which given a filter size and standard deviation, returns a centered gaussian filter. Unlike the usual 2-D gaussian which is defined on a continuous space, for the gaussian filter you will assume that $x,y,\mu_x,\mu_y$ are discrete integers.

*Note:* Don't forget to normalize the filter to make sure that it sums to 1.

### **Answer 3.1:**
Copy paste your solution in the cell below on overleaf for Question 3.1.
"""

# Write your answer in this cell.

def gaussian_filter(size: int, sigma: float):
  assert size%2 == 1
  const_a =  1 / (2 * np.pi * sigma ** 2)
  mean = size // 2
  filt = [[
          const_a * \
          np.exp( -1*((x - mean)**2 + (y - mean)**2)/(2 * sigma ** 2))
          for x in range(size)] for y in range(size)]
  filt /= np.sum(filt)
  return filt

"""## (2)

### **Answer 3.2:**

Execute the cell below and copy the saved image on overleaf for Question 3.2.
"""

fig, ax = plt.subplots(1,4,figsize=(1 + 4*4.5,4))
for i in range(1,5):
    gauss_filt = gaussian_filter(21,i)
    display_axis(ax[i-1],gauss_filt,f'\u03C3={i}', normalized=True)
fig.tight_layout()
fig.savefig(path+'/Solutions/question_3_2.pdf', format='pdf', bbox_inches='tight')

"""### Image Blurring

In this sub-part you will see that the average and gaussian filter defined above can be used for image blurring. If your implementation of Conv2D and gaussian filter is correct then you should observe that increasing the filter size for the average filter and the filter size/variance for the gaussian filter will increase the blurring. So the images on the right will be more blurred.

#### Average Filter
"""

fig, ax = plt.subplots(1,4,figsize=(1 + 4*4.5,4))
for i in range(1,5):
    size = 4*i+1
    avg_filt = average_filter(size)
    conv_avg = conv2D(img_data, avg_filt)
    display_axis(ax[i-1],conv_avg,f'Kernel Size={size}')

"""## (3)
#### Gaussian Filter

### **Answer 3.3:**

Execute the cell below and copy the saved image on overleaf for Question 3.3.
"""

fig, ax = plt.subplots(2,4,figsize=(1 + 4*4.5,2*4))
for i in range(1,5):
    sigma = 4*(i-1)+1
    s = 4*i + 1
    gauss_filt = gaussian_filter(21,sigma)
    conv_gauss = conv2D(img_data, gauss_filt)
    display_axis(ax[0,i-1],conv_gauss,f'\u03C3={sigma}')
    gauss_filt = gaussian_filter(s,5)
    conv_gauss = conv2D(img_data, gauss_filt)
    display_axis(ax[1,i-1],conv_gauss,f'Kernel Size={s}')
fig.tight_layout()
fig.savefig(path+'/Solutions/question_3_3.pdf', format='pdf', bbox_inches='tight')

"""## Image Denoising

In this question you will use `conv2D` to perform image denoising. You will use three types of filtering for denoising: (i) average, (ii) gaussian and (iii) median. Average and Gaussian filtering can easily be performed using the current implementation of the `conv2D` function. However, the median filter cannot be characterized using a known filter unlike average, gaussian. You will write a function for performing median filtering.

You will perform all the three types of filtering and report best filtering method (you may find the `rel_abs_dist` function useful for this part.

Display the noisy image
"""

noisy_img_data = np.asarray(Image.open(path + '/Singles/noisy_house.png'))
noisy_img_data = noisy_img_data/255
display_gray(noisy_img_data)

"""## (5) 
### Median filtering

Complete the function `median_filtering(image, kernel_size)` which takes the `image` as input along with the `kernel_size` and returns the median filtered output which has the same size as the input image (you need to perform zero padding).

### **Answer 3.5:**
Copy paste your solution in the cell below on overleaf for Question 3.5.
"""

# Write your answer in this cell. Then copy paste the code into the overleaf file corresponding to Question 3 (d).

def median_filtering(image: np.array, kernel_size: int = None):
  assert kernel_size%2 == 1

  # get shape of image
  irow, icol = image.shape

  # pad the image
  pad = kernel_size//2
  pad_image = np.pad(image, pad, mode='constant')

  # make output image
  out = np.zeros_like(image)

  # loop through and compute the convolution
  for i in range(irow):
    for j in range(icol):
      # dot product between kernel and sub image
      out[i][j] = np.median(pad_image[i:i+kernel_size,j:j+kernel_size])

  return out

"""Perform the 3 types of filtering."""

noisy_img_data_1 = noisy_img_data.copy()
avg_filt = average_filter(7)
gauss_filt = gaussian_filter(7,3)
avg_filt_noisy_img = conv2D(noisy_img_data_1, avg_filt)
gauss_filt_noisy_img = conv2D(noisy_img_data_1, gauss_filt)
median_filt_noisy_img = median_filtering(noisy_img_data,7)

"""Display all the images.

### **Answer 3.6:**

Execute the cell below and copy the saved image on overleaf for Question 3.6.
"""

fig, ax = plt.subplots(1,5,figsize=(1 + 5*4.5,4))
display_axis(ax[0],noisy_img_data, 'Noisy Image')
display_axis(ax[1],img_data, 'Noiseless Image')
display_axis(ax[2],avg_filt_noisy_img,'Average Filtering')
display_axis(ax[3],gauss_filt_noisy_img,'Gaussian Filtering')
display_axis(ax[4],median_filt_noisy_img,'Median Filtering')
fig.tight_layout()
fig.savefig(path+'/Solutions/question_3_6.pdf', format='pdf', bbox_inches='tight')

"""Relative absolute distance"""

print(f'Average Filtering: {rel_l1_dist(img_data, avg_filt_noisy_img)}')
print(f'Gaussian Filtering: {rel_l1_dist(img_data, gauss_filt_noisy_img)}')
print(f'Median Filtering: {rel_l1_dist(img_data, median_filt_noisy_img)}')

"""## Question 4

## Gradients

In this question you will be using convolution, `conv2D` to compute image gradients. Gradients are useful in obtaining the edges in an image. Multiple edge level features can be combined to obtain higher level features which are useful in image classification. 

Design a filter to compute the gradient along the horizontal and vertical direction. After convolving with a filter which computes the gradient along the horizontal direction you should observe that all the vertical edges in the filtered image and vice-versa. 

*Hint:* See Prewitt filter

## (1)

Design a filter `gradient_x` for computing the horizontal gradient (along the x direction) using `conv2D`.

### **Answer 4.1:**
Copy paste your solution in the cell below on overleaf for Question 4.1.
"""

# Write your code in this cell.
gradient_x = np.array([[1,0,-1],
                       [1,0,-1],
                       [1,0,-1]])

"""## (2)

Design a filter `gradient_y` for computing the vertical gradient (along the y direction) using `conv2D`.

### **Answer 4.2:**
Copy paste your solution in the cell below on overleaf for Question 4.2.
"""

# Write your code in this cell.
gradient_y = np.array([[1,1,1],
                       [0,0,0],
                       [-1,-1,-1]])

"""Display the absolute gradient along the horizontal, vertical directions and their sum. You should observe that the gradient in the horizontal (x-direction) is unable to capture the horizontal parts of the rooftops, while the vertical gradient is unable to captures features like the edges of chimney.

### **Answer 4.3:**

Execute the cell below and copy the saved image on overleaf for Question 4.3.
"""

fig, ax = plt.subplots(1,3,figsize=(1 + 3*4.5,4))
img_gradient_x = conv2D(img_data, gradient_x)
img_gradient_y = conv2D(img_data, gradient_y)
display_axis(ax[0], np.abs(img_gradient_x), 'Gradient-X')
display_axis(ax[1], np.abs(img_gradient_y), 'Gradient-Y')
display_axis(ax[2], np.abs(img_gradient_x) + np.abs(img_gradient_y), 'Gradient-Sum')
fig.tight_layout()
fig.savefig(path+'/Solutions/question_4_3.pdf', format='pdf', bbox_inches='tight')

"""## Question 5

### Image Filtering

In this question you will be completing a function `filtering_2(image, kernel, sigma_int, norm_fac)` which takes as input the `image`, a gaussian filter `kernel` which is the filter for the spatial dimension, `sigma_int` is the standard deviation of the gaussian along the intensity/pixel dimension and `norm_fac` is the normalization factor.

*Note:* For this filter you have two types of gaussian filters (one along the spatial dimension and the other along the pixel dimension). The gaussian filter along the spatial dimension is 2-D can be obtained using the `gaussian_filter` function you wrote previously, however, the gaussian filter along the intensity dimension is 1-D and non-linear filter.

### **Answer 5.5:**
Copy paste your solution in the cell below on overleaf for Question 5.5.
"""

def filtering_2(image: np.array, kernel: np.array = None, sigma_int: float = None, norm_fac: float = None):
    # get the shape of the image and kernel
    krow, kcol = kernel.shape
    irow, icol  = image.shape[0], image.shape[1]

    assert krow%2 == 1
    assert krow==kcol

	# define Gaussian helper
    def gaussian(x):
        a = 2 * np.pi * sigma_int**2
        a = np.sqrt(a)
        a = 1 / a
        b = -1 * (x - sigma_int)**2 / (2*sigma_int**2)
        b = np.exp(b)
        return a * b

    # pad the image
    pad = krow // 2
    pad_img = np.pad(image, pad,'constant')

    # create output image
    out = np.zeros_like(image)
    for i in range(irow):
        for j in range(icol):
            # create intensity filter to compare p and q
            gaussian_weight = pad_img[i:i+krow, j:j+krow] - pad_img[i+pad, j+pad]
            gaussian_weight = np.abs(gaussian_weight)
            filt = gaussian(gaussian_weight) * kernel

            # dot product between sub image and filter
            out[i][j] = np.sum(pad_img[i:i+krow, j:j+krow] * filt)

            # normalize pixel
            out[i][j] /= np.sum(filt)

    out /= 255
    out /= norm_fac
    return out

gauss_filt = gaussian_filter(11,3)
gauss_filt_img_data = conv2D(img_data, gauss_filt)
# filt_2_img_data = filtering_2(img_data, gauss_filt, sigma_int=0.2, norm_fac=0.0075) #These are some reference values, feel free to tune the values.
filt_2_img_data = filtering_2(img_data, gauss_filt, sigma_int=0.04, norm_fac=0.004)

"""Comparison of the new filter with the gaussian filter should show that the new filter preserves edges while smoothing the remaining image.

### **Answer 5.6:**

Execute the cell below and copy the saved image on overleaf for Question 5.6.
"""

fig, ax = plt.subplots(1,3,figsize=(1 + 3*4.5,4))
display_axis(ax[0], img_data, 'Original Image')
display_axis(ax[1], gauss_filt_img_data, 'Gaussian Filtering')
display_axis(ax[2], filt_2_img_data, 'Filtering 2')
fig.tight_layout()
fig.savefig(path+'/Solutions/question_5_6.pdf', format='pdf', bbox_inches='tight')

from PIL import ImageOps

image = Image.open(os.path.join(path,'Singles/boys.png'))

x = ImageOps.grayscale(image)

boys = np.asarray(x)/255

a = boys
orig = boys
s = np.array(
    [
     [-1,-1,-1],
     [-1,9,-1],
     [-1,-1,-1]
    ]
)
med_val = 3
# avg_val = 11
gaus_ker = 3
gaus_sig = .1
bilat_sig = 0.04
bilat_norm = 0.004

g = gaussian_filter(gaus_ker,gaus_sig)
# avg = average_filter(avg_val)
# gx = conv2D(a, gradient_x)
# gy = conv2D(a, gradient_y)

bilatg = filtering_2(a, g, sigma_int=bilat_sig, norm_fac=bilat_norm)
# bilata = filtering_2(a, avg, sigma_int=bilat_sig, norm_fac=bilat_norm)
median = median_filtering(a, med_val)
# gxy = gx + gy
# sharp = conv2D(a,s)

# title = "bilatg(median)"
display_gray(filtering_2(median, g, sigma_int=bilat_sig, norm_fac=bilat_norm))

# fig, ax = plt.subplots(3,5,figsize=(70,30))

# display_axis(ax[0][0], orig, "orignal")
# display_axis(ax[0][1], bilatg, "bilatg")
# display_axis(ax[0][2], median, "median")
# display_axis(ax[0][3], gxy, "grad")
# display_axis(ax[0][4], sharp, "sharp")

# display_axis(ax[1][0], bilatg, "bilatg")
# display_axis(ax[1][1], bilata, "bilata")
# display_axis(ax[1][2], filtering_2(sharp, g, sigma_int=bilat_sig, norm_fac=bilat_norm), "bilatg(sharp)")
# display_axis(ax[1][3], filtering_2(median, g, sigma_int=bilat_sig, norm_fac=bilat_norm), "bilatg(median)")
# display_axis(ax[1][4], a, "a")

# display_axis(ax[2][0], a, "a")
# display_axis(ax[2][1], a, "a")
# display_axis(ax[2][2], a, "a")
# display_axis(ax[2][3], a, "a")
# display_axis(ax[2][4], a, "a")