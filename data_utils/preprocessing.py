import os
import nibabel as nib


SEGMENTATION_FILE = "segmentation.nii.gz"
IMAGE_FILE = "imaging.nii.gz"

class Preprocessor:

    def __init__(self, dir):
        self.dir = dir
        self.case_ids = os.listdir(dir)

    def extract_slices(self, vol, seg):
        pass

    def save_slices(self, slices, segmentations):
        pass

    def generate_bounding_boxes(self, segmentations):
        pass

    def save_bounding_boxes(self, segmentations):
        pass

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

    def run(self):
        for case_id in self.case_ids:
            vol, seg = self.load_case(case_id)
            slices, segmentations = self.extract_slices(vol, seg)
            self.save_slices(slices, segmentations)
            bounding_boxes = self.generate_bounding_boxes(segmentations)
            self.save_bounding_boxes(bounding_boxes)
