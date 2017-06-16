from commonconf import override_settings

FTRUMBA = 'restclients.dao_implementation.trumba.CalendarFile'
fdao_trumba_override = override_settings(
    RESTCLIENTS_CALENDAR_DAO_CLASS=FTRUMBA)

FTRUMBA_SEA = 'restclients.dao_implementation.trumba.FileSea'
fdao_trumba_sea_override = override_settings(
    RESTCLIENTS_TRUMBA_SEA_DAO_CLASS=FTRUMBA_SEA)

FTRUMBA_BOT = 'restclients.dao_implementation.trumba.FileBot'
fdao_trumba_bot_override = override_settings(
    RESTCLIENTS_TRUMBA_BOT_DAO_CLASS=FTRUMBA_BOT)

FTRUMBA_TAC = 'restclients.dao_implementation.trumba.FileTac'
fdao_trumba_tac_override = override_settings(
    RESTCLIENTS_TRUMBA_TAC_DAO_CLASS=FTRUMBA_TAC)
