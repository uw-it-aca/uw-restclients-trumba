"""
This module directly interacts with campus specific web services on
It will log the http requests and responses.
Be sure to set the logging configuration if you use the LiveDao!
"""

import logging
import json
import time
from lxml import etree
from icalendar import Calendar, Event
from restclients_core.exceptions import DataFailureException
from uw_trumba.dao import TrumbaBot_DAO, TrumbaSea_DAO, TrumbaTac_DAO
from uw_trumba.dao import TrumbaCalendar_DAO
from uw_trumba.util import to_bytestring


logger = logging.getLogger(__name__)


def get_calendar_by_name(calendar_name):
    url = "/calendars/%s.ics" % calendar_name

    response = TrumbaCalendar_DAO().getURL(url)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)
    try:
        calendar = Calendar.from_ical(response.data)
    except Exception as ex:
        # turn data errors (ie, UnicodeEncodeError) into
        # DataFailureException
        raise DataFailureException(url, 503, ex)

    return calendar


def _log_xml_resp(campus, url, response):
    if response.status == 200 and response.data is not None:
        logger.info("%s %s ==status==> %s" % (campus, url, response.status))
        root = etree.fromstring(to_bytestring(response.data))
        resp_msg = ''
        for el in root.iterchildren():
            resp_msg += str(el.attrib)
        logger.info("%s %s ==message==> %s" % (campus, url, resp_msg))
    else:
        logger.error("%s %s ==error==> %s %s" % (campus, url,
                                                 response.status,
                                                 response.reason))


def _log_json_resp(campus, url, body, response):
    if response.status == 200 and response.data is not None:
        logger.info("%s %s %s ==status==> %s" % (campus, url, body,
                                                 response.status))
        logger.debug("%s %s %s ==data==> %s" % (campus, url, body,
                                                response.data))
    else:
        logger.error("%s %s %s ==error==> %s %s" % (campus, url, body,
                                                    response.status,
                                                    response.reason))


def get_bot_resource(url):
    """
    Get the requested resource or update resource using Bothell account
    :returns: http response with content in xml
    """
    response = None
    response = TrumbaBot_DAO().getURL(url,
                                      {"Content-Type": "application/xml"})
    _log_xml_resp("Bothell", url, response)
    return response


def get_sea_resource(url):
    """
    Get the requested resource or update resource using Seattle account
    :returns: http response with content in xml
    """
    response = None
    response = TrumbaSea_DAO().getURL(url,
                                      {"Accept": "application/xml"})
    _log_xml_resp("Seattle", url, response)
    return response


def get_tac_resource(url):
    """
    Get the requested resource or update resource using Tacoma account
    :returns: http response with content in xml
    """
    response = None
    response = TrumbaTac_DAO().getURL(url,
                                      {"Accept": "application/xml"})
    _log_xml_resp("Tacoma", url, response)
    return response


def post_bot_resource(url, body):
    """
    Get the requested resource of Bothell calendars
    :returns: http response with content in json
    """
    response = None
    response = TrumbaBot_DAO().postURL(
        url,
        {"Content-Type": "application/json"},
        body)
    _log_json_resp("Bothell", url, body, response)
    return response


def post_sea_resource(url, body):
    """
    Get the requested resource using the Seattle account
    :returns: http response with content in json
    """
    response = None
    response = TrumbaSea_DAO().postURL(
        url,
        {"Content-Type": "application/json"},
        body)
    _log_json_resp("Seattle", url, body, response)
    return response


def post_tac_resource(url, body):
    """
    Get the requested resource of Tacoma calendars
    :returns: http response with content in json
    """
    response = None
    response = TrumbaTac_DAO().postURL(
        url,
        {"Content-Type": "application/json"},
        body)
    _log_json_resp("Tacoma", url, body, response)
    return response
