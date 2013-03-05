import imghdr

from five import grok

from collective.dexteritytextindexer import searchable
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.directives import form
from plone.namedfile.field import NamedImage
from zope.interface import Invalid
from zope.schema import TextLine, Text

from seantis.dir.base import item
from seantis.dir.base import core
from seantis.dir.base.interfaces import (
    IFieldMapExtender, IDirectoryItem
)

from seantis.dir.council.directory import ICouncilDirectory
from seantis.dir.council import _


class ICouncilDirectoryItem(IDirectoryItem):
    """Extends the seantis.dir.IDirectoryItem."""

    image = NamedImage(
        title=_(u'Image'),
        required=False,
        default=None
    )

    searchable('street')
    street = TextLine(
        title=_(u'Street'),
        required=False,
        default=u''
    )

    searchable('zipcode')
    zipcode = TextLine(
        title=_(u'Zipcode'),
        required=False,
        default=u''
    )

    searchable('city')
    city = TextLine(
        title=_(u'Town'),
        required=False,
        default=u''
    )

    searchable('phone')
    phone = TextLine(
        title=_(u'Phone'),
        required=False,
        default=u''
    )

    searchable('fax')
    fax = TextLine(
        title=_(u'Fax'),
        required=False,
        default=u''
    )

    searchable('information')
    form.widget(information=WysiwygFieldWidget)
    information = Text(
        title=_(u'Information'),
        required=False,
        default=u''
    )


# Ensure that the uploaded image at least has an image header.
@form.validator(field=ICouncilDirectoryItem['image'])
def validate_image(value):
    if not value:
        return

    if not imghdr.what(value.filename, value.data):
        raise Invalid(_(u'Unknown image format'))


class CouncilDirectoryItem(item.DirectoryItem):
    pass


class CouncilDirectoryItemViewlet(grok.Viewlet):
    grok.context(ICouncilDirectoryItem)
    grok.name('seantis.dir.council.item.detail')
    grok.require('zope2.View')
    grok.viewletmanager(item.DirectoryItemViewletManager)

    template = grok.PageTemplateFile('templates/listitem.pt')


class View(core.View):
    """Default view of a seantis.dir.council item."""
    grok.context(ICouncilDirectoryItem)
    grok.require('zope2.View')

    template = grok.PageTemplateFile('templates/item.pt')


class ExtendedDirectoryItemFieldMap(grok.Adapter):
    """Adapter extending the import/export fieldmap of
    seantis.dir.council.item.

    """
    grok.context(ICouncilDirectory)
    grok.provides(IFieldMapExtender)

    def __init__(self, context):
        self.context = context

    def extend_import(self, itemmap):
        itemmap.typename = 'seantis.dir.council.item'
        itemmap.interface = ICouncilDirectoryItem

        extended = [
            'street',
            'zipcode',
            'city',
            'phone',
            'fax'
        ]

        itemmap.add_fields(extended, len(itemmap))
