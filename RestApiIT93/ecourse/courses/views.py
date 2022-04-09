from django.shortcuts import render
from django.http import  HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Course, Lesson, Comment, User, Rating, Like
from .perms import CommentOwnerPerms
from .serializers import CourseSerializer, \
    CategorySerializer, LessonSerializer, \
    CommentSerializer, LessonDetailSerializer, UserSerializer
from .paginators import CoursePaginator



class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active = True)
    serializer_class = CategorySerializer

    def get_queryset(self):
        q = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)

        return q


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active = True)
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    @swagger_auto_schema(
        operation_description='Get the lessons of a course',
        responses={
            status.HTTP_200_OK: LessonSerializer()
        }
    )
    @action(methods=['get'],detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        course = self.get_object()
        lessons = course.lessons.filter(active=True)

        kw = request.query_params.get('kw')
        if kw:
            lessons = lessons.filter(subject_icontains=kw)

        return Response(data=LessonSerializer(lessons, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)



class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonDetailSerializer

    def get_permissions(self):
        if self.action in ['like', 'rating']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @swagger_auto_schema(
        operation_description='Get the comments of a lesson',
        responses={
            status.HTTP_200_OK: CommentSerializer()
        }
    )
    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        lesson = self.get_object()
        comments = lesson.comments.select_related('user').filter(active=True)

        return Response(CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        lesson = self.get_object()
        user = request.user

        l, _ = Like.objects.get_or_create(lesson=lesson, user=user)
        l.active = not l.active
        try:
            l.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='rating', detail=True)
    def rating(self, request, pk):
        lesson = self.get_object()
        user = request.user

        r, _ = Rating.objects.get_or_create(lesson=lesson, user=user)
        r.rate = request.data.get('rate', 0)
        try:
            r.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)




class CommentViewSet(viewsets.ViewSet, generics.ListAPIView , generics.CreateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer
    permissions_class = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [CommentOwnerPerms()]

        return [permissions.IsAuthenticated()]



class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer



