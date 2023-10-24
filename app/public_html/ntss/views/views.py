"""
This is the base module for Views
All Views should inherit from this class
"""
from jinja2 import Environment, FileSystemLoader, select_autoescape
from ntss.config.constants import US_STATES


class Views:
    """
    This is the base class for Views
    All Views should inherit from this class
    """
    template = None
    _templates_path = '/var/www/html/public_html/ntss/templates'
    _env = Environment()
    platformName = 'NTSS'
    templateVars = {
        'platformName': platformName,
    }

    def set_templates_environment(self, templates_path: str = ''):
        """
        Sets the jinja environment for where templates should be found

        :param templates_path:
        :return:
        """
        if templates_path == '':
            templates_path = self._templates_path

        self._env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def set_template(self, template_name: str, templates_path: str = ''):
        """
        Loads the template requested

        :param template_name:
        :param templates_path:
        :return:
        """
        if templates_path == '':
            templates_path = self._templates_path

        self.set_templates_environment(templates_path)

        self.template = self._env.get_template(template_name)
