from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="/chain")),
    path("mine", views.mine),
    path("transactions/new", views.new_transaction),
    path("chain", views.full_chain),
    path("chain-json", views.full_chain_json),
    path("nodes", views.Node.as_view()),
    path("nodes/resolve", views.consensus),
]
