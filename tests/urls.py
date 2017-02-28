from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('spectator.urls', namespace='spectator')),
]

