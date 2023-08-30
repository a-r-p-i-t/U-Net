





import cv2
import numpy as np
import os
import json

# Class ID to color mapping
# class_colors = {
#     0: (0,0,0),           # Black (Background)
#     1: (255, 192, 203),   # Pink (Acne)
#     2: (139, 69, 19),     # Brown (Blemish)
#     3: (255, 255, 255),   # White (Clogged Pores)
#     4: (255, 255, 0),     # Yellow (Dark Circles)
#     5: (0, 255, 0),       # Green (Freckle/Beauty Spot)
#     6: (0, 0, 255),       # Blue (Hyperpigmentation/Dark Marks)
#     7: (255, 0, 0),       # Red (Redness)
#     8: (128, 0, 128),     # Purple (Uneven Skintone)
#     9: (255, 165, 0),     # Orange (Wrinkle/Fine Lines)
# }
class_colors = {
    0: (0,0,0),           # Black (Background)
    1: (203, 192, 255),   # Pink (Acne)
    2: (19, 69, 139),     # Brown (Blemish)
    3: (255, 255, 255),   # White (Clogged Pores)
    4: (0, 255, 255),     # Yellow (Dark Circles)
    5: (0, 255, 0),       # Green (Freckle/Beauty Spot)
    6: (255, 0, 0),       # Blue (Hyperpigmentation/Dark Marks)
    7: (0, 0, 255),       # Red (Redness)
    8: (128, 0, 128),     # Purple (Uneven Skintone)
    9: (0, 165, 255),     # Orange (Wrinkle/Fine Lines)
}

# Path to the directory containing the exported annotations
annotations_dir = "new_annot\\instances_default.json"

# Output directory for mask images
output_dir = "test_categories"

# Load the exported annotations (COCO JSON format)
with open(os.path.join(annotations_dir), "r") as f:
    annotations_data = json.load(f)

# Process each annotation
for image_data in annotations_data["images"]:
    image_id = image_data["id"]
    image_filename = image_data["file_name"]
    image_width = image_data["width"]
    image_height = image_data["height"]
    
    # Create a black background
    mask = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    
    # Find annotations for this image
    for annotation in annotations_data["annotations"]:
        if annotation["image_id"] == image_id:
            # Extract the polygon points from the annotation (modify based on your annotation format)
            polygon_points = annotation["segmentation"]
            
            # Convert polygon points to integer format
            polygon_points = np.array(polygon_points, dtype=np.float32).reshape((-1, 2))
            polygon_points = polygon_points.astype(np.int32)
            
            # Get the class ID for this annotation
            class_id = annotation["category_id"]
            
            # Get the color for this class
            color = class_colors.get(class_id, (0, 0, 0))
            
            # Create a mask for the annotation with the class color
            cv2.fillPoly(mask, [polygon_points], color)
    
    # Save the mask as a PNG image
    mask_filename = os.path.splitext(image_filename)[0] + ".png"
    mask_filepath = os.path.join(output_dir, mask_filename)
    cv2.imwrite(mask_filepath, mask)

print("Conversion complete.")



