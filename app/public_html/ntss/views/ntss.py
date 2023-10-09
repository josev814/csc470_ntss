from jinja2 import Environment, FileSystemLoader, select_autoescape

class ntss_views():

    def login_view():
        """
        Load the login template
        """
        env = Environment(
            loader=FileSystemLoader('ntss/templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('login.html')

        print(
            template.render(
            )
        )
