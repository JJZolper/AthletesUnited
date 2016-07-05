import stream_django
from stream_django import feed_manager
from stream_django.enrich import Enrich

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views.generic.edit import CreateView

from athletesunited.athletes.models import Athlete
from athletesunited.main.models import TeamMember
from athletesunited.communities.models import CommunityPost, Hashtag

# AU Home
@login_required
def Home(request):
    enricher = Enrich()
    feeds = feed_manager.get_news_feeds(request.user.id)
    activities = feeds.get('flat').get()['results']
    activities = enricher.enrich_activities(activities)
    hashtags = Hashtag.objects.order_by('-occurrences')
    SelectedAthlete = get_object_or_404(Athlete, id=request.user.athlete.id)
    TotalAthletes = Athlete.objects.count()
    contextdata = {
        'activities': activities,
        'login_user': request.user,
        'hashtags': hashtags,
        'TotalAthletes': TotalAthletes
    }
    return render(request, 'index.html', contextdata)

# AU About
def About(request):
    contextdata = {}
    teammembers = TeamMember.objects.all()
    contextdata = {
        'TeamMembers': teammembers
    }
    return render(request, 'about.html', contextdata)

# AU Contact Us
def ContactUs(request):
    return render(request, 'underconstruction.html')

# AU Design Testing
def Design(request):
    return render(request, 'design.html')

# AU Give Feedback
@login_required
def GiveFeedback(request):
    return render(request, 'underconstruction.html')

# AU Privacy And Terms
def PrivacyAndTerms(request):
    return render(request, 'underconstruction.html')

# AU Report Spam
@login_required
def ReportSpam(request):
    return render(request, 'underconstruction.html')

# AU Report Community Post Spam
@login_required
def ReportCommunityPostSpam(request, communitypostid):
    contextdata = {}
    SelectedCommunityPost = get_object_or_404(CommunityPost, id = communitypostid)
    # Increment Spam Counter
    SelectedCommunityPost.spam_count += 1
    SelectedCommunityPost.save()
    print("Spam count is: " + str(SelectedCommunityPost.spamcount))
    '''
    if SelectedCommunityPost.spamcount > 6:
        # Reached SPAM Max, freeze the user's account
        userToFreeze = get_object_or_404(User, id = SelectedCommunityPost.user.id)
        userToFreeze.is_active = False
        userToFreeze.save()
        # Remove the SPAM
        SelectedCommunityPost.delete()
    '''
    return HttpResponseRedirect('/')

# AU Store
def Store(request):
    return render(request, 'store.html')

# AU Team Member
def TeamMemberPage(request, teammemberreq):
    context_data = {}
    SelectedTeamMember = get_object_or_404(TeamMember, slug = teammemberreq)
    contextdata = {
        'TeamMember': SelectedTeamMember
    }
    return render(request, 'teammember.html', context_data)











