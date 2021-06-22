from django.apps import apps
from django.core.management.base import BaseCommand

from Apps.Budget.utils.import_settings import ImportData


class Command(BaseCommand):
    def add_arguments(self, request):
        request.add_argument('--url', type=str, required=True, help='URL для запроса')
        request.add_argument('--model', type=str, required=True, help='Модель для загрузки данных')
        request.add_argument('--pageNum', type=str, help='Номер страницы')
        request.add_argument('--pageSize', type=str, help='Размер страницы')
        request.add_argument('--filterstatus', type=str, choices=['ACTIVE', 'ARCHIVE'], help='Фильтрация по статусу')

    def handle(self, *args, **options):
        url = options.pop('url')
        model_name = options.pop('model')
        model = apps.get_model('Budget', model_name)
        filtered_options = {k: v for k, v in options.items() if v}
        import_conf = ImportData(url, model, **filtered_options)
        import_conf.import_data()
