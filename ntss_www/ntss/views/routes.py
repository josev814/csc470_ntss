"""
Package for Route Views
"""
from ntss.views.views import Views


class RouteViews(Views):
    """
    Class for Route Views
    """
    def error_page(self):
        """
        Load the error page template
        """
        self.set_template('404.html')
        self.template_vars['pageName'] = 'Page Not Found'
        return self.template.render(self.template_vars)

    def access_denied(self):
        """
        Load the access denied page template
        """
        self.set_template('403.html')
        self.template_vars['pageName'] = 'Unauthorized Access'
        return self.template.render(self.template_vars)
