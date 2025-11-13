# api/models.py
import json
from django.db import models

class MissingChild(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    photo = models.ImageField(upload_to='images/')
    last_seen_location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Missing')
    encoding = models.TextField(null=True, blank=True)   # store JSON string of encoding

    def set_encodings(self, encodings):
        # encodings: list of lists (floats)
        self.face_encodings_json = json.dumps(encodings)
    def get_encodings(self):
        if not self.face_encodings_json:
            return []
        return json.loads(self.face_encodings_json)

class Report(models.Model):
    uploaded_photo = models.ImageField(upload_to='reports/')
    matched_child = models.ForeignKey(MissingChild, on_delete=models.SET_NULL, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)

def __str__(self):
        return self.name