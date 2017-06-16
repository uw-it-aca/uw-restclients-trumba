from unittest import TestCase
from uw_trumba import get_calendar_by_name
from uw_trumba.util import fdao_trumba_override


@fdao_trumba_override
class TestCalendarParse(TestCase):

    def test_ical_parsing(self):
        calendar = get_calendar_by_name('sea_acad-comm')
        self.assertEquals(len(calendar.walk('vevent')), 4)
