from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from uw_trumba.calendars import Calendars, _is_valid_calendarid


class TestCalendars(TestCase):

    def test_load(self):
        cals = Calendars()

        self.assertTrue(cals.exists('bot'))

        self.assertEquals(cals.total_calendars('bot'), 3)
        self.assertEquals(cals.total_calendars('sea'), 10)
        self.assertEquals(cals.total_calendars('tac'), 1)

        sorted_cals = cals.get_campus_calendars('sea')
        self.assertEqual(len(sorted_cals), 10)
        self.assertEqual(sorted_cals[0].name, "Seattle calendar")
        self.assertEqual(sorted_cals[1].name,
                         "Seattle calendar >> Seattle child calendar1")

        trumba_cal = cals.get_calendar('sea', 1)
        self.assertEqual(trumba_cal.calendarid, 1)
        self.assertEqual(trumba_cal.campus, 'sea')
        self.assertEqual(trumba_cal.name, 'Seattle calendar')

        self.assertTrue(cals.has_calendar('sea', 1))

        trumba_cal1 = cals.get_calendar('sea', 11321)
        self.assertEqual(trumba_cal1.name,
                         "{}{}{}{}".format('Seattle calendar >> Seattle',
                                           ' child calendar3 >> Seattle',
                                           ' child-sub-calendar32 >> Seattle',
                                           ' child-sub-sub-calendar321'))

        self.assertIsNone(cals.get_campus_calendars('sss'))
        self.assertIsNone(cals.get_calendar('sea', 21))
        self.assertIsNone(cals.get_calendar('sss', 11321))

        cals.campus_calendars['bot'] = {}
        self.assertFalse(cals.exists('bot'))
        self.assertEquals(cals.total_calendars('bot'), 0)

    def test_is_valid_calendarid(self):
        self.assertTrue(_is_valid_calendarid(1))
        self.assertFalse(_is_valid_calendarid(0))
        self.assertFalse(_is_valid_calendarid(-1))
