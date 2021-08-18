from django.urls import path

from diabetes_therapy.views import TherapyTypeCreateView, TherapyTypeListView

app_name = "diabetes_therapy"

urlpatterns = [
    path('type/create/', TherapyTypeCreateView.as_view(), name='therapy_type_create'),
    path('type/list/', TherapyTypeListView.as_view(), name='therapy_type_list'),
]