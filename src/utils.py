# -*- coding: utf-8 -*-


class Pagination(object):

    def __init__(self, model, page, count_per_page):
        self.model = model
        self.page = page
        self.count_per_page = count_per_page
        self.total_count = self.get_items_count()

    @property
    def pages(self):
        return int(round(float(self.total_count) / self.count_per_page))

    def iter_pages(self):
        for num in xrange(1, self.pages + 1):
            yield num

    def get_items_count(self):
        return self.model.query.count()

    def get_items(self):
        return self.model.query.limit(self.count_per_page).offset((self.page - 1) * \
            self.count_per_page).all()
