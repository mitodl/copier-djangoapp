"""
{{ project_name }} views
"""
from django.shortcuts import render


def index(request):
    """
    The index view.
    """
    return render(request, "index.html")
