import factory
import factory.fuzzy

from study.models import Part, Word


class WordFactory(factory.DjangoModelFactory):
    class Meta:
        model = Word

    part = factory.Iterator(Part.objects.all())
    name = factory.Faker('first_name')
    translation = factory.Faker('first_name')

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if extracted:
            for user in extracted:
                self.users.add(user)
