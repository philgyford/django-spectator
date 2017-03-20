from .core import urlpatterns as core_urlpatterns
from .events import urlpatterns as events_urlpatterns
from .reading import urlpatterns as reading_urlpatterns

urlpatterns = core_urlpatterns
urlpatterns += events_urlpatterns
urlpatterns += reading_urlpatterns

