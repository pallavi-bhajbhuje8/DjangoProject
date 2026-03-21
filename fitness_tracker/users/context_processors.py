def user_profile_context(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Exception:
            profile = None
        return {'user_profile': profile}
    return {'user_profile': None}