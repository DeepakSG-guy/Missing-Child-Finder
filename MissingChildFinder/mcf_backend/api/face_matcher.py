# api/face_matcher.py
import face_recognition
import numpy as np
from .models import MissingChild
import json

def encode_image_file(path):
    """
    Return a 1D numpy array encoding for the first face in the image.
    Returns None if no face found.
    """
    img = face_recognition.load_image_file(path)
    encs = face_recognition.face_encodings(img)
    if len(encs) == 0:
        return None
    return encs[0]  # numpy ndarray

def load_all_known_encodings():
    """
    Loads encodings from DB, returns two lists:
    - known_encs: list of numpy arrays
    - known_objs: list of MissingChild objects (same order)
    """
    known_encs = []
    known_objs = []
    for child in MissingChild.objects.exclude(encoding__isnull=True).exclude(encoding__exact=''):
        try:
            enc_list = json.loads(child.encoding)
            enc = np.array(enc_list, dtype=np.float64)
            known_encs.append(enc)
            known_objs.append(child)
        except Exception as e:
            # skip corrupt encoding
            print("Warning: skipping child id", child.id, "encoding load error:", e)
            continue
    return known_encs, known_objs

def compare_with_database(known_encs, unknown_enc, tolerance=0.5):
    """
    known_encs: list or array of known encodings (numpy arrays)
    unknown_enc: single numpy array
    returns (is_match: bool, best_idx: int or None, best_distance: float or None)
    """
    if unknown_enc is None or len(known_encs) == 0:
        return False, None, None

    # convert to numpy array of shape (N, 128)
    encs_np = np.vstack(known_encs)  # shape (N, 128)
    distances = face_recognition.face_distance(encs_np, unknown_enc)  # lower is better
    best_idx = int(np.argmin(distances))
    best_distance = float(distances[best_idx])
    is_match = best_distance <= tolerance
    return is_match, best_idx, best_distance
