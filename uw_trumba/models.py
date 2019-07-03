import json
from restclients_core import models


EDITOR = 'editor'
SHOWON = 'showon'
EDITOR_GROUP_DESC =\
     "Specifying who can add/edit/delete events on this calendar"
SHOWON_GROUP_DESC =\
    "Specifying the groups whose members have the showon permissions" +\
    " on this calendar"
ADMIN_GROUP_NAME = 'u_eventcal_support'


def get_group_admin():
    return ADMIN_GROUP_NAME


def is_bot(campus_code):
    return campus_code is not None and\
        campus_code == TrumbaCalendar.BOT_CAMPUS_CODE


def is_sea(campus_code):
    return campus_code is not None and\
        campus_code == TrumbaCalendar.SEA_CAMPUS_CODE


def is_tac(campus_code):
    return campus_code is not None and\
        campus_code == TrumbaCalendar.TAC_CAMPUS_CODE


def is_valid_campus_code(campus_code):
    return is_bot(campus_code) or is_sea(campus_code) or is_tac(campus_code)


def is_editor(group_type):
    # group_type: editor or showon in lower case
    return group_type is not None and group_type == EDITOR


def is_showon(group_type):
    # group_type: editor or showon in lower case
    return group_type is not None and group_type == SHOWON


def get_group_desc(group_type):
    if is_editor(group_type):
        return EDITOR_GROUP_DESC
    else:
        return SHOWON_GROUP_DESC


class TrumbaCalendar(models.Model):
    SEA_CAMPUS_CODE = 'sea'
    BOT_CAMPUS_CODE = 'bot'
    TAC_CAMPUS_CODE = 'tac'
    CAMPUS_CHOICES = (
        (SEA_CAMPUS_CODE, 'Seattle'),
        (BOT_CAMPUS_CODE, 'Bothell'),
        (TAC_CAMPUS_CODE, 'Tacoma')
        )
    calendarid = models.PositiveIntegerField()
    campus = models.CharField(max_length=3,
                              choices=CAMPUS_CHOICES,
                              default=SEA_CAMPUS_CODE)
    name = models.CharField(max_length=196, default=None)

    def get_group_admin(self):
        return get_group_admin()

    def get_group_desc(self, group_type):
        # group_type: editor or showon in lower case
        return get_group_desc(group_type)

    def get_group_name(self, group_type):
        # group_type: editor or showon in lower case
        return "u_eventcal_{0}_{1}-{3}".format(super.campus,
                                               super.calendarid,
                                               group_type)

    def get_group_title(self, group_type):
        # group_type: editor or showon in lower case
        return "{0} calendar {1} group".format(super.name, group_type)

    def is_bot(self):
        return is_bot(self.campus)

    def is_sea(self):
        return is_sea(self.campus)

    def is_tac(self):
        return is_tac(self.campus)

    def add_permission(self, permission):
        self.permissions.append(permission)

    def to_json(self):
        perm_json = []
        for perm in self.permissions:
            perm_json.append(perm.to_json())
        return {'calendarid': self.calendarid,
                'campus': self.campus,
                'name': self.name,
                'permissions': perm_json}

    def __eq__(self, other):
        return self.calendarid == other.calendarid

    def __lt__(self, other):
        return (self.campus == other.campus and
                self.name < other.name)

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        super(TrumbaCalendar, self).__init__(*args, **kwargs)
        self.permissions = []
        # Expect a list of Permission objects sorted by
        # descending level and ascending uwnetid


class Permission(models.Model):
    PUBLISH = 'PUBLISH'
    EDIT = 'EDIT'
    REPUBLISH = 'REPUBLISH'
    SHOWON = 'SHOWON'
    VIEW = 'VIEW'
    NONE = 'NONE'
    LEVEL_CHOICES = ((EDIT, 'Can add, delete and change content'),
                     (PUBLISH, 'Can view, edit and publish'),
                     (REPUBLISH, 'Can view, edit and republish'),
                     (SHOWON, 'Can view and show on'),
                     (VIEW, 'Can view content'),
                     (NONE, 'None'))
    calendar = models.ForeignKey(TrumbaCalendar)
    uwnetid = models.CharField(max_length=32)
    name = models.CharField(max_length=96, default=None)
    level = models.CharField(max_length=6, choices=LEVEL_CHOICES, default=VIEW)

    def get_calendarid(self):
        return self.calendar.calendarid

    def get_campus_code(self):
        return self.calendar.campus

    def get_trumba_userid(self):
        return "{0}@washington.edu".format(self.uwnetid)

    def is_bot(self):
        return self.calendar.is_bot()

    def is_sea(self):
        return self.calendar.is_sea()

    def is_tac(self):
        return self.calendar.is_tac()

    def is_edit(self):
        return self.level is not None and self.level == Permission.EDIT

    def is_showon(self):
        return self.level is not None and self.level == Permission.SHOWON

    def is_publish(self):
        return self.level is not None and self.level == Permission.PUBLISH

    def is_republish(self):
        return self.level is not None and self.level == Permission.REPUBLISH

    def is_view(self):
        return self.level is not None and self.level == Permission.VIEW

    def is_higher_permission(self, level):
        # Return True if self.level is higher than the given level
        return (self.is_publish() and
                level != Permission.PUBLISH or
                self.is_edit() and
                level != Permission.PUBLISH and
                level != Permission.EDIT or
                self.is_showon() and
                level == Permission.VIEW)

    def in_editor_group(self):
        return self.is_edit() or self.is_publish()

    def in_showon_group(self):
        return self.is_showon() or self.is_republish()

    def to_json(self):
        return {'uwnetid': self.uwnetid,
                'name': self.name,
                'level': self.level}

    def __eq__(self, other):
        return (self.calendar == other.calendar and
                self.uwnetid == other.uwnetid and
                self.name == other.name and self.level == other.level)

    def __lt__(self, other):
        return (self.calendar == other.calendar and
                (self.is_higher_permission(other.level) or
                 self.level == other.level and
                 self.uwnetid < other.uwnetid))

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        super(Permission, self).__init__(*args, **kwargs)
