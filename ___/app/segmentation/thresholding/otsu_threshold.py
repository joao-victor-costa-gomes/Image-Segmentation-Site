import cv2

def otsu_threshold(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded correctly
    if image is None:
        print("Error loading the image.")
        return

    # Otsu thresholding
    _, otsu_threshold_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Display the results
    cv2.imshow('Original', image)
    cv2.imshow('Otsu Threshold', otsu_threshold_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
