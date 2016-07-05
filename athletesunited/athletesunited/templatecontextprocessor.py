from django.conf import settings

def AUPhaseManagement(request):
    AU_Phase_Mgmt = {
        'DEBUG': settings.DEBUG,
    }
    return AU_Phase_Mgmt



