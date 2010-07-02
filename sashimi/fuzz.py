from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest
import transaction

from sashimi.contenttypes import ContentTypeVisitor
from sashimi.content import ContentMapVisitor

def login(app, manager_user):
    user = app.acl_users.getUserById(manager_user).__of__(app.acl_users)
    newSecurityManager(None, user)
    return makerequest(app)

app = login(app, "zopeadmin")

a = ContentTypeVisitor(app.portal)
map = a.visit_types()

b = ContentMapVisitor(map)
b.fuzz()

