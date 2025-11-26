
def total_data(request):
    if request.user.is_authenticated:
        branch = request.user.branch
    else:
        branch = None
    context={
        'branch': branch,
        'user': request.user,
    }
    return context