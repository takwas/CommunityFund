from dj_static import Cling
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "communityfund.settings")

application = Cling(get_wsgi_application())

