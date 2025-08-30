def user_groups(request):
    user = request.user
    return {
        'is_client': user.groups.filter(name='Clients').exists(),
        'is_admin': user.groups.filter(name='Administrators').exists(),
        'is_agent': user.groups.filter(name='Agents').exists(),
    }