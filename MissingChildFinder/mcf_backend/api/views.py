# from django.shortcuts import render

# # Create your views here.
# from django.http import HttpResponse

# def hello(request):
#     return HttpResponse("Backend setup successful!")
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MissingChild, Report
from .serializers import MissingChildSerializer, ReportSerializer
from .face_matcher import compare_faces

@api_view(['POST'])
def register_child(request):
    serializer = MissingChildSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upload_image(request):
    image_file = request.FILES.get('uploaded_photo')
    report = Report.objects.create(uploaded_photo=image_file)

    for child in MissingChild.objects.all():
        match = compare_faces(child.photo.path, report.uploaded_photo.path)
        if match:
            report.matched_child = child
            report.save()
            return Response({
                "match": True,
                "child": MissingChildSerializer(child).data
            })
    report.save()
    return Response({"match": False})
