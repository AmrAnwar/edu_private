import factory
import factory.fuzzy

from .user import UserFactory
from accounts.models import UserProfile, Group


def generate_username():
    i = 1
    while UserProfile.objects.filter(username='user_%d' % i):
        i += 1
    return 'user_%d' % i


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserProfile

    # user = factory.SubFactory(UserFactory)
    group = factory.Iterator(Group.objects.all())
    username = factory.LazyFunction(generate_username)
