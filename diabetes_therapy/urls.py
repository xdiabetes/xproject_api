from django.urls import path

from diabetes_therapy.views import TherapyTypeCreateView, TherapyTypeListView, TherapyCreateView

app_name = "diabetes_therapy"

urlpatterns = [
    path('category/create/', TherapyTypeCreateView.as_view(), name='therapy_category_create'),
    path('category/basic/list/', TherapyTypeListView.as_view(), name='therapy_category_list_basic'),
    path('therapy/<therapy_mode>/create/', TherapyCreateView.as_view(), name='therapy_create'),
]