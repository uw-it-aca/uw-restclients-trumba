# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Exceptions when Trumba's Web services returns an error in
a successful request.
"""


class TrumbaException(Exception):

    def __init__(self, message, code):
        self.message = "{} ==> {}".format(message, code)

    def __str__(self):
        return "{}: {}".format(self.message, self.__class__.__name__)


class AccountNameEmpty(TrumbaException):
    """
    Exception when creating an account with an empty name
    Coresponding to Trumba error code: 3016
    """
    pass


class AccountNotExist(TrumbaException):
    """
    Exception when the account has not been created
    Coresponding to Trumba error code: 3008
    """
    pass


class AccountUsedByDiffUser(TrumbaException):
    """
    Exception when the account already been used for another user
    Coresponding to Trumba error code: 3009 or 3013
    """
    pass


class CalendarNotExist(TrumbaException):
    """
    Exception when the given calendar ID doesn't exist.
    Coresponding to Trumba error code: 3006
    """
    pass


class CalendarOwnByDiffAccount(TrumbaException):
    """
    Exception when the given calendar ID beongs to a different account.
    Coresponding to Trumba error code: 3007
    """
    pass


class ErrorCreatingEditor(TrumbaException):
    """
    Exception when other errors occur on a creating editor request
    """
    pass


class FailedToClosePublisher(TrumbaException):
    """
    Exception when the account to close is a publisher account
    Coresponding to Trumba error code: 3011
    """
    pass


class InvalidEmail(TrumbaException):
    """
    Exception when creating an account with an invalid email address
    Coresponding to Trumba error code: 3014
    """
    pass


class InvalidPermissionLevel(TrumbaException):
    """
    Exception when the permission level is not valid
    Coresponding to Trumba error code: 3010
    """
    pass


class NoAllowedPermission(TrumbaException):
    """
    Exception when the permission level is not allowed for this account
    Coresponding to Trumba error code: 3015
    """
    pass


class NoDataReturned(TrumbaException):
    """
    Exception when there is empty data in the response
    """
    pass


class UnknownError(TrumbaException):
    """
    Exception when no ResponseMessage or no error code presents
    """
    pass


class UnexpectedError(TrumbaException):
    """
    Exception when the error code is not expected with this request
    """
    pass
