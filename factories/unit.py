import factory
import factory.fuzzy

from study.models import Unit


class UnitFactory(factory.DjangoModelFactory):
    class Meta:
        model = Unit

    title = factory.sequence(lambda n: "unit %s" % n)

