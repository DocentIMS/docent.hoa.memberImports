# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from docent.hoa.memberImport import _
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDocentHoaMemberimportLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IImportMembers(form.Schema):
    csv_import_file = NamedBlobFile(
        title=_(u"CSV Import File"),
        description=_(u"Please attach the Member CSV File."),
        required=True)

    overwrite_csv = schema.Bool(title=_(u"Overwrite Contacts"),
                                description=_(u"Toggling this on to overwrite conflicting accounts, otherwise "
                                              u"conflicting accounts will be created and logged instead of being"
                                              u"attached to a home."),
                                required=False,
                                default=False)