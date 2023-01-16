from django.contrib.auth import authenticate, login, logout
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    HttpResponseNotAllowed,
    Http404,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import (
    User,
    Member,
    Project,
    Milestone,
    MilestoneTask,
    Organization,
    STATUS_CHOICES,
    PRIORITY_CHOICES,
)
from django.db import IntegrityError
import json
from .forms import OrganizationLoginForm

# Create your views here.
from django.urls import reverse


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(
                request,
                "tasks/pages/sign-in.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "tasks/pages/sign-in.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            member = Member.objects.create(user=user)
            member.save()
        except IntegrityError:
            return render(
                request,
                "tasks/pages/sign-up.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "tasks/pages/sign-up.html")


@login_required
def profile_view(request, username):
    profile_user = User.objects.get_by_natural_key(username)

    form = OrganizationLoginForm()
    context = {
        "profile_user": profile_user,
        "form": form,
        "status_choices": STATUS_CHOICES,
        "priority_choices": PRIORITY_CHOICES,
    }

    if request.method == "POST":
        form = OrganizationLoginForm(request.POST)
        if form.is_valid():
            try:
                organization = Organization.objects.get(
                    login=form.cleaned_data.get("login")
                )
            except Organization.DoesNotExist:
                context[
                    "organization_form_message"
                ] = "Invalid username and/or password."
                return render(request, "tasks/pages/profile.html", context=context)

            if organization.password == form.cleaned_data.get("password"):
                member = request.user.member
                member.organization = organization
                member.save()

    return render(request, "tasks/pages/profile.html", context=context)


def dashboard_view(request):
    return render(request, "tasks/pages/dashboard.html")


def billing_view(request):
    return render(request, "tasks/pages/billing.html")


def notification_view(request):
    return render(request, "tasks/pages/notifications.html")


def tables_view(request):
    return render(request, "tasks/pages/tables.html")


def template_view(request):
    return render(request, "tasks/pages/template.html")


def typography_view(request):
    return render(request, "tasks/pages/typography.html")


@login_required
def projects_view(request):

    context = {
        "status_choices": STATUS_CHOICES,
        "priority_choices": PRIORITY_CHOICES,
    }

    if request.user.member.organization:
        context["organization"] = request.user.member.organization

    return render(request, "tasks/pages/projects.html", context=context)


@login_required
def project_detail_view(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.user.member in project.organization.members.all():
        context = {
            "project": project,
            "status_choices": STATUS_CHOICES,
            "priority_choices": PRIORITY_CHOICES,
        }
        return render(request, "tasks/pages/project_detail.html", context=context)
    return HttpResponseForbidden()


def add_project_milestone(request, project_id):
    if request.method == "POST":
        member = Member.objects.get(
            user=User.objects.get_by_natural_key(request.POST["assignment"])
        )
        milestone = Milestone.objects.create(
            title=request.POST["title"],
            deadline=request.POST["deadline"],
            status=request.POST["status"],
            priority=request.POST["priority"],
            project=Project.objects.get(pk=project_id),
            assignment=member,
            author=request.user.member,
        )
        milestone.save()

    return HttpResponseRedirect(reverse("project", args=[project_id]))


#################
# Project PUT views
#################


@login_required
def project_put_status(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.user == project.author.user:
        if request.method == "PUT":
            data = json.loads(request.body)
            project.status = data["status"]
            project.save()
            return HttpResponse(status=204)


@login_required
def project_put_priority(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.user == project.author.user:
        if request.method == "PUT":
            data = json.loads(request.body)
            project.priority = data["priority"]
            project.save()
            return HttpResponse(status=204)


@login_required
def project_put_member(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.user == project.author.user:
        if request.method == "PUT":
            data = json.loads(request.body)
            member = Member.objects.get(
                user=User.objects.get_by_natural_key(data["member"])
            )
            if member in project.members.all():
                member_project_milestones = Milestone.objects.filter(
                    project=project, assignment=member
                )
                for milestones in member_project_milestones:
                    milestones.assignment = None
                    milestones.save()
                project.members.remove(member)

            else:
                project.members.add(member)

            return HttpResponse(status=204)


#################
# milestone PUT views
#################


@login_required
def milestone_put_status(request, milestone_id):
    milestone = Milestone.objects.get(pk=milestone_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        milestone.status = data["status"]
        milestone.save()
        return HttpResponse(status=204)


@login_required
def milestone_put_priority(request, milestone_id):
    milestone = Milestone.objects.get(pk=milestone_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        milestone.priority = data["priority"]
        milestone.save()
        return HttpResponse(status=204)


@login_required
def milestone_put_assignment(request, milestone_id):
    milestone = Milestone.objects.get(pk=milestone_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data["assignment"] != "None":
            member = Member.objects.get(
                user=User.objects.get_by_natural_key(data["assignment"])
            )
            milestone.assignment = member
        else:
            milestone.assignment = None
        milestone.save()
        return HttpResponse(status=204)


@login_required
def milestone_remove(request, milestone_id):
    milestone = Milestone.objects.get(pk=milestone_id)
    if request.method == "DELETE":
        if request.user.member in milestone.project.members.all():
            milestone.delete()
            return HttpResponse(status=204)


#################
# milestones PUT views
#################


def milestone_tasks(request, milestone_id):
    milestone = Milestone.objects.get(pk=milestone_id)

    if request.user.member in milestone.project.organization.members.all():
        context = {
            "milestone": milestone,
            "status_choices": STATUS_CHOICES,
            "priority_choices": PRIORITY_CHOICES,
        }
        return render(request, "tasks/pages/milestone_detail.html", context=context)
    return HttpResponseForbidden()


def milestone_tasks_add(request, milestone_id):
    if request.method == "POST":
        milestone = Milestone.objects.get(pk=milestone_id)
        task = MilestoneTask.objects.create(
            title=request.POST["title"], milestone=milestone
        )
        task.save()

    return HttpResponseRedirect(reverse("milestone_tasks", args=[milestone_id]))


def milestone_task_update(request, task_id):
    if request.method == "PUT":
        task = MilestoneTask.objects.get(pk=task_id)
        if request.user == task.milestone.assignment.user:
            if task.complete:
                task.complete = False
            else:
                task.complete = True
            task.save()
            return HttpResponse(status=204)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()
