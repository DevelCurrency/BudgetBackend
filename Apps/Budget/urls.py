from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Apps.Budget.views import BudgetViewSet, GlavBudgetClasstViewSet, BudgetIncomeViewSet

router = DefaultRouter()
router.register('budget', BudgetViewSet, 'budget')
router.register('glavbudgetclass', GlavBudgetClasstViewSet, 'glavbudgetclass')
router.register('budgetincome', BudgetIncomeViewSet, 'budgetincome')


urlpatterns = [
    path('', include(router.urls)),
]