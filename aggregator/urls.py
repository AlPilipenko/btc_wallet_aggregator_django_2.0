from django.urls import path
from . import views # '.' means current folders

"""route urls to certain location so they can be handles by certain way"""
"""goes to URL admin, then logic in admin.site.urls handels the route further"""
urlpatterns = [
    # leave first argument(path) empty since its home page
    # specify the view(function created in views) that will handle the logic
    # name -
    path('', views.home, name='aggregator-home'),
    # path('tests', views.tests, name='aggregator-tests'),
    path('about/', views.about, name='aggregator-about'), #  name='aggregator-about' - important for URLs lookup(in home.html)
    path('agg-func/', views.agg_func, name='aggregator-agg_func'),  # leave trailing /
    path('cat-func/', views.cat_func, name='aggregator-cat_func'),
    path('plot-func/', views.plot_func, name='aggregator-plot_func'),
    path('wallets_list/', views.wallets_list, name='aggregator-wallets_list'),
    path('light_theme/', views.light_theme,
                                        name='aggregator-light_theme'),
    path('dark_theme/', views.dark_theme,
                                        name='aggregator-dark_theme'),
    path('wallets_list_maker_func/', views.wallets_list_maker_func,
                                        name='aggregator-wallets_list_maker_func'),


]
