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

class TrumbaBot_DAO(TrumbaSea_DAO):
    def service_name(self):
        return 'trumba_bot'

class TrumbaTac_DAO(TrumbaSea_DAO):
    def service_name(self):
        return 'trumba_tac'
