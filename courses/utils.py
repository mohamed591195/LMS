

def belong_to_group(user, name):
    return user.groups.filter(name=name).exists()

