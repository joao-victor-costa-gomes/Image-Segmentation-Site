from segmentation.thresholding.fixed_threshold import fixed_threshold
from segmentation.thresholding.otsu_threshold import otsu_threshold
from segmentation.thresholding.adaptative_threshold import adaptive_threshold

# Image path
image_path = 'image.jpg'

# Call each function
print("Applying Fixed Threshold...")
fixed_threshold(image_path)

print("Applying Adaptive Threshold...")
adaptive_threshold(image_path)

print("Applying Otsu Threshold...")
otsu_threshold(image_path)
