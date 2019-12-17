import requests
import os
import arrow
import logging

logger = logging.getLogger(__name__)

def import_notebook(notebook_url, notebook_name, access_token, cookies = None):
    notebook_url = notebook_url.replace('http:', 'https:')

    # logger.info('import_notebook extension() --> notebook_url:' + notebook_url)
    # logger.info('import_notebook extension() --> access_token:' + access_token)
    headers = {'Authorization': 'Bearer {}'.format(access_token),
               'X-Access-Token': access_token}
    try:
        response = requests.get(notebook_url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            notebook_content = response.content
            if os.path.isfile(notebook_name):
                notebook_name = notebook_name.replace('.ipynb',
                                                      '-{}.ipynb'.format(
                                                      arrow.now().format(
                                                      'YYYY-MM-DD-HH:mm:ss'
                                                      )))
            with open(notebook_name,'wb') as f:
                f.write(notebook_content)
            return notebook_name
    
    except Exception as e:
        logger.info('Exception while importing notebook:{} - {}'.format(notebook_name, repr(e)))
        notebook_name = '' 
   
    return notebook_name
