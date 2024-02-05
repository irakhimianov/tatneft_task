from django.contrib.admin.widgets import AdminFileWidget
from django.db.models.fields import files
from django.forms.renderers import DjangoTemplates
from django.utils.safestring import mark_safe


class AdminImageWidget(AdminFileWidget):
    def render(
            self,
            name: str,
            value: files.ImageFieldFile,
            attrs: dict = None,
            renderer: DjangoTemplates = None,
    ) -> str:
        output = []
        if value and hasattr(value, 'url'):
            output.append(
                f'<a href="{value.url}" target="_blank">'
                f'<img src="{value.url}" alt="{value}" width="90" style="object-fit: fill; margin: 0 20px;"/>'
                f'</a>'
            )
        output.append(super().render(name, value, attrs, renderer))
        return mark_safe(''.join(output))
