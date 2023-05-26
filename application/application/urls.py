"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.views import CreateUserAPIView
from API.views import ProjectViewset, UsersViewset, IssuesViewset,\
    CommentsViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')
project_router = routers.NestedSimpleRouter(router,
                                            r'projects',
                                            lookup='project')
project_router.register(r'users', UsersViewset, basename='users')
project_router.register(r'issues', IssuesViewset, basename='issues')

issue_router = routers.NestedSimpleRouter(project_router,
                                          r'issues',
                                          lookup='issue')
issue_router.register(r'comments', CommentsViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('signup/', CreateUserAPIView.as_view(), name='signup'),
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
]
