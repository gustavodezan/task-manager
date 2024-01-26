from . import schemas, auth

# Workspace
def check_if_user_can_change_workspace(user, workspace):
    if user.id in [member.id for member in workspace.members] and user.access_level >= 1:
        return True
    return False