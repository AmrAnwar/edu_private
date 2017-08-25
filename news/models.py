# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse

import requests
import json

User = get_user_model()

types = (
    ('a', 'news'),
    ('b', 'education news'),
)


def upload_location(instance, filename):
    if instance.id:
        new_id = instance.id
    else:
        try:
            new_id = Post.objects.order_by("id").last().id + 1
        except:
            new_id = 1
    return "news/%s/%s" % (new_id, filename)


# Create your models here.
try:
    first_user = User.objects.all().first()
    first_user = first_user.id
except:
    first_user = 1

class Post(models.Model):
    user = models.ForeignKey(User, default=1, null=False)
    title = models.CharField(null=False, max_length=50)
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    wait = models.BooleanField(default=False)
    type = models.CharField(choices=types, max_length=3, default=1)
    image = models.ImageField(
        upload_to=upload_location,
        null=True, blank=True,
        height_field='height_field_image',
        width_field='width_field_image',
    )
    file = models.FileField(null=True, blank=True)
    height_field_image = models.IntegerField(default=0)
    width_field_image = models.IntegerField(default=0)

    class Meta:
        ordering = ["-timestamp"]

    def __unicode__(self):
        return "%s:%s" % (self.user, self.title)

        # def get_absolute_url(self):
        #     return reverse("news:detail", kwargs={'slug': self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    url = 'https://fcm.googleapis.com/fcm/send'
    data = {'to': '/topics/news',
            'data': {
                'message_title': '%s' % (instance.title),
                'message_body': '%s' % (instance.content),
                'where': 'news'
                }
            }
    headers = {
        'Authorization': 'key=AIzaSyC6PljgOsaTz2fULnW8uIY0sYIJ0MrDWDA',
        'Content-Type': 'application/json',
    }

    r = requests.post(url, data=json.dumps(data), headers=(headers))

pre_save.connect(pre_save_post_receiver, sender=Post)
