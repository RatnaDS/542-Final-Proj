import os
from data_utils.preprocessing import Preprocessor

save_dir = os.path.join("data", "preprocessed_data")
dir = "D:\\Desktop\\ECE_542\\ECE_542_Course_Project\\kits19\\data"
segmentation_image_path = os.path.join("data", "preprocessed_data", "sliced_seg_images")
preprocessor = Preprocessor(dir)
preprocessor.generate_bb(segmentation_image_path, save_dir, seg_values=[1, 2])
