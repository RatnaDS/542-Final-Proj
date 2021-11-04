import numpy as np

DEFAULT_KIDNEY_COLOR = [255, 0, 0]
DEFAULT_TUMOR_COLOR = [0, 0, 255]
DEFAULT_OVERLAY_ALPHA = 0.3


def visualize_mask(image, mask, alpha=DEFAULT_OVERLAY_ALPHA):

    _image = image.copy().astype(np.float32)
    _mask = mask.copy().astype(np.float32)

    # Get binary array for places where an ROI lives
    segbin = np.max(mask, axis=-1) > 0
    repeated_segbin = np.stack((segbin, segbin, segbin), axis=-1)

    # Weighted sum where there's a value to overlay
    overlayed = np.where(
        repeated_segbin,
        np.round(alpha*_mask+(1-alpha)*_image).astype(np.uint8),
        np.round(image).astype(np.uint8)
    )
    return overlayed


def colorize_mask(segmentation):

    # Get binary array for places where an ROI lives
    segbin_kidney = segmentation == 1
    segbin_tumor = segmentation == 2

    vis_mask = np.zeros(segmentation.shape+(3,))
    vis_mask[segbin_kidney] = np.array(DEFAULT_KIDNEY_COLOR)
    vis_mask[segbin_tumor] = np.array(DEFAULT_TUMOR_COLOR)
    
    return vis_mask.astype(np.uint8)
