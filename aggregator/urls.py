from django.urls import path
from . import views # '.' means current folders

"""route urls to certain location so they can be handles by certain way"""
"""goes to URL admin, then logic in admin.site.urls handels the route further"""
urlpatterns = [
    # leave first argument(path) empty since its home page
    # specify the view(function created in views) that will handle the logic
    # name -
    path('', views.home, name='aggregator-home'),
    path('about/', views.about, name='aggregator-about'), #  name='aggregator-about' - important for URLs lookup(in home.html)
    path('agg-func/', views.agg_func, name='aggregator-agg_func'),  # leave trailing /
    path('cat-func/', views.cat_func, name='aggregator-cat_func'),
]
