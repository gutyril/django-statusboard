from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import versioning

from .models import Service, ServiceGroup, Incident, IncidentUpdate, Maintenance
from .serializers import ServiceSerializer, ServiceGroupSerializer, IncidentSerializer, IncidentUpdateSerializer
from .forms import IncidentForm, IncidentUpdateFormSet, ServiceGroupForm, ServiceForm


def index(request):
    from django.db.models import Count
    return render(request, "statusboard/index.html", {
        "statusgroups": ServiceGroup.objects.annotate(services_count=Count('service')).filter(services_count__gt=0),
        "worst_status": Service.objects.worst_status(),
        "incidents": Incident.objects.occurred_in_last_n_days(7).order_by('-modified'),
        "maintenances": Maintenance.objects.filter(scheduled__gt=timezone.now()).order_by('-scheduled'),
    })


class ServiceGroupCreate(PermissionRequiredMixin, CreateView):
    model = ServiceGroup
    form_class = ServiceGroupForm
    template_name = "statusboard/servicegroup/create.html"
    success_url = reverse_lazy('statusboard:index')
    permission_required = 'statusboard.create_servicegroup'


class ServiceGroupUpdate(PermissionRequiredMixin, UpdateView):
    model = ServiceGroup
    form_class = ServiceGroupForm
    template_name = "statusboard/servicegroup/edit.html"
    success_url = reverse_lazy('statusboard:index')
    permission_required = 'statusboard.edit_servicegroup'


class ServiceGroupDelete(PermissionRequiredMixin, DeleteView):
    model = ServiceGroup
    template_name = "statusboard/servicegroup/confirm_delete.html"
    success_url = reverse_lazy('statusboard:index')
    permission_required = 'statusboard.delete_servicegroup'


class ServiceCreate(PermissionRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "statusboard/service/create.html"
    success_url = reverse_lazy('statusboard:index')
    permission_required = 'statusboard.create_service'


class ServiceUpdate(PermissionRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "statusboard/service/edit.html"
    success_url = reverse_lazy('statusboard:index')
    permission_required = 'statusboard.edit_service'


class ServiceDelete(PermissionRequiredMixin, DeleteView):
    model = Service
    template_name = "statusboard/service/confirm_delete.html"
    success_url = reverse_lazy('statusboard:index')
    permission_required = 'statusboard.delete_service'


@permission_required('statusboard.create_incident')
def incident_create(request):
    form = IncidentForm()
    incident_updates = IncidentUpdateFormSet()
    if request.POST:
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident_updates = IncidentUpdateFormSet(request.POST, instance=incident)
            if incident_updates.is_valid():
                incident.save()
                incident_updates.save()
                return HttpResponseRedirect(reverse('statusboard:index'))

    return render(request, "statusboard/incident/create.html", {
        "form": form,
        "incident_updates": incident_updates,
    })


@permission_required('statusboard.change_incident')
def incident_edit(request, pk):
    incident = Incident.objects.get(pk=pk)
    form = IncidentForm(instance=incident)
    incident_updates = IncidentUpdateFormSet(instance=incident)

    if request.POST:
        form = IncidentForm(request.POST or None, instance=incident)
        if form.is_valid():
            incident = form.save(commit=False)
            incident_updates = IncidentUpdateFormSet(request.POST, request.FILES, instance=incident)
            if incident_updates.is_valid():
                incident.save()
                incident_updates.save()
                return HttpResponseRedirect(reverse('statusboard:index'))

    return render(request, "statusboard/incident/edit.html", {
        "form": form,
        "incident_updates": incident_updates,
    })


class IncidentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Incident
    template_name = "statusboard/incident/confirm_delete.html"
    success_url = reverse_lazy('statusboard:index')
    permission_required = 'statusboard.delete_incident'


class IncidentMonthArchiveView(MonthArchiveView):
    queryset = Incident.objects.all()
    date_field = "occurred"
    allow_future = False
    month_format = "%m"
    template_name = "statusboard/incident/archive_month.html"


    def get_year(self):
        try:
            return super(IncidentMonthArchiveView, self).get_year()
        except Http404:
            return str(self.get_queryset().latest(self.date_field).occurred.year)

    def get_month(self):
        try:
            return super(IncidentMonthArchiveView, self).get_month()
        except Http404:
            return str(self.get_queryset().latest(self.date_field).occurred.month)


class ServiceGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceGroupSerializer
    queryset = ServiceGroup.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    versioning_class = versioning.URLPathVersioning


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    versioning_class = versioning.URLPathVersioning


class IncidentViewSet(viewsets.ModelViewSet):
    serializer_class = IncidentSerializer
    queryset = Incident.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    versioning_class = versioning.URLPathVersioning


class IncidentUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = IncidentUpdateSerializer
    queryset = IncidentUpdate.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    versioning_class = versioning.URLPathVersioning
