# import the necessary packages
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import csv
import os

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
	# show the images
	#plt.show()
	return m, s

def process_images(imageA_path, imageB_path):
	original = cv2.imread(imageA_path)
	map_test = cv2.imread(imageB_path)
	# convert the images to grayscale
	original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
	map_test = cv2.cvtColor(map_test, cv2.COLOR_BGR2GRAY)

	original = cv2.resize(original, (600,600))
	map_test = cv2.resize(map_test, (600,600))

	return original, map_test
 
# process the images -- the original, the original + contrast,
# and the original + photoshop

map1_dir = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map1"
map2_dir = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map2"
map3_dir = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map3"
map4_dir = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map4"
map5_dir = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map5"

image_stat_data = open('image_stat_data.csv', mode='w')
image_stat_data = csv.writer(image_stat_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

image_stat_data.writerow(["IMAGE", "MSE", "SSIM"])

# compare map 1 images
for image in os.listdir(map1_dir):
	image_test = os.path.join(map1_dir, image)
	image_real = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map1/map1_real.png"
	image_real, image_test = process_images(image_real, image_test)	# process images to compare them

	mse_val, ssim_val = compare_images(image_real, image_test, "Original vs. Test")
	# SAVE IN DATA
	print("MSE: " + str(mse_val))
	print("SSIM: " + str(ssim_val))


	# EXPORT DATA TO CSV
	image_stat_data.writerow([image, mse_val, ssim_val])

# compare map 2 images
for image in os.listdir(map2_dir):
	image_test = os.path.join(map2_dir, image)
	image_real = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map2/map2_real.png"
	image_real, image_test = process_images(image_real, image_test)	# process images to compare them

	mse_val, ssim_val = compare_images(image_real, image_test, "Original vs. Test")
	# SAVE IN DATA
	print("MSE: " + str(mse_val))
	print("SSIM: " + str(ssim_val))


	# EXPORT DATA TO CSV
	image_stat_data.writerow([image, mse_val, ssim_val])

# compare map 3 images
for image in os.listdir(map3_dir):
	image_test = os.path.join(map3_dir, image)
	image_real = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map3/map3_real.png"
	image_real, image_test = process_images(image_real, image_test)	# process images to compare them

	mse_val, ssim_val = compare_images(image_real, image_test, "Original vs. Test")
	# SAVE IN DATA
	print("MSE: " + str(mse_val))
	print("SSIM: " + str(ssim_val))


	# EXPORT DATA TO CSV
	image_stat_data.writerow([image, mse_val, ssim_val])

# compare map 4 images
for image in os.listdir(map4_dir):
	image_test = os.path.join(map4_dir, image)
	image_real = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map4/map4_real.png"
	image_real, image_test = process_images(image_real, image_test)	# process images to compare them

	mse_val, ssim_val = compare_images(image_real, image_test, "Original vs. Test")
	# SAVE IN DATA
	print("MSE: " + str(mse_val))
	print("SSIM: " + str(ssim_val))


	# EXPORT DATA TO CSV
	image_stat_data.writerow([image, mse_val, ssim_val])

# compare map 5 images
for image in os.listdir(map5_dir):
	image_test = os.path.join(map5_dir, image)
	image_real = "C:/Users/dmccl/OneDrive/Documents/SRI_bot/controllers/omni_controller_py/images/map5/map5_real.png"
	image_real, image_test = process_images(image_real, image_test)	# process images to compare them

	mse_val, ssim_val = compare_images(image_real, image_test, "Original vs. Test")
	# SAVE IN DATA
	print("MSE: " + str(mse_val))
	print("SSIM: " + str(ssim_val))


	# EXPORT DATA TO CSV
	image_stat_data.writerow([image, mse_val, ssim_val])

