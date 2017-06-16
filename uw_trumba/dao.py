import logging
import os
from os.path import abspath, dirname
from restclients_core.dao import DAO


class TrumbaCalendar_DAO(DAO):
    def service_name(self):
        return 'trumba_cal'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]


class TrumbaSea_DAO(DAO):
    def service_name(self):
        return 'trumba_sea'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def _edit_mock_response(self, method, url, headers, body, response):
        if "POST" == method or "PUT" == method:
            if response.status != 400:
                path = "%s/resources/%s/file%s.%s" % (
                    abspath(dirname(__file__)), self.service_name(),
                    url, method)

                try:
                    handle = open(path)
                    response.data = handle.read()
                    response.status = 200
                except IOError:
                    response.status = 404
        elif "DELETE" == method:
            response.status = 200


class TrumbaBot_DAO(TrumbaSea_DAO):
    def service_name(self):
        return 'trumba_bot'


class TrumbaTac_DAO(TrumbaSea_DAO):
    def service_name(self):
        return 'trumba_tac'
