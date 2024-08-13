import os
import uuid
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import win32com.client
import pythoncom
import logging

logger = logging.getLogger(__name__)

def scan_document(request):
    if request.method == 'POST':
        try:
            pythoncom.CoInitialize()
            wia = win32com.client.Dispatch("WIA.CommonDialog")
            print(wia)
            scanner = wia.ShowSelectDevice(1, True, False)

            if scanner:
                # Retrieve user options
                paper_size = request.POST.get('paper_size', 'A4')
                color_mode = request.POST.get('color_mode', 'Color')
                auto_scan = request.POST.get('auto_scan', False)
                zoom_level = int(request.POST.get('zoom_level', 100))

                try:
                    scan_item = scanner.Items[1]

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

                    # Generate a unique filename
                    unique_filename = f"scanned_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}.jpg"
                    output_file = os.path.join(settings.MEDIA_ROOT, unique_filename)

                    # Save scanned image
                    image.SaveFile(output_file)
                    logger.info(f"Scanned image saved to {output_file}")

                    return JsonResponse({"image_url": settings.MEDIA_URL + unique_filename})

                except Exception as scan_error:
                    error_code = scan_error.args[2][5]
                    logger.error(f"Scan error: {scan_error}")
                    if error_code == -2145320957:
                        return JsonResponse({"error": "The document feeder is empty. Please add documents to the feeder and try again."}, status=400)
                    else:
                        return JsonResponse({"error": str(scan_error)}, status=500)
            else:
                logger.error("No scanner was found or selected.")
                return JsonResponse({"error": "No scanner was found or selected."}, status=400)

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

