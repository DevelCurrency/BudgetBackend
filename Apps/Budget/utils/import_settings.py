from urllib.parse import urlsplit, urlencode, parse_qs
from .date_normalize import date_normalize
from Apps.Budget.models import Budget
import requests


class ImportData:
    def __init__(self, url, model, **kwargs):
        self.url = url
        self.model = model
        self.kwargs = kwargs

    def get_url(self):
        # нормализация url
        parsed_url = urlsplit(self.url)
        query = parse_qs(parsed_url.query)
        query.update(**self.kwargs)
        new_query = urlencode(query, doseq=True)
        parsed_url = parsed_url._replace(query=new_query)
        return parsed_url.geturl()

    def get_page_data(self):
        # Получаем данные для импорта
        page_url = self.get_url()
        response = requests.get(page_url)
        return response.json()['data']

    def get_import_data(self):
        # Пунтк ТЗ №3
        # api позволяет получать данные только постранично, для реализации импорта
        # необходимо обеспечить автоматическое получение всех страниц
        if 'pageNum' in self.kwargs:
            data = self.get_page_data()
            yield data
        else:
            page_num = 1
            while True:
                self.kwargs.update({'pageNum': page_num})
                data = self.get_page_data()
                if not data:
                    break
                yield data
                page_num += 1

    def validate_data(self, data):
        import_data = self.filter_data_fields(data)
        self.empty_data_field(import_data, 'startdate')
        self.empty_data_field(import_data, 'enddate')
        if 'parentcode' in import_data:
            # обработка 5 пункта ТЗ:
            self.replace_parentcode(import_data)
        if 'budgetname' in import_data:
            # название бюджета
            self.replace_budgetname(import_data)
        startdate = import_data.get('startdate')
        enddate = import_data.get('enddate')
        if startdate:
            import_data['startdate'] = date_normalize(startdate)
        if enddate:
            import_data['enddate'] = date_normalize(enddate)
        return import_data

    @staticmethod
    def empty_data_field(data, field):
        if not data[field]:
            data[field] = None
        return data

    def replace_parentcode(self, data):
        # обработка 5 пункта ТЗ:
        # Для элементов, у которых в данных, получаемых через API, указан parentcode,
        # при импорте это поле должно заполняться не оригинальным значением, а id элемента соответствующей записи в базе данных
        parentcode = data.get('parentcode')
        new_parentcode = self.model.get_by_code(parentcode)
        data['parentcode'] = new_parentcode
        self.empty_data_field(data, 'parentcode')
        return data

    def replace_budgetname(self, data):
        budgetname = data['budgetname'].capitalize()
        new_budgetname = Budget.get_by_name(budgetname)
        data['budgetname'] = new_budgetname
        return data

    def filter_data_fields(self, data):
        # Фильтрация данных под соответствующую модель
        model_fields = self.model.get_field_names()
        return {k: data[k] for k in model_fields}

    def compare_db_obj_with_import_data(self, obj_from_db, import_data):
        obj_attrs = {attr: getattr(obj_from_db, attr) for attr in self.model.get_field_names()}
        return obj_attrs == import_data

    def import_data(self):
        # Пунтк ТЗ №1
        # Импорт в модель Budget (Приложение 1) данных из api
        data = self.get_import_data()
        for d in data:
            for i in d:
                import_data = self.validate_data(i)
                code = import_data['code']
                obj_from_db = self.model.get_by_code(code)
                if not obj_from_db:
                    self.model.objects.create(**import_data)
                else:
                    if not self.compare_db_obj_with_import_data(obj_from_db, import_data):
                        self.model.objects.filter(id=obj_from_db.id).update(**import_data)
                    continue
