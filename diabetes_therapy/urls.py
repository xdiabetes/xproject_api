from django.urls import path

from diabetes_therapy.views import TherapyTypeCreateView

app_name = "diabetes_therapy"

urlpatterns = [
    path('type/create/', TherapyTypeCreateView.as_view(), name='therapy_type_create'),

]