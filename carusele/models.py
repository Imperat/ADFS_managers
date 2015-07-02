from django.db import models

# Create your models here.

class Listing (models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField(default="")
    content = models.TextField()
    pubdate = models.DateTimeField()
    image = models.ImageField(upload_to="media")

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return "/carusele/art/%i/" % self.id

class Element (models.Model):
    description = models.CharField(max_length=400)
    content = models.TextField()
    image = models.ImageField(upload_to="media")
    caruse = models.OneToOneField("Listing")

    def __unicode__(self):
        return unicode(self.description)

