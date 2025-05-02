import sensor, image, time, pyb

# Initialize the camera
sensor.reset()                      # Reset and initialize the sensor
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings to take effect
clock = time.clock()                # Create a clock object to track the FPS

# Define the min/max LAB values for fire colors (red/orange/yellow)
# These values are in HSV color space (Hue, Saturation, Value)
fire_thresholds = [
    (20, 60, 200, 255, 150, 255),   # Bright orange/red (high saturation)
    (10, 30, 200, 255, 200, 255),   # Bright yellow/orange
    (0, 20, 200, 255, 150, 255),    # Bright red
]

# Settings for blob detection
blob_settings = {
    'thresholds': fire_thresholds,
    'pixels_threshold': 100,         # Minimum number of pixels to be considered
    'area_threshold': 100,           # Minimum area
    'merge': True,                    # Merge overlapping blobs
    'margin': 10,                     # How close blobs can be before merging
}

# LED setup for visual feedback
red_led = pyb.LED(1)    # Red LED
green_led = pyb.LED(2)  # Green LED

def detect_fire():
    img = sensor.snapshot()
    
    # Find blobs that match fire colors
    blobs = img.find_blobs(fire_thresholds, 
                          pixels_threshold=blob_settings['pixels_threshold'],
                          area_threshold=blob_settings['area_threshold'],
                          merge=blob_settings['merge'],
                          margin=blob_settings['margin'])
    
    fire_detected = False
    
    for blob in blobs:
        # Draw a rectangle around the detected blob
        img.draw_rectangle(blob.rect(), color=(255, 0, 0))
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 255, 0))
        
        # Additional checks to reduce false positives
        # 1. Check if the blob is in the upper part of the image (smoke rises)
        if blob.cy() < img.height()//2:
            # 2. Check if the blob is growing (not implemented here - would need frame comparison)
            fire_detected = True
    
    # Visual feedback
    if fire_detected:
        red_led.on()
        green_led.off()
        print("FIRE DETECTED!")
    else:
        red_led.off()
        green_led.on()
    
    return img, fire_detected

while(True):
    clock.tick()                    # Update the FPS clock.
    img, fire = detect_fire()       # Detect fire
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
