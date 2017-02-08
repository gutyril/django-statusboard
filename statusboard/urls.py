from django.conf.urls import url, include

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'servicegroups', views.ServiceGroupViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'incidents', views.IncidentViewSet)
router.register(r'incidentupdates', views.IncidentUpdateViewSet)

app_name = "statusboard"

servicegroup_urls = [
    url('^create/$',
        views.ServiceGroupCreate.as_view(),
        name="create"),
    url('^(?P<pk>[0-9]+)/edit/$',
        views.ServiceGroupUpdate.as_view(),
        name="edit"),
    url('^(?P<pk>[0-9]+)/delete/$',
        views.ServiceGroupDelete.as_view(),
        name="delete"),
]

incident_urls = [
    url('^archive/$',
        views.IncidentMonthArchiveView.as_view(),
        name="archive-index"),
    url('^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',
        views.IncidentMonthArchiveView.as_view(),
        name="archive-month"),
    url('^create/$',
        views.incident_create,
        name="create"),
    url('^(?P<pk>[0-9]+)/edit/$',
        views.incident_edit,
        name="edit"),
    url('^(?P<pk>[0-9]+)/delete/$',
        views.IncidentDeleteView.as_view(),
        name="delete"),
]

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^servicegroups/', include(servicegroup_urls, namespace="servicegroup")),
    url(r'^incidents/', include(incident_urls, namespace="incident")),
    url(r'^api/(?P<version>v0\.1)/', include(router.urls, namespace="api")),
]
