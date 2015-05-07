import urlparse

from rest_framework.relations import HyperlinkedRelatedField


class RelativePathMixin(object):

    def get_url(self, *args, **kwargs):
        url = super(RelativePathMixin, self).get_url(*args, **kwargs)
        parsed = urlparse.urlparse(url)
        return parsed.path


class PathRelatedField(RelativePathMixin, HyperlinkedRelatedField):
    pass
