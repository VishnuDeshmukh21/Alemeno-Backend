# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
# import cv2
# import numpy as np

# @csrf_exempt
# def analyze_strip(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES['image']
#         file_path = default_storage.save('temp.jpg', ContentFile(image_file.read()))
        
#         # Process the image to extract colors
#         colors = extract_colors(file_path)
        
#         # Labels for the colors
#         labels = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']
        
#         # Create a dictionary with labels as keys and colors as values
#         color_dict = {labels[i]: colors[i] for i in range(len(labels))}
        
#         return JsonResponse(color_dict, safe=False)
#     return JsonResponse({'error': 'Invalid request'}, status=400)

# def extract_colors(file_path):
#     # Load the image using OpenCV
#     image = cv2.imread(file_path)
    
#     # Convert the image to RGB (OpenCV loads images in BGR format)
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     # Assume the strip is vertically aligned and find the 10 color boxes
#     height, width, _ = image_rgb.shape
#     box_height = height // 10
    
#     colors = []
#     for i in range(10):
#         box = image_rgb[i * box_height: (i + 1) * box_height, :]
#         average_color = box.mean(axis=0).mean(axis=0)
#         colors.append(average_color.astype(int).tolist())
    
#     return colors


from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cv2
import numpy as np

@csrf_exempt
def analyze_strip(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        file_path = default_storage.save('temp.jpg', ContentFile(image_file.read()))
        
        # Process the image to extract colors
        colors = extract_colors(file_path)
        
        # Labels for the colors
        labels = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']
        
        # Create a dictionary with labels as keys and colors as values
        color_dict = {labels[i]: colors[i] for i in range(len(labels))}
        
        return JsonResponse(color_dict, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def extract_colors(file_path):
    # Load the image using OpenCV
    image = cv2.imread(file_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use edge detection to find the strip
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the contour with the largest area, which should be the strip
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Crop the strip from the image
    strip = image[y:y+h, x:x+w]
    
    # Ensure the strip is vertically aligned
    if w > h:
        strip = cv2.rotate(strip, cv2.ROTATE_90_CLOCKWISE)
        h, w = w, h  # Swap height and width
    
    # Convert the strip to RGB (OpenCV loads images in BGR format)
    strip_rgb = cv2.cvtColor(strip, cv2.COLOR_BGR2RGB)
    
    # Calculate the height of each box
    box_height = h // 10
    
    colors = []
    for i in range(10):
        box = strip_rgb[i * box_height: (i + 1) * box_height, :]
        average_color = box.mean(axis=0).mean(axis=0)
        colors.append(average_color.astype(int).tolist())
        
        # Optional: Draw rectangles for debugging
        cv2.rectangle(strip, (0, i * box_height), (w, (i + 1) * box_height), (255, 0, 0), 2)
    
    # Save the processed image with rectangles drawn for debugging
    cv2.imwrite('dddetected_strip.jpg', strip)
    
    return colors



# def extract_colors(file_path):
#     # Load the image using OpenCV
#     image = cv2.imread(file_path)
    
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Use edge detection to find the strip
#     edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
#     # Find contours in the edge-detected image
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     # Find the contour with the largest area, which should be the strip
#     largest_contour = max(contours, key=cv2.contourArea)
    
#     # Get the bounding box of the largest contour
#     x, y, w, h = cv2.boundingRect(largest_contour)
    
#     # Crop the strip from the image
#     strip = image[y:y+h, x:x+w]
    
#     # Assume the strip is vertically aligned and find the 10 color boxes
#     box_height = h // 10
    
#     colors = []
#     for i in range(10):
#         box = strip[i * box_height: (i + 1) * box_height, :]
#         average_color = box.mean(axis=0).mean(axis=0)
#         colors.append(average_color.astype(int).tolist())

#         cv2.rectangle(strip, (0, i * box_height), (w, (i + 1) * box_height), (255, 0, 0), 2)
#     cv2.imwrite('detected_strip.jpg', image)
#     return colors
