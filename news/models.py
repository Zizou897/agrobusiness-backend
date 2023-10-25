from django.db import models
from ckeditor.fields import RichTextField

from core.constants import NEWS_IMAGE_PATH
from core.validators import validate_image_extension, validate_image_size

class NewsType(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField(verbose_name="Description", null=True, blank=True)
    image = models.ImageField(upload_to=NEWS_IMAGE_PATH, validators=[validate_image_size, validate_image_extension])
    news_type = models.ForeignKey(NewsType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


