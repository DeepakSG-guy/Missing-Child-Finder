from rest_framework import serializers
from .models import MissingChild, Report

class MissingChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingChild
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
