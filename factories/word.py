import factory
import factory.fuzzy

from study.models import Part, Word


class WordFactory(factory.DjangoModelFactory):
    class Meta:
        model = Word

    part = factory.Iterator(Part.objects.all())
    name = factory.Faker('first_name')
    translation = factory.Faker('first_name')
