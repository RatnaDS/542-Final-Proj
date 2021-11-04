import os
import nibabel as nib
import numpy as np
import cv2

from .extraction import extract_and_save_slices


SEGMENTATION_FILE = "segmentation.nii.gz"
IMAGE_FILE = "imaging.nii.gz"

class Preprocessor:

    def __init__(self, dir):
        self.dir = dir
        self.case_ids = [f for f in os.listdir(dir) if "." not in f]

    def extract_and_save_slices(self, cid, vol, seg, destination):
        filenames, indices = extract_and_save_slices(cid, vol, seg, destination)
        return filenames, indices

    def generate_bounding_boxes(self, segmentations, seg_values=[1, 2], center_and_scale=False):
        
        labels = []

        # Find bounding box
        for segmentation_mask in segmentations:

            H, W = segmentation_mask.shape

            # Threshold
            if isinstance(seg_values, list):
                _segmentation_mask = (
                    1*np.logical_or(
                        segmentation_mask == seg_values[0], 
                        segmentation_mask == seg_values[1])).astype(np.uint8)
            else:
                _segmentation_mask = ((segmentation_mask == seg_values)*1).astype(np.uint8)
            contours, hierarchy = cv2.findContours(_segmentation_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            _label_str = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if center_and_scale:
                    x_center = float(x) + float(w) / 2.
                    y_center = float(y) + float(h) / 2.

                    # Scale
                    x_center = x_center / float(W)
                    w = w / float(W)
                    y_center = y_center / float(H)
                    h = h / float(H)
                    _label_str.append(f"0 {x_center} {y_center} {w} {h}")
                else:
                    _label_str.append(f"0 {x} {y} {w} {h}")

            label_str = "\n".join(_label_str)
            labels.append(label_str)

        return labels

    def save_bounding_boxes(self, base_save_dir, filename, bounding_boxes):
        for i, bounding_box in enumerate(bounding_boxes):
            filename = os.path.join(base_save_dir, "labels", "{}.txt".format(filename))
            with open(filename, "w") as f:
                f.write(bounding_box)

    def load_image_volume(self, case_path):
        volume_path = os.path.join(case_path, IMAGE_FILE)
        vol = nib.load(volume_path).get_data()
        return vol

    def load_segmentation_volume(self, case_path):
        segmentation_path = os.path.join(case_path, SEGMENTATION_FILE)
        seg = nib.load(segmentation_path).get_data().astype(np.int32)
        return seg
    
    def load_case(self, case_id):
        case_path = os.path.join(self.dir, case_id)
        image_volume = self.load_image_volume(case_path)
        segmentation_volume = self.load_segmentation_volume(case_path)
        return image_volume, segmentation_volume

    def run(self, base_save_dir):
        files = []
        for case_id in self.case_ids:
            vol, seg = self.load_case(case_id)
            filenames, indices = self.extract_and_save_slices(case_id, vol, seg, base_save_dir)

    def generate_bb(self, segmentation_image_path, base_save_dir, seg_values=[1, 2]):
        images = os.listdir(segmentation_image_path)
        for image in images:
            seg_img = cv2.imread(os.path.join(segmentation_image_path, image))[:, :, ::-1]
            # Convert to original
            seg = np.zeros(seg_img.shape[:2])
            seg[seg_img[:, : 0] == 255] = 1 # R
            seg[seg_img[:, : 2] == 255] = 2 # B
            bounding_boxes = self.generate_bounding_boxes([seg], seg_values=seg_values)
            filename = image.split(".")[0]
            self.save_bounding_boxes(base_save_dir, filename, bounding_boxes)
