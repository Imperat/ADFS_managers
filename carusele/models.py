from django.db import models

# Create your models here.
class Element (models.Model):
    description = models.CharField(max_length=400)
    content = models.TextField(null=2)
    image = models.ImageField(upload_to="media")

    def __unicode__(self):
        return unicode(self.description)
