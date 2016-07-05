from django.shortcuts import get_object_or_404

from athletesunited.athletes.models import Athlete

def RenderAthleteAvatar(request):
    if request.user.is_authenticated() and "admin" not in request.path:
        athlete = get_object_or_404(Athlete, pk=request.user.athlete.id)
        return {'Uathlete': athlete}
    else:
        return {}



