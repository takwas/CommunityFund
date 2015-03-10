from communityfund.wsgi import CommunityFundApplication
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "communityfund.settings")

application = CommunityFundApplication

