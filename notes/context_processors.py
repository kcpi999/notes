def current_user(request):
    user = request.user
    if user.is_authenticated():
        return {'current_user': user}
    else:
        return {}

def current_user_fio(request):
    user = request.user    
    fio = ''
    if user.is_authenticated():
        fio += user.first_name
        if user.last_name != '':
            fio += ' ' + user.last_name
        if len(fio) < 1:
            fio = user.username
        
    return {'current_user_fio': fio}
