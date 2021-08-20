from .models import FixTherapy, WithMealTherapy, MixTherapy, Therapy
from .serializes import FixTherapyBaseSerializer

therapy_serializers = {
    Therapy.FIX: FixTherapyBaseSerializer
}
