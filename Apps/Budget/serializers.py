from rest_framework import serializers
from .models import Budget, GlavBudgetClass, BudgetIncome


class BudgetValidate(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['code',
                  'name',
                  'parentcode',
                  'startdate',
                  'status',
                  'budgtypecode']


class GlavBudgetValidate(serializers.ModelSerializer):
    class Meta:
        model = GlavBudgetClass
        fields = ['code',
                  'name',
                  'startdate',
                  'enddate',
                  'budgetname']


class BudgetIncomeValidate(serializers.ModelSerializer):
    class Meta:
        model = BudgetIncome
        fields = ['code',
                  'name',
                  'startdate',
                  'enddate',
                  'budgetname',
                  'ppocode']