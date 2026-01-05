from django.urls import path
from .views import (
    EstimateView, ParseMeasurementsView, ProductRecommendationsView, 
    DistributorsView, GenerateQuotePDFView, SaveToCRMView
)

urlpatterns = [
    path('estimate/', EstimateView.as_view(), name='estimate'),
    path('parse-measurements/', ParseMeasurementsView.as_view(), name='parse-measurements'),
    path('recommendations/', ProductRecommendationsView.as_view(), name='product-recommendations'),
    path('distributors/', DistributorsView.as_view(), name='distributors'),
    path('generate-quote/', GenerateQuotePDFView.as_view(), name='generate-quote'),
    path('save-to-crm/', SaveToCRMView.as_view(), name='save-to-crm'),
]
