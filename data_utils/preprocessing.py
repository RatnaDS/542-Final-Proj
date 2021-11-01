import os
import nibabel as nib
import cv2


SEGMENTATION_FILE = "segmentation.nii.gz"
IMAGE_FILE = "imaging.nii.gz"

class Preprocessor:

    def __init__(self, dir):
        self.dir = dir
        self.case_ids = os.listdir(dir)

    def extract_and_save_slices(self, vol, seg):
        pass

    def generate_bounding_boxes(self, segmentations):
        
        labels = []

        # Find bounding box
        for segmentation_mask in segmentations:
            contours, hierarchy = cv2.findContours(segmentation_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            _label_str = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                _label_str.append(f"0 {x} {y} {w} {h}")
            label_str = "\n".join(_label_str)
            labels.append(label_str)

        return labels

    def save_bounding_boxes(self, base_save_dir, case_id, bounding_boxes):
        for i, bounding_box in enumerate(bounding_boxes):
            filename = os.path.join(base_save_dir, f"{case_id}_{i}.txt")
            with open(filename, "w") as f:
                f.write(bounding_box)

    def load_image_volume(self, case_path):
        volume_path = os.path.join(case_path, IMAGE_FILE)
        vol = nib.load(volume_path)
        return vol

    def load_segmentation_volume(self, case_path):
        segmentation_path = os.path.join(case_path, SEGMENTATION_FILE)
        seg = nib.load(segmentation_path)
        return seg
    
    def load_case(self, case_id):
        case_path = os.path.join(self.dir, case_id)
        image_volume = self.load_image_volume(case_path)
        segmentation_volume = self.load_segmentation_volume(case_path)
        return image_volume, segmentation_volume

    def run(self, base_save_dir):
        for case_id in self.case_ids:
            vol, seg = self.load_case(case_id)
            filenames, segmentations = self.extract_and_save_slices(vol, seg)
            bounding_boxes = self.generate_bounding_boxes(segmentations)
            self.save_bounding_boxes(base_save_dir, case_id, bounding_boxes)
