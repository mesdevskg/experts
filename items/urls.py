from django.urls import path

from items.views import *

urlpatterns = [
    path('history/', HistoryListView.as_view(), name='history_list'),
    path('history/<int:pk>/', HistoryDetailView.as_view(), name='history_detail'),
    path('expert/', ExpertListView.as_view(), name='expert_list'),
    path('expert/<int:pk>/', ExpertDetailView.as_view(), name='expert_detail'),
]
