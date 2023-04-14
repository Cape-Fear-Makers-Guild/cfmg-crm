from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.admin.sites import AdminSite
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Q
from simple_history.admin import SimpleHistoryAdmin
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ObjectDoesNotExist

import datetime
import uuid
import zipfile
import os
import re

import logging

logger = logging.getLogger(__name__)

from members.models import User

from django.views.decorators.csrf import csrf_exempt
from gandalf.decorators import superuser_or_bearer_required

import json
from django.http import JsonResponse
from ipware import get_client_ip

from members.models import User
from acl.models import Machine

from servicelog.models import Servicelog
from servicelog.forms import ServicelogForm

import logging

logger = logging.getLogger(__name__)


@login_required
def servicelog_overview(request, machine_id=None):
    try:
        entries = Servicelog.objects.all()
        if machine_id:
            machine = Machine.objects.get(id=machine_id)
    except ObjectDoesNotExist as e:
        return HttpResponse("Machine not found", status=404, content_type="text/plain")

    if machine_id:
        # Just show ALL entries when dealing with one machine
        entries = entries.filter(machine_id=machine_id).order_by("-last_updated")
        title = "Historic service log for {}".format(machine)
    else:
        # Just show the last/most recent entry for one machine
        entries = (
            entries.order_by("machine", "-last_updated")
            .distinct("machine")
            .order_by("machine")
        )
        title = "Current / most recent service state of all machines"

    context = {
        "title": title,
        "items": entries,
        "has_permission": request.user.is_authenticated,
    }
    return render(request, "overview.html", context)


@login_required
def servicelog_crud(request, machine_id=None, servicelog_id=None):
    try:
        machine = Machine.objects.get(id=machine_id)
        most_recent = (
            Servicelog.objects.all()
            .filter(machine_id=machine_id)
            .order_by("-reported")
            .first()
        )
    except ObjectDoesNotExist as e:
        return HttpResponse("Machine not found", status=404, content_type="text/plain")

    servicelog = None
    if servicelog_id:
        try:
            servicelog = Servicelog.objects.get(id=servicelog_id)
        except ObjectDoesNotExist as e:
            return HttpResponse(
                "Servicelog not found", status=404, content_type="text/plain"
            )
    context = {
        "item": machine,
        "has_permission": request.user.is_authenticated,
    }
    if machine.out_of_order:
        context["title"] = "Report as back in service"
        context["action"] = "Update state"
    else:
        context["title"] = "Report as broken or report a problem"
        context["action"] = "File report"
    # context['action'] = context['title']

    if request.POST:
        form = ServicelogForm(
            request.POST or None,
            request.FILES,
            instance=servicelog,
            canreturntoservice=machine.canInstruct(request.user),
        )
        if form.is_valid():
            try:
                item = form.save(commit=False)
                item.machine = machine
                item.reporter = request.user
                item.changeReason = (
                    "Changed by {} via service log issue reporting".format(request.user)
                )
                item.save()

                old_state = machine.out_of_order
                new_state = form.cleaned_data.get("out_of_order")
                if old_state != new_state and (
                    most_recent == None
                    or item.id == most_recent.id
                    or servicelog_id == None
                ):
                    machine.out_of_order = new_state
                    machine.changeReason = (
                        "Changed by {} via servicelog issue reporting".format(
                            request.user
                        )
                    )
                    machine.save()

            except Exception as e:
                logger.error("Unexpected error during update of tag: {}".format(e))

            return redirect("service_log_view", machine_id=machine.id)

    form = ServicelogForm(
        instance=servicelog, canreturntoservice=machine.canInstruct(request.user)
    )
    if servicelog != None and most_recent != None and servicelog != most_recent:
        form.fields["out_of_order"].disabled = True
        form.fields[
            "out_of_order"
        ].help_text = (
            "Cannot change this - as there is a more recent servicelog entry in force."
        )

    if servicelog:
        form.fields["out_of_order"].value = machine.out_of_order
        form.fields["out_of_order"].help_text = (
            form.fields["out_of_order"].help_text
            + "<p>Shown is the <i>current</i> state of the machine."
        )

    context["form"] = form
    context[
        "back"
    ] = "machine_list"  # reverse("machine_overview", kwargs={"machine_id": machine.id})
    return render(request, "crud.html", context)
