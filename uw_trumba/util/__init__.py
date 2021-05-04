# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.util.decorators import use_mock
from uw_trumba.dao import (
    TrumbaCalendar_DAO, TrumbaSea_DAO, TrumbaBot_DAO, TrumbaTac_DAO)


fdao_trumba_override = use_mock(TrumbaCalendar_DAO())
fdao_trumba_sea_override = use_mock(TrumbaSea_DAO())
fdao_trumba_bot_override = use_mock(TrumbaBot_DAO())
fdao_trumba_tac_override = use_mock(TrumbaTac_DAO())
