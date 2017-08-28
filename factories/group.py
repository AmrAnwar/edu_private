import factory
import factory.fuzzy

from accounts.models import Group


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group

    title = factory.Iterator([
        'GUC',
        'AUC',
        'MSA',
        'AAST CAIRO',
        'AAST ALEX',
        'MUST',
        'MANSOURA'])
