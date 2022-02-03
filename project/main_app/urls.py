"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path
from main_app import views
from project import settings

urlpatterns = [
    path('', views.main_page, name='home'),
    path('cases/', views.cases_list, name="cases_list"),
    path('add-case/', views.AddCaseView.as_view(), name='add_case'),
    path('case/<int:pk>/', views.CaseView.as_view()),
    path('case/<int:pk>/edit/', views.EditCaseView.as_view()),
    path('case/<int:pk>/close/', views.CloseCaseView.as_view()),
    path('case/<int:pk>/delete', views.DeleteCaseView.as_view()),
    path('case/<int:case_pk>/comment/', views.AddEditCommentView.as_view()),
    path('case/<int:case_pk>/comment/<int:com_pk>/', views.AddEditCommentView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
