from usuarios.models import Profile  # Importa Profile desde donde lo tengas

def get_profile_username(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return {'profile_username': profile.user}
        except Profile.DoesNotExist:
            return {}
    return {}
