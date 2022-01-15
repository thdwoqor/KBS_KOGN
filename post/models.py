from django.db import models
from radio.models import Radio
from .write import Write

from django.db.models.query import QuerySet
from django.urls import reverse

# https://simpleisbetterthancomplex.com/tutorial/2018/08/13/how-to-use-bootstrap-4-forms-with-django.html
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    # https://velog.io/@hwang-eunji/backend-django-%EC%A0%95%EC%B0%B8%EC%A1%B0-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0
    radio = models.ForeignKey(Radio, on_delete=models.CASCADE, related_name='radio_uniq_id')
    address = models.CharField(max_length=200)  
    contents = models.TextField(max_length=200)  

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self) -> str:
        return self.title
    
    def save(self):
        super().save()
        print(self.id, self.title, self.radio.id, self.address, self.contents)
        write = Write()
        write.Login()
        write.Write_Post(self.radio.id, self.title, self.address, self.contents)

    def get_absolute_url(self)-> int:
        return reverse("post-detail", kwargs={"id": self.id})
