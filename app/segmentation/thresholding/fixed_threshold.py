import cv2

def fixed_threshold(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded correctly
    if image is None:
        print("Error loading the image.")
        return

    # Fixed thresholding
    _, fixed_threshold_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Display the results
    cv2.imshow('Original', image)
    cv2.imshow('Fixed Threshold', fixed_threshold_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
