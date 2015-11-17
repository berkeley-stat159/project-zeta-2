"""smooth images"""
# noinspection PyUnresolvedReferences
import scipy.ndimage as snd

def smooth (img_dict):
    """
    smooth images with
    Parameters
    ----------
    img_dict: dictionary of images for one subject

    Returns
    -------
    dictionary of smooth results

    """
    result = {}
    for key, img in img_dict.iteritems():
        result[key] = snd.gaussian_filter(img, 1)

    return result
