import face_recognition
import numpy as np
from PIL import Image

def load_image_rgb(path):
    """Load image and ensure it's in RGB numpy format."""
    img = face_recognition.load_image_file(path)  # returns RGB numpy array
    return img

def get_face_encodings(image_np):
    """Return list of encodings for faces found in the image."""
    encs = face_recognition.face_encodings(image_np)
    return encs

def compare_faces(known_image_path, unknown_image_path, tolerance=0.5, debug=False):
    """
    Compare known and unknown image paths.
    Returns (match_bool, distance or None, debug_info)
    """
    debug_info = {}

    # Load images
    try:
        known_img = load_image_rgb(known_image_path)
    except Exception as e:
        return False, None, {"error": f"Failed to load known image: {e}"}

    try:
        unknown_img = load_image_rgb(unknown_image_path)
    except Exception as e:
        return False, None, {"error": f"Failed to load unknown image: {e}"}

    # Get encodings
    known_encs = get_face_encodings(known_img)
    unknown_encs = get_face_encodings(unknown_img)

    debug_info['known_faces_found'] = len(known_encs)
    debug_info['unknown_faces_found'] = len(unknown_encs)

    if debug:
        print("DEBUG: known faces:", debug_info['known_faces_found'])
        print("DEBUG: unknown faces:", debug_info['unknown_faces_found'])

    if len(known_encs) == 0:
        return False, None, {**debug_info, "error": "No face found in known image."}
    if len(unknown_encs) == 0:
        return False, None, {**debug_info, "error": "No face found in uploaded image."}

    # If there are multiple faces, choose the first one by default.
    # You may want to change strategy: compute pairwise distances and pick best match.
    # We'll compute pairwise distances and choose best pair.
    best_distance = None
    best_pair = (None, None)  # (known_idx, unknown_idx)

    for i, k_enc in enumerate(known_encs):
        for j, u_enc in enumerate(unknown_encs):
            dist = np.linalg.norm(k_enc - u_enc)  # same as face_recognition.face_distance
            if best_distance is None or dist < best_distance:
                best_distance = dist
                best_pair = (i, j)

    debug_info['best_distance'] = float(best_distance)
    debug_info['best_pair'] = best_pair
    debug_info['tolerance'] = tolerance

    match = (best_distance <= tolerance)

    if debug:
        print("DEBUG: best_distance =", best_distance)
        print("DEBUG: match =", match)

    return match, float(best_distance), debug_info


# Quick test-run if executed directly
if __name__ == "__main__":
    m, d, info = compare_faces("child_known.jpg", "child_unknown.jpg", tolerance=0.5, debug=True)
    print("Match:", m, "Distance:", d, "Info:", info)
