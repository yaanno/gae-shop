from apps.files.models import File
from tipfy.ext.i18n import gettext as _


def get_files():
    files = File.get_latest_files(None, 100)
    '''
    [{ 'id': 1, 'title': 'title' }]
    '''
    
    
    default_list = {'id': '', 'title': unicode(_('Please choose an image'))}
    if files:
        file_list = [( { 'id': f.key().id(), 'title': unicode(f.title) }) for f in files]
        file_list.insert(0, default_list)
    else:
        file_list = default_list
    return file_list