function openSettings() {
     // Implement settings popup or redirection
     alert('Settings dialog opens here.');
 }
 
 function autoScan() {
     // Implement auto-scan logic
     alert('Auto Scan initiated.');
 }
 
 function scanDocument() {
     // Implement document scanning and progress handling
     let progressBar = document.getElementById('progress-bar');
     progressBar.value = 0;
 
     let interval = setInterval(function() {
         if (progressBar.value < 100) {
             progressBar.value += 10; // Simulate progress
         } else {
             clearInterval(interval);
             // Handle the scanned document response here
             document.getElementById('scanner-image').src = 'path_to_scanned_image'; // Update with actual image path
         }
     }, 500);
 }
 
 function resetForm() {
     document.getElementById('scanner-image').src = '';
     document.getElementById('progress-bar').value = 0;
 }
 
 function rotateImage() {
     let img = document.getElementById('scanner-image');
     let currentRotation = img.style.transform.replace('rotate(', '').replace('deg)', '') || 0;
     img.style.transform = `rotate(${(parseInt(currentRotation) + 90) % 360}deg)`;
 }
 
 function zoomIn() {
     let img = document.getElementById('scanner-image');
     let currentScale = img.style.transform.replace('scale(', '').replace(')', '') || 1;
     img.style.transform = `scale(${parseFloat(currentScale) + 0.1})`;
 }
 
 function zoomOut() {
     let img = document.getElementById('scanner-image');
     let currentScale = img.style.transform.replace('scale(', '').replace(')', '') || 1;
     img.style.transform = `scale(${Math.max(1, parseFloat(currentScale) - 0.1)})`;
 }
 