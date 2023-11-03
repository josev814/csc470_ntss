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
        self.templateVars['pageName'] = 'Page Not Found'
        return self.template.render(self.templateVars)
