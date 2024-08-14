import os
import uuid
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import win32com.client
import pythoncom
import logging
from PIL import Image
import time

from django.views.decorators.csrf import csrf_exempt




logger = logging.getLogger(__name__)

def rotate_image(image_path, angle):
    """Rotate image by a specific angle."""
    with Image.open(image_path) as img:
        rotated_img = img.rotate(angle, expand=True)
        rotated_img.save(image_path)

def resize_image(image_path, zoom_factor):
    """Resize image to zoom in or out."""
    with Image.open(image_path) as img:
        width, height = img.size
        new_size = (int(width * zoom_factor), int(height * zoom_factor))
        resized_img = img.resize(new_size, Image.ANTIALIAS)
        resized_img.save(image_path)
        
@csrf_exempt
def scan_document(request):
    if request.method == 'POST':
        try:
            pythoncom.CoInitialize()
            wia = win32com.client.Dispatch("WIA.CommonDialog")
            logger.info("WIA CommonDialog dispatched successfully.")

            device_manager = win32com.client.Dispatch("WIA.DeviceManager")
            logger.info("WIA DeviceManager dispatched successfully.")
            
            devices = device_manager.DeviceInfos
            logger.info(f"Number of devices found: {devices.Count}")

            if devices.Count == 0:
                logger.error("No scanner devices found.")
                return JsonResponse({"error": "No scanner devices found."}, status=400)
            
            # Directly access the default scanner
            default_device = devices.Item(1).Connect()  # Assuming the first device is the default one
            scan_item = default_device.Items[1]

            logger.info(f"Received request data: {request.POST}")

            # Retrieve user options
            paper_size = request.POST.get('paper_size', 'A4')
            color_mode = request.POST.get('color_mode', 'Color')
            auto_scan = request.POST.get('auto_scan', False)
            zoom_level = int(request.POST.get('zoom_level', 100))
            num_pages = int(request.POST.get('num_pages', 1))  # Number of pages to scan

            scanned_files = []

            for page in range(num_pages):
                retry_attempts = 3
                for attempt in range(retry_attempts):
                    try:
                        # Set scan properties based on user selection
                        if color_mode == 'Grayscale':
                            scan_item.Properties("6146").Value = 2  # 1: Color, 2: Grayscale
                        else:
                            scan_item.Properties("6146").Value = 1  # 1: Color, 2: Grayscale

                        # Set zoom level by adjusting DPI
                        dpi = int(300 * (zoom_level / 100))
                        scan_item.Properties("6147").Value = dpi  # Horizontal DPI
                        scan_item.Properties("6148").Value = dpi  # Vertical DPI

                        image = scan_item.Transfer()

                        # Generate a unique filename for each page
                        unique_filename = f"scanned_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}_page_{page+1}.jpg"
                        output_file = os.path.join(settings.MEDIA_ROOT, unique_filename)

                        # Save scanned image
                        image.SaveFile(output_file)
                        logger.info(f"Scanned image page {page+1} saved to {output_file}")

                        # Optionally rotate or resize the image
                        # rotate_image(output_file, 90)  # Rotate by 90 degrees
                        # resize_image(output_file, 0.8)  # Zoom out by 80%

                        scanned_files.append(settings.MEDIA_URL + unique_filename)
                        break  # Exit retry loop on success

                    except Exception as scan_error:
                        logger.error(f"Error scanning page {page+1} (attempt {attempt+1}): {scan_error}")
                        time.sleep(2)  # Wait before retrying

            return JsonResponse({"image_urls": scanned_files})

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            pythoncom.CoUninitialize()
            logger.info("COM library uninitialized")

    else:
        return render(request, 'scanner_app/scan.html')

def reset_form(request):
    return JsonResponse({"message": "Form has been reset."})

def cancel_scan(request):
    # Logic to cancel an ongoing scan could be complex; here we just return a response
    return JsonResponse({"message": "Scan operation canceled."})

def home(request):
    return render(request, 'scanner_app/home.html')
