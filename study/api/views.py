from django.db.models import Q
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from news.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

from rest_framework.filters import SearchFilter, OrderingFilter
from django.http import HttpResponse, HttpResponseRedirect, Http404
from rest_framework.response import Response

from study.models import Unit,Part,Word

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    UnitListV1Serializer,
    UnitListSerializer,
    WordDetailSerializer,
    PartDetailFullSerializer,
PartDetailSerializer,
PartDetailWordSerializer,
PartDetailTestSerializer,
)
from django.contrib.auth.models import User

# class UnitDetailAPIView(RetrieveAPIView):
#     queryset = Unit.objects.all()
#     serializer_class = UnitDetailSerializer
#     lookup_field = 'slug'


class PartDetailWordsAPIView(APIView):
    def gg



class PartDetailTestsAPIView(RetrieveAPIView):
    queryset = Part.objects.all()
    serializer_class = PartDetailTestSerializer
    lookup_field = 'id'


class UnitListAPIViewV2(ListAPIView):
    serializer_class = UnitListSerializer
    # filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = PostPageNumberPagination
    def get_queryset(self):
        querset_list = Unit.objects.filter(wait=False)
        return querset_list


class UnitListAPIViewV1(ListAPIView):
    serializer_class = UnitListV1Serializer
    pagination_class = PostPageNumberPagination
    def get_queryset(self):
        querset_list = Unit.objects.filter(wait=False)
        return querset_list


class PartListAPIView(ListAPIView):
    serializer_class = PartDetailFullSerializer
    pagination_class = PostPageNumberPagination
    def get_queryset(self):
        querset_list = Part.objects.filter(wait=False)
        q = self.request.GET.get("q")
        if q:
            querset_list = Part.objects.filter(id=int(q))
        return querset_list


class WordListAPIView(APIView):
    def get_object(self, slug):
        try:
            return Part.objects.get(slug=slug)
        except Part.DoesNotExist:
            raise Http404

    def get(self, request, slug=None, format=None):
        part = Part.objects.get(slug=slug)
        queryset = Word.objects.filter(part=part)
        serializer = WordDetailSerializer(queryset)
        return Response(serializer.data)


class WordStarToggle(APIView):
    def get(self, request, word_id=None, user_id=None, format=None):
        word = get_object_or_404(Word, id=word_id)
        user = get_object_or_404(User, id=user_id)
        toggle = False
        if user in word.users.all():
            word.users.remove(user)
        else:
            word.users.add(user)
            toggle = True
        word.save()
        data = {
            "toggle": toggle,
        }
        return Response(data)

