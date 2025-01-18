import cv2

def adaptive_threshold(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded correctly
    if image is None:
        print("Error loading the image.")
        return

    # Adaptive thresholding
    adaptive_threshold_image = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 9
    )

    # Display the results
    cv2.imshow('Original', image)
    cv2.imshow('Adaptive Threshold', adaptive_threshold_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
