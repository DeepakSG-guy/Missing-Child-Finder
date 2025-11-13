# api/views.py
import json
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MissingChild, Report
from .serializers import MissingChildSerializer, ReportSerializer
from .face_matcher import encode_image_file, load_all_known_encodings, compare_with_database

@api_view(['POST'])
def register_child(request):
    serializer = MissingChildSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()  # saved and photo file uploaded
        # compute encoding from saved image file
        if obj.photo and os.path.exists(obj.photo.path):
            enc = encode_image_file(obj.photo.path)
            if enc is not None:
                # convert to list for JSON serializable storage
                enc_list = enc.tolist()
                obj.encoding = json.dumps(enc_list)
                obj.save()
            else:
                # no face detected — you may want to delete or flag this entry
                print("Warning: no face found in registered image for id", obj.id)
        return Response(MissingChildSerializer(obj).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upload_image(request):
    image_file = request.FILES.get('uploaded_photo')  # Postman key must be 'uploaded_photo'
    if not image_file:
        return Response({"error": "No file provided under key 'uploaded_photo'."}, status=status.HTTP_400_BAD_REQUEST)

    report = Report.objects.create(uploaded_photo=image_file)
    report.save()  # ensure file is saved and path exists

    if not os.path.exists(report.uploaded_photo.path):
        return Response({"error": "uploaded file not saved properly."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # encode uploaded image
    unknown_enc = encode_image_file(report.uploaded_photo.path)
    if unknown_enc is None:
        return Response({"match": False, "reason": "No face detected in uploaded image."})

    # load known encodings from DB
    known_encs, known_objs = load_all_known_encodings()
    is_match, best_idx, best_distance = compare_with_database(known_encs, unknown_enc, tolerance=0.5)

    if is_match:
        matched_child = known_objs[best_idx]
        report.matched_child = matched_child
        report.save()
        return Response({
            "match": True,
            "child": MissingChildSerializer(matched_child).data,
            "distance": best_distance
        })
    else:
        return Response({"match": False, "distance": best_distance})
