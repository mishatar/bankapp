from django.urls import path, include
from .views import (IncomeViewSet, ExpensesViewSet, GoalsViewSet,
                    WalletApiView, CustomerViewSet, TransferViewSet,
                    AccountViewSet)

from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register(r'income', IncomeViewSet, basename='income')
router.register(r'expenses', ExpensesViewSet, basename='expenses')
router.register(r'goals', GoalsViewSet, basename='goals')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'transfer', TransferViewSet, basename='transfer')
router.register(r'account', AccountViewSet, basename='account')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('wallet/', WalletApiView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]