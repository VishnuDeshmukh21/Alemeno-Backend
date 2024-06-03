from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cv2
import numpy as np
from PIL import Image
import os
from datetime import datetime

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def analyze_strip(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        original_file_name = image_file.name
        
        # Generate a unique file name with date and time
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_file_name = f"{original_file_name.split('.')[0]}_{current_time}.{original_file_name.split('.')[-1]}"
        
        # Define the target directory
        target_directory = os.path.join('urine_strip_analyzer', 'images')
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        
        # Save the file to the target directory
        file_path = os.path.join(target_directory, new_file_name)
        with default_storage.open(file_path, 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        
        # Process the image to extract colors
        colors = extract_colors(file_path)
        
        # Labels for the colors
        labels = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']
        
        # Create a dictionary with labels as keys and colors as values
        color_dict = {labels[i]: colors[i] for i in range(len(labels))}
        
        return JsonResponse(color_dict, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def crop_image(image_array, left_percentage=45, right_percentage=10, bottom_percentage=30, num_sections=10):
    height, width = image_array.shape[:2]
    crop_left = int(width * (left_percentage / 100))
    crop_right = int(width * (right_percentage / 100))
    crop_bottom = int(height * (1 - bottom_percentage / 100))
    
    # Calculate the height of each section
    section_height = (crop_bottom) // num_sections
    
    cropped_sections = []
    for i in range(num_sections):
        start_row = i * section_height
        end_row = (i + 1) * section_height if i < num_sections - 1 else crop_bottom
        cropped_section = image_array[start_row:end_row, crop_left:-crop_right]
        cropped_sections.append(cropped_section)
    
    return cropped_sections

def calculate_region_color(image_array):
    region_height, region_width = image_array.shape[:2]
    center_row = region_height // 2
    center_col = region_width // 2
    region = image_array[center_row - 4:center_row + 4, center_col - 4:center_col + 4]
    average_color = np.mean(region, axis=(0, 1)).astype(int)
    return average_color

def extract_colors(file_path):
    # Load the image using OpenCV
    image = cv2.imread(file_path)
    
    # Convert the image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Crop the image into sections
    cropped_sections = crop_image(image_rgb, left_percentage=45, right_percentage=20, bottom_percentage=35)
    
    # Calculate the average color of the center region of each section
    colors = []
    for section in cropped_sections:
        region_color = calculate_region_color(section)
        colors.append(region_color.tolist())
    
    return colors
