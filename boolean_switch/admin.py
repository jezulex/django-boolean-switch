from django.db.models import BooleanField
from django.forms import widgets
try:
    # Django 1.8
    from django.core.exceptions import FieldDoesNotExist
except ImportError:
    # Django 1.7
    from django.db.models.fields import FieldDoesNotExist


def boolean_switch_field(field):
    def _f(self):
        v = getattr(self, field.name)
        url = '%d/%s/switch/' % (self._get_pk_val(), field.name)
        return '<a href ="%s" class="boolean_switch"><img src="/static/admin/img/icon-%s.svg" alt="%d" /></a>' % (url, ('no','yes')[v], v)
    _f.short_description = field.verbose_name
    _f.allow_tags = True
    return _f


class AdminBooleanMixin(object):
    """
    Change boolean fields presence in list
    """

    @property
    def media(self):
        m = super(AdminBooleanMixin, self).media
        return m + widgets.Media(js=('boolean_switch/boolean_switch.js',))

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        list_display = []
        for field_name in self.list_display:
            try:
                db_field = self.model._meta.get_field(field_name)
                if isinstance(db_field, BooleanField):
                    field_name = boolean_switch_field(db_field)
            except FieldDoesNotExist:
                pass
            list_display.append(field_name)
        return list_display

    def get_list_display_links(self, request, list_display):
        """
        Return a sequence containing the fields to be displayed as links
        on the changelist. The list_display parameter is the list of fields
        returned by get_list_display().
        """
        list_display = super(AdminBooleanMixin, self).get_list_display_links(request, list_display)
        return list_display if isinstance(list_display, list) else [list_display]

