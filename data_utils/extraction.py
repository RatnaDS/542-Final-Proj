from pathlib import Path
import numpy as np
from imageio import imwrite

# Constants
DEFAULT_KIDNEY_COLOR = [255, 0, 0]
DEFAULT_TUMOR_COLOR = [0, 0, 255]
DEFAULT_HU_MAX = 512
DEFAULT_HU_MIN = -512
DEFAULT_OVERLAY_ALPHA = 0.3
DEFAULT_PLANE = "axial"

def hu_to_grayscale(volume, hu_min, hu_max):
    # Clip at max and min values if specified
    if hu_min is not None or hu_max is not None:
        volume = np.clip(volume, hu_min, hu_max)

    # Scale to values between 0 and 1
    mxval = np.max(volume)
    mnval = np.min(volume)
    im_volume = (volume - mnval)/max(mxval - mnval, 1e-3)

    # Return values scaled to 0-255 range, but *not cast to uint8*
    # Repeat three times to make compatible with color overlay
    im_volume = 255*im_volume
    return np.stack((im_volume, im_volume, im_volume), axis=-1)


def visualize_mask(seg):
    H, W = seg.shape
    vis_mask = np.zeros((H, W, 3), dtype=np.uint8)
    vis_mask[seg == 1] = np.array([255, 0, 0], dtype=np.uint8) # R for kidney
    vis_mask[seg == 2] = np.array([0, 0, 255], dtype=np.uint8) # B for tumor
    return vis_mask


def extract_and_save_slices(cid, vol, seg, destination, 
                            hu_min=DEFAULT_HU_MIN, hu_max=DEFAULT_HU_MAX):

    # Prepare output location
    out_path = Path(destination)
    if not out_path.exists():
        out_path.mkdir()  
    
    # Convert to a visual format
    vol_ims = hu_to_grayscale(vol, hu_min, hu_max)

    sliced_vol_path = out_path / "sliced_vol_images"  
    sliced_seg_path = out_path / "sliced_seg_images"

    if not sliced_vol_path.exists():

        sliced_vol_path.mkdir()

    if not sliced_seg_path.exists():

        sliced_seg_path.mkdir()

    list_seg = []
    list_vol = []

    for i in range(seg.shape[0]):

        seg_slice = seg[i]
        vol_slice = vol_ims[i]

        if np.equal(seg_slice,1).sum() > 0 or np.equal(seg_slice,2).sum()>0:

            list_seg.append(i)

            vis_seg_slice = visualize_mask(seg_slice)

            #saving of images
            imwrite(str(sliced_vol_path / ("{}_{:05d}.png".format(cid, i))),vol_slice)#.astype('uint8'))
            imwrite(str(sliced_seg_path / ("{}_{:05d}.png".format(cid, i))),vis_seg_slice)#.astype('uint8'))

            #maintaining the path lists in a list 
            list_vol.append(sliced_vol_path / ("{}_{:05d}.png".format(cid, i)))

    return list_vol, list_seg
