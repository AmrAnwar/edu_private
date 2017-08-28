import factory
import factory.fuzzy

from asks.models import Ask
from django.contrib.auth.models import User


class AskFactory(factory.DjangoModelFactory):
    class Meta:
        model = Ask

    user = factory.Iterator(User.objects.all())
    question = factory.Faker('text')
    image_sender = factory.django.ImageField(color='blue')
