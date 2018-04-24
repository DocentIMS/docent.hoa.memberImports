# -*- coding: utf-8 -*-
from docent.hoa.memberImport.configlet import IImportContactsSettings
from plone import api

def registry_modified_event(event):
    record = event.record
    if record.interface == IImportContactsSettings:
        if record.fieldName == 'clear_report':
            if record.value:
                api.portal.set_registry_record(name='clear_report',
                                               value=False,
                                               interface=IImportContactsSettings)

                api.portal.set_registry_record(name='report_log',
                                               value=[],
                                               interface=IImportContactsSettings)


