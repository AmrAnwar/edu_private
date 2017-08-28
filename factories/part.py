import factory
import factory.fuzzy

from study.models import Unit, Part


class PartFactory(factory.DjangoModelFactory):
    class Meta:
        model = Part

    unit = factory.Iterator(Unit.objects.all())
    title = factory.sequence(lambda n: "Part %s" % n)

