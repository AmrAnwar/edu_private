# Avoid importing settings directly to
# allow tests to use test-specific settings
from django.conf import settings
from django.contrib.auth.models import User
import factory
import factory.fuzzy

from news.models import Post


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.Iterator(User.objects.all())

    title = factory.Faker('text')
    content = factory.Faker('text')
    image = factory.django.ImageField(color='red')
    file = factory.django.FileField()
    type = factory.Iterator(['a', 'b'])
