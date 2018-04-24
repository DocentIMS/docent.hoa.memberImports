# -*- coding: utf-8 -*-
from datetime import datetime
from plone import api
from docent.hoa.memberImport.configlet import IImportContactsSettings

def logImportReport(status_code, member_email):
    status_code_lookup_dict = {'missing_email': u'Missing Import Email. Could not import <%s>.' % member_email,
                               'member_overwritten': u'Member data for <%s> overwritten.' % member_email,
                               'member_preexists': u'Member <%s> pre-exists. No action taken.' % member_email,
                               'member_created': u'Member <%s> created' % member_email}
    report_log = api.portal.get_registry_record(name='report_log', interface=IImportContactsSettings, default=[])
    report_log.append(u'%s - %s' % (datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                                    status_code_lookup_dict.get(status_code) or 'Unknown Action'))

    api.portal.set_registry_record(name='report_log',
                                   value=report_log,
                                   interface=IImportContactsSettings)

def updateHomeOwner(lot_id, member_data, portal=None):
    if not portal:
        portal = api.portal.get()

    inspection_tool = portal.get('the-meadows-annual-property-inspection') or None
    if not inspection_tool:
        api.portal.show_message(message="Could Not Update Home: %s" % lot_id,
                                request=portal.REQUEST,
                                type='warn')
        return

    member_home = inspection_tool[lot_id]
    setattr(member_home, 'owner_one', member_data.getUserName())
    member_home.reindexObject()
