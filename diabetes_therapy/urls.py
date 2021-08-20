from django.urls import path

from diabetes_therapy.views import TherapyCategoryCreateView, TherapyCategoryListView, TherapyCreateView

app_name = "diabetes_therapy"

urlpatterns = [
    path('category/create/', TherapyCategoryCreateView.as_view(), name='therapy_category_create'),
    path('category/basic/list/', TherapyCategoryListView.as_view(), name='therapy_category_list_basic'),
    path('therapy/<therapy_mode>/create/', TherapyCreateView.as_view(), name='therapy_create'),
]