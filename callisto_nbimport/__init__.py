import os
import arrow
import logging
from tornado import escape
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler

logger = logging.getLogger(__name__)


def _jupyter_server_extension_paths():
    return [{
        "module": "callisto_nbimport"
    }]


class NotebookImportHandler(IPythonHandler):

    def check_xsrf_cookie(self):
        # Uses token authentication
        pass

    def post(self):
        # TODO Add token validation
        # access_token = self.request.headers.get('Authorization')
        try:
            data = escape.json_decode(self.request.body)
            notebook_name = data['notebook_name']
            notebook_contents = data['notebook_contents']

            if os.path.isfile(notebook_name):
                notebook_name = notebook_name.replace('.ipynb',
                                                      '-{}.ipynb'.format(arrow.now().format('YYYY-MM-DD-HH:mm:ss')))
            with open(notebook_name, 'w') as f:
                f.write(notebook_contents)
            self.write({'notebook_name': notebook_name})
        except Exception as e:
            logger.info(repr(e))
            self.set_status(500, 'JupyterHub failed to import notebook. Exception: {0}'.format(repr(e)))


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
    web_app.add_handlers(host_pattern, [(route_pattern, NotebookImportHandler)])
