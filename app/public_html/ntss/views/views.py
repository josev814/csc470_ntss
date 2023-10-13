from jinja2 import Environment, FileSystemLoader, select_autoescape

class Views():

    template = None
    platformName = 'NTSS'
    templateVars = {
        'platformName': platformName,
    }

    def set_template(self, template_name: str, templates_path:str='/var/www/html/public_html/ntss/templates'):
        """
        Load the template
        """
        env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.template = env.get_template(template_name)
