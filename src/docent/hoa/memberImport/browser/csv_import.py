# -*- coding: utf-8 -*-
from datetime import datetime
import csv
import random
import string
from plone import api
from plone.directives import form
from z3c.form import button, field

from plone import api
from plone.api.exc import MissingParameterError, InvalidParameterError

from docent.hoa.memberImport.app_config import EXPECTED_FIELDNAMES, HOME_OWNERS_GID
from docent.hoa.memberImport.configlet import IImportContactsSettings
from docent.hoa.memberImport.interfaces import IImportMembers
from docent.hoa.memberImport.utils import logImportReport, updateHomeOwner

import logging
logger = logging.getLogger("Plone")
from docent.hoa.memberImport import _


class MemberImportForm(form.SchemaForm):

    label = _(u"Member Import Form")
    schema = IImportMembers
    ignoreContext = True

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, actions):
        api.portal.show_message(message="Member Import Action Cancelled.",
                                request=self.request,
                                type='info')
        return self.request.response.redirect(api.portal.get().absolute_url())

    @button.buttonAndHandler(u"Upload")
    def handleApply(self, actions):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        csv_file = data.get('csv_import_file') or None
        overwrite_csv = data.get('overwrite_csv') or False

        dictreader = csv.DictReader(csv_file.data.splitlines(),
                                    delimiter=',',
                                    quotechar='"')
        fieldnames_actual = [i for i in dictreader.fieldnames if i]
        if sorted(fieldnames_actual) != sorted(EXPECTED_FIELDNAMES):
            api.portal.show_message(message="CSV file does not contain matching headers. "
                                            "We expect: %s" % EXPECTED_FIELDNAMES,
                                    request=self.request,
                                    type='warn')
            self.request.response.redirect(api.portal.get().absolute_url())

        try:
            home_owners_group = api.group.get(groupname=HOME_OWNERS_GID)
        except ValueError:
            home_owners_group = None
        if not home_owners_group:
            api.group.create(groupname=HOME_OWNERS_GID,
                             title='Home Owners')

        for row in dictreader:
            contact_dict = dict()
            email = row.get('Email').strip()
            if not email:
                logImportReport('missing_email', email)
                continue
            name = row.get('Name').strip()
            if ',' in name:
                name_split = name.split(',')
                if len(name_split) == 2:
                    lastname, firstname = name_split
                    fullname = '%s %s' % (firstname.strip(), lastname.strip())
                else:
                    lastname, firstname = name_split[:2]
                    middlenames = [i.strip() for i in name_split[3:]]
                    fullname = '%s %s %s' % (firstname.strip(),
                                             ' '.join(middlenames),
                                             lastname.strip())
            else:
                fullname = name

            fullname = fullname.title()

            lot_id = row.get('Lot #').strip()
            lot_id = lot_id.replace('-', '_')

            property_address = row.get('Property Address')
            if property_address:
                property_address = property_address.strip().title()
            mailing_address = row.get('Mailing Address').strip().title()
            if mailing_address:
                mailing_address = mailing_address.strip().title()
            has_renters = property_address == mailing_address
            if has_renters:
                mailing_city = row.get('City')
                if mailing_city:
                    mailing_city = mailing_city.strip().title()
                mailing_state = row.get('State')
                if mailing_state:
                    mailing_state.strip().upper()
                mailing_zipcode = row.get('Zipcode')
                if mailing_zipcode:
                    mailing_zipcode = mailing_zipcode.strip()
            else:
                mailing_city = ''
                mailing_state = ''
                mailing_zipcode = ''

            password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
            processed_members = []
            #check if member exists:
            try:
                member_data = api.user.get(username=email)
            except MissingParameterError:
                logger.warn("MEMBER IMPORT ERROR: When trying to get member %s, error returned: "
                            "MissingParameterError" % email)
                member_data = None

            if member_data:
                if overwrite_csv:
                    #update their properties
                    member_data.setMemberProperties(mapping={'email':email,
                                                             'fullname': u'%s' % fullname,
                                                             'mailing_address_1': u'%s' % mailing_address.title(),
                                                             'mailing_city': u'%s' % mailing_city.title(),
                                                             'mailing_state': u'%s' % mailing_state.title(),
                                                             'mailing_zipcode': u'%s' % mailing_zipcode})
                    #add to group
                    api.group.add_user(user=member_data, groupname=HOME_OWNERS_GID)

                    #add as homeowner
                    updateHomeOwner(lot_id, member_data)
                    logImportReport('member_overwritten', email)
                else:
                    logImportReport('member_preexists', email)
            else:
                #we need to create this member
                member_data = api.user.create(email=email,
                                              password=password,
                                              properties={'email':email,
                                                          'fullname': u'%s' % fullname,
                                                          'mailing_address_1': u'%s' % mailing_address.title(),
                                                          'mailing_city': u'%s' % mailing_city.title(),
                                                          'mailing_state': u'%s' % mailing_state.title(),
                                                          'mailing_zipcode': u'%s' % mailing_zipcode})
                #add to group
                api.group.add_user(user=member_data, groupname=HOME_OWNERS_GID)

                #add as homeowner
                updateHomeOwner(lot_id, member_data)

                logImportReport('member_created', email)

        api.portal.show_message(message="Members CSV Imported.",
                                request=self.request,
                                type='Info')
        return self.request.response.redirect(api.portal.get().absolute_url())

