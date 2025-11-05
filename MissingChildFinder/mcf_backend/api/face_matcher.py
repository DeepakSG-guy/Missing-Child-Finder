import face_recognition

def compare_faces(known_image_path, unknown_image_path):
    try:
        known = face_recognition.load_image_file(known_image_path)
        unknown = face_recognition.load_image_file(unknown_image_path)
        known_enc = face_recognition.face_encodings(known)[0]
        unknown_enc = face_recognition.face_encodings(unknown)[0]
        results = face_recognition.compare_faces([known_enc], unknown_enc)
        return results[0]
    except Exception as e:
        print("Error:", e)
        return False
