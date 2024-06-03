# Alemeno-Backend

# Urine Strip Analyzer

This project is a web application for analyzing urine strip images and identifying the colors present on the strip. It provides an interface for users to upload an image of their urine strip and receive the color analysis results in JSON format.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Backend Explanation](#backend-explanation)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/urine-strip-analyzer.git
    ```

2. Navigate to the project directory:
    ```sh
    cd urine-strip-analyzer
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Django server:
    ```sh
    python manage.py runserver
    ```

2. Open your web browser and go to `http://localhost:8000/` to access the application.

3. Upload an image of a urine strip using the provided form.

4. Click the "Upload" button to submit the image for analysis.

5. View the color analysis results displayed on the page.

## Technologies Used

- Django: Web framework for backend development.
- OpenCV: Library for image processing.
- JavaScript: Used for frontend interaction.
- HTML/CSS: Used for frontend layout and styling.
- Bootstrap: CSS framework for styling.

## Backend Explanation

### Views

- **index**: Renders the index.html template which contains the form for uploading images.

- **analyze_strip**: Handles the POST request for analyzing the urine strip image. It saves the uploaded image to the server, processes it using OpenCV to extract colors, and returns the color analysis results in JSON format.

### Image Processing

The `extract_colors` function in the backend processes the uploaded image using OpenCV. Here's a breakdown of the image processing steps:

1. **Image Cropping**: The uploaded image is cropped into sections to isolate different regions of the urine strip.

2. **Color Extraction**: For each section, the average color of the center region is calculated to represent the color of that region.

3. **Result**: The extracted colors are returned as a list of RGB values in the JSON response.


