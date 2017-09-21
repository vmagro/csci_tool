"""Context processors that merge a dictionary into the context of all rendered templates."""

from . import app_settings


def app_info(request):
    """Include some settings that we might want to display in the UI for every request."""
    return {'course_name': app_settings.CLASS_NAME}
