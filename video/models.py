from django.db import models

class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    request_type = models.CharField(max_length=10)       
    text = models.TextField()                            

    def __str__(self):
        return f"{self.timestamp} - {self.request_type}: {self.text}"