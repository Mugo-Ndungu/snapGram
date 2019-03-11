from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^about/$', core_views.about, name='about'),
    url(r'^register/$', core_views.register, name='register'),
    url(r'^profile/$', core_views.profile, name='profile'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(
        template_name='registration/logout.html'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
