from django.db import models


class Comment(models.Model):
    comment_no = models.AutoField(primary_key = True)
    title = models.CharField(max_length=100)
    shop_id = models.IntegerField(default = 0)
    text = models.CharField(max_length = 500)