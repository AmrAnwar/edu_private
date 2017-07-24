from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from django.db.models import Q

from asks.models import Ask
from accounts.api.serializers import UserDetailSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

ask_url = HyperlinkedIdentityField(
    view_name='asks-api:detail',
    lookup_field='id',
)
ask_delete_url = HyperlinkedIdentityField(
    view_name='asks-api:delete',
    lookup_field='id',
)
ask_edit_url = HyperlinkedIdentityField(
    view_name='asks-api:edit',
    lookup_field='id',
)


class UserQuestionsSerializer(ModelSerializer):
    # user = UserDetailSerializer(read_only=True)

    # questions = SerializerMethodField()
    class Meta:
        model = Ask
        fields = [
            'question',
            'replay',
        ]

    # def get_questions(self, obj):
    #     c_qs = Ask.objects.filter(user=obj).filter(~Q(replay=None))
    #     asks = AskDetailSerializer(c_qs, many=True).data
    #     return asks


class AskCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Ask
        fields = [
            'user',
            'question',
            # 'replay',
        ]

    # def validate(self, data):
    #     username = data.get("user", None)
    #     user = User.Objects.get(username=username)
    #     data['user'] = user
    #     return data

class AskDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    delete_url = ask_delete_url
    edit_url = ask_edit_url
    class Meta:
        model = Ask
        fields = [
            'id',
            'user',
            'question',
            'replay',
            'edit_url',
            'delete_url',

        ]


class AskListSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    # url = answer_url
    delete_url = ask_delete_url
    edit_url = ask_edit_url
    class Meta:
        model = Ask
        fields = [
            # 'url',
            'id',
            'user',
            'question',
            'replay',
            'timestamp',
            'delete_url',
            'edit_url',
    ]

