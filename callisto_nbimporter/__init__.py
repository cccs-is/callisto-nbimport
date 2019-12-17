from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
#from tornado import web
from .helper import import_notebook
import logging

logger = logging.getLogger(__name__)

def _jupyter_server_extension_paths():
    return [{
        "module": "callisto_nbimporter"
    }]


class HelloWorldHandler(IPythonHandler):
    def get(self):
        notebook_location = self.get_argument('notebook_location')
        notebook_name = self.get_argument('notebook_name')
        access_token = self.get_argument('access_token')
        target = self.get_argument('target', default=None)
        #logger.info('>>> calling import_notebook() @web.authenticated removed (replace http with https)')
        oauth2_proxy_cookie = self.get_cookie('_oauth2_proxy')
        cookies = None
        if oauth2_proxy_cookie is not None :
            cookies = {'_oauth2_proxy': oauth2_proxy_cookie} 
        # logger.info('cookies we well use:')
        # logger.info(cookies)
        notebook_name = import_notebook(notebook_location, notebook_name, access_token, cookies)
        # self.finish('Imported notebook {}'.format(
        #    notebook_name))
        if target == 'voila':
            url = "{base}voila/voila/render/{nbname}".format(
                base=self.base_url,
                nbname=notebook_name
            )
        else:
            url = "{base}notebooks/{nbname}".format(
                        base=self.base_url,
                        nbname=notebook_name
            )
        # logger.info('HelloWorldHandler() -> url:' +  url)
        self.redirect(url)
        # self.redirect(self.base_url)


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication):
            handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'],
                                  '/notebook-import')
    web_app.add_handlers(host_pattern, [(route_pattern, HelloWorldHandler)])
