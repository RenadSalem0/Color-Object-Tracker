import cv2
import numpy as np

class ColorTracker:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.running = False
        
        # HSV color range for red (can be adjusted)
        self.lower_color1 = np.array([0, 120, 70])
        self.upper_color1 = np.array([10, 255, 255])
        self.lower_color2 = np.array([170, 120, 70])
        self.upper_color2 = np.array([180, 255, 255])
        
        # Morphological kernel
        self.kernel = np.ones((5,5), np.uint8)
        
        # Minimum contour area threshold
        self.min_contour_area = 500
        
    def process_frame(self, frame):
        """Process a single frame for color tracking"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create masks for the color range
        mask1 = cv2.inRange(hsv, self.lower_color1, self.upper_color1)
        mask2 = cv2.inRange(hsv, self.lower_color2, self.upper_color2)
        combined_mask = cv2.bitwise_or(mask1, mask2)
        
        # Apply morphological operations to reduce noise
        processed_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, self.kernel)
        processed_mask = cv2.morphologyEx(processed_mask, cv2.MORPH_DILATE, self.kernel)
        
        return processed_mask
    
    def find_largest_contour(self, mask):
        """Find the largest contour in the mask"""
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > self.min_contour_area:
                return largest_contour
        return None
    
    def draw_tracking_info(self, frame, contour):
        """Draw tracking information on the frame"""
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracked Object", (x, y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw center point (optional)
        center = (x + w//2, y + h//2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
        return frame
    
    def run(self):
        """Main tracking loop"""
        self.running = True
        
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Process the frame and track the object
            mask = self.process_frame(frame)
            contour = self.find_largest_contour(mask)
            
            if contour is not None:
                frame = self.draw_tracking_info(frame, contour)
            
            # Display results
            cv2.imshow("Color Tracking", frame)
            
            # Check for user input
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                self.running = False
            elif key == ord('p'):
                cv2.waitKey(-1)  # Pause until any key is pressed
                
        self.cleanup()
    
    def cleanup(self):
        """Release resources"""
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    tracker = ColorTracker("color.mp4")
    tracker.run()
