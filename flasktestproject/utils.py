# -*- coding: utf-8 -*-
from math import ceil


class Pagination(object):

    def __init__(self, query, page, count_per_page, search_query=None):
        self.query = query
        self.page = page
        self.count_per_page = count_per_page
        self.total_count = self.get_items_count()
        self.search_query = search_query

    @property
    def pages(self):
        return int(ceil(float(self.total_count) / self.count_per_page))

    def iter_pages(self):
        for num in xrange(1, self.pages + 1):
            yield num

    def get_items_count(self):
        return self.query.count()

    def get_items(self):
        return self.query.limit(self.count_per_page).offset((self.page - 1) * \
            self.count_per_page).all()
