from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect

urlpatterns = [
    path('', lambda request: HttpResponseRedirect('/polls/')),  # Redirect root to /polls/
    path('polls/', include('pollsapp.urls')),
    path('admin/', admin.site.urls),
]
