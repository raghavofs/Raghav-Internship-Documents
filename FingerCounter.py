import cv2
import numpy as np

# Function to count fingers
def count_fingers(thresholded, hand_contour):
    # Find the convex hull of the hand contour
    hull = cv2.convexHull(hand_contour, returnPoints=False)
    
    # Calculate the defects in the convex hull
    defects = cv2.convexityDefects(hand_contour, hull)
    
    if defects is not None:
        finger_count = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(hand_contour[s][0])
            end = tuple(hand_contour[e][0])
            far = tuple(hand_contour[f][0])
            
            # Calculate the triangle area formed by each defect point
            a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c))
            
            # If angle < 90 degrees, it's a convexity defect (finger)
            if angle < np.pi/2:
                finger_count += 1
        
        # Add one to finger count to adjust for thumb
        return finger_count + 1
    
    return 0

# Main function for real-time finger counting
def main():
    cap = cv2.VideoCapture(0)  # Open webcam
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Perform thresholding to create binary image
        _, thresholded = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # Find the largest contour (hand)
            hand_contour = max(contours, key=cv2.contourArea)
            
            # Draw contours on the original frame
            cv2.drawContours(frame, [hand_contour], -1, (0, 255, 0), 2)
            
            # Count fingers based on defects in the convex hull
            finger_count = count_fingers(thresholded, hand_contour)
            
            # Display finger count on the frame
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # Display the frame
        cv2.imshow('Finger Count', frame)
        
        # Exit loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
