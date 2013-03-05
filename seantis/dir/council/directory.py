from five import grok
from plone.namedfile.field import NamedImage
from collections import namedtuple

from seantis.dir.base import directory
from seantis.dir.base import utils
from seantis.dir.base.interfaces import IDirectory
from seantis.dir.council import _


class ICouncilDirectory(IDirectory):
    """Extends the seantis.dir.base.directory.IDirectory"""

    image = NamedImage(
        title=_(u'Image'),
        required=False,
        default=None
    )


ICouncilDirectory.setTaggedValue('seantis.dir.base.omitted', [
    'cat1', 'cat2', 'cat3', 'cat4',
    'cat1_suggestions',
    'cat2_suggestions',
    'cat3_suggestions',
    'cat4_suggestions'
])


class CouncilDirectory(directory.Directory):

    def labels(self):
        return {
            'cat1': _(u'Town'),
            'cat2': _(u'Party'),
            'cat3': _(u'Committee'),
            'cat4': _(u'Function'),
        }

    def used_categories(self):
        return ('cat1', 'cat2', 'cat3', 'cat4')

    def unused_categories(self):
        return tuple()


DirectoryTag = namedtuple('DirectoryTag', ['name', 'url'])


class CouncilDirectoryView(directory.View):
    grok.name('view')
    grok.context(ICouncilDirectory)
    grok.require('zope2.View')

    itemsperpage = 250
    template = grok.PageTemplateFile('templates/directory.pt')

    def generate_tags(self, item):

        url = self.context.absolute_url() + '?filter&%s=%s'
        excempted_categories = ['cat3']

        for cat, label, value in item.categories:

            if cat in excempted_categories:
                continue

            for value in utils.flatten(value):
                if not value:
                    continue

                yield DirectoryTag(url=url % (cat, value), name=value)

    def tags(self, item):
        return list(self.generate_tags(item))

    def tag_url(self, tag):
        return self.context.absolute_url() + '?filter&cat1='


class ExtendedDirectoryViewlet(grok.Viewlet):
    grok.context(ICouncilDirectory)
    grok.name('seantis.dir.council.directory.detail')
    grok.require('zope2.View')
    grok.viewletmanager(directory.DirectoryViewletManager)

    template = grok.PageTemplateFile('templates/directorydetail.pt')
