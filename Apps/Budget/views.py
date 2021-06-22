from django.shortcuts import render
from rest_framework import viewsets
from .models import Budget, GlavBudgetClass
from .serializers import GlavBudgetValidate, BudgetValidate
from Apps.Budget.utils.import_settings import ImportData
from django.apps import apps


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = GlavBudgetValidate


class GlavBudgetClasstViewSet(viewsets.ModelViewSet):
    queryset = GlavBudgetClass.objects.all()
    serializer_class = BudgetValidate


def ImportRun(request):
    if request.POST.get("run_import"):
        import_url = request.POST.get('import_url')
        import_model = request.POST.get('import_model')
        import_status = request.POST.get('status')
        import_pageNum = request.POST.get('page_num')
        import_pageSize = request.POST.get('page_size')

        options = {'filterstatus': import_status,
                   'pageNum': import_pageNum,
                   'pageSize': import_pageSize,
                   }
        # print(options)
        # url = options.pop('url')
        # model_name = options.pop('model')
        model = apps.get_model('Budget', import_model)
        filtered_options = {k: v for k, v in options.items() if v}
        # print(filtered_options)
        import_conf = ImportData(import_url, model, **filtered_options)
        import_conf.import_data()

    return render(request, 'content_main.html', {})
