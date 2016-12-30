from django.db import models


class News (models.Model):
    """
    News model represent detail description and
    content of each carusele element.
    """
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
    """
    This model presents picture and short description
    of news in carusele javascript element on main page.
    """
    description = models.CharField(max_length=400)
    image = models.ImageField(upload_to="media")
    news = models.OneToOneField("News")

    def __unicode__(self):
        return unicode(self.description)
