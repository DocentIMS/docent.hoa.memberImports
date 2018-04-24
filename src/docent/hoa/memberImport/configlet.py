# -*- coding: utf-8 -*-
import csv
import datetime
from plone import api
from plone.app.registry.browser import controlpanel
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from plone.protect.utils import addTokenToUrl
from zope import schema
from z3c.form import button
from z3c.form import interfaces

import logging
logger = logging.getLogger("Plone")

from docent.hoa.memberImport import _

def defaultList():
    return list()

class IImportContactsSettings(form.Schema):
    """
    Uses IDublinCore
    """

    # csv_import_file = NamedBlobFile(
    #     title=_(u"CSV Import File"),
    #     description=_(u"Please attach the Member CSV File."),
    #     required=False)

    # overwrite_csv = schema.Bool(title=_(u"Overwrite Contacts"),
    #                             description=_(u"Toggling this on to overwrite conflicting accounts, otherwise "
    #                                           u"conflicting accounts will be created and logged instead of being"
    #                                           u"attached to a home."),
    #                             required=False,
    #                             default=False)

    form.mode(clear_report='hidden')
    clear_report = schema.Bool(title=_(u"Clear Report"),
                                description=_(u"Check this and save to remove the existing report log."),
                                required=False,
                                default=False)

    form.mode(report_log='display')
    report_log = schema.List(title=_(u'Report Log'),
                               description=_(u''),
                               value_type=schema.TextLine(),
                               required=False,
                               defaultFactory=defaultList)

class HOAMemberImportSettings(controlpanel.RegistryEditForm):

    schema = IImportContactsSettings
    label = _(u"HOA Member Import")
    description = _(u'')

    def update(self):
        super(HOAMemberImportSettings, self).update()
        description = u"This form imports home owners from a csv file. <a href='%s/@@csv_member_import'>Member " \
                      u"Upload Form</a>" % api.portal.get().absolute_url()

        self.description = description

    def updateFields(self):
        super(HOAMemberImportSettings, self).updateFields()


    def updateWidgets(self):
        try:
            report_log = api.portal.get_registry_record(name='report_log',
                                                        interface=IImportContactsSettings,
                                                        default=[])
        except Exception as e:
            logger.warn("HOA Member Import Error! Could not get existing report log, error: %s" % e)
            report_log = []

        if report_log:
            fields = self.fields
            fields['clear_report'].mode = interfaces.INPUT_MODE

        super(HOAMemberImportSettings, self).updateWidgets()

class HOAMemberImportSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = HOAMemberImportSettings