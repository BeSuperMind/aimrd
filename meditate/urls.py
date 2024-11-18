from django.urls import path
from .views import Say, GenerateHRVReport
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", Say.as_view(), name='say'),
    path("generate_hrv_report/", GenerateHRVReport.as_view(), name='Generate_hrv_report' ),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
