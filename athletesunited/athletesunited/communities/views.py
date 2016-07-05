import stream_django
from stream_django import feed_manager
from stream_django.enrich import Enrich

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import translation

from athletesunited.athletes.models import Athlete, AthleteEmail
from athletesunited.ads.models import Ad
from athletesunited.comments.models import Comment
from athletesunited.comments.views.moderation import perform_delete
from athletesunited.communities.forms import CommunityPostForm
from athletesunited.communities.models import Community, Country, City, CommunityPost

# AU Communities
def Communities(request):
    contextdata = {}
    Communities = Community.objects.all()
    SelectedAthlete = get_object_or_404(Athlete, id=request.user.athlete.id)
    if Communities.exists():
        contextdata = {
            'Communities': Communities,
            'SelectedAthlete': SelectedAthlete
        }
        return render(request, 'communities.html', contextdata)
    else:
        contextdata = {
            'CommunitiesError': 'There aren\'t any Communities'
        }
        return render(request, 'communities.html', contextdata)

# AU Community My Conversations
@login_required
def CommunityMyConversations(request):
    contextdata = {}
    SelectedAthlete = get_object_or_404(Athlete, id=request.user.athlete.id)
    athlete_conversations = SelectedAthlete.my_conversations.all().order_by('-created_at')[:3600]
    contextdata = {
        'CommunityPosts': athlete_conversations
    }
    return render(request, 'communitymyconversations.html', contextdata)

# AU Communities Search
@login_required
def Search_Communities_AJAX(request):
    contextdata = {}
    if request.method == 'POST' and request.is_ajax():
        searchquery = request.POST['searchquery']
    else:
        searchquery = ''
    if searchquery == '':
        selectedCommunities = ''
    else:
        selectedCommunities = Community.objects.filter(name__icontains = searchquery)
    contextdata = {
        'Communities': selectedCommunities
    }
    return render(request, 'search_community_results_ajax.html')

# AU Communities Search Results
@login_required
def Search_Community_Results(request):
    contextdata = {}
    if request.method == 'POST':
        searchquery = request.POST['searchquery']
    else:
        searchquery = ''
    if searchquery == '':
        selectedCommunities = ''
    else:
        selectedCommunities = Community.objects.filter(name__icontains = searchquery)
    contextdata = {
        'Communities': selectedCommunities,
        'searchquery': searchquery
    }
    return render(request, 'search_community_results.html', contextdata)

# AU Community City Post
@login_required
def CommunityCityPostPage(request, communityslug, cityslug):
    contextdata = {}
    SelectedCommunity = get_object_or_404(Community, slug = communityslug)
    SelectedAthlete = get_object_or_404(Athlete, id=request.user.athlete.id)
    if request.method == 'POST' and request.is_ajax():
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            user = request.user
            body = form.cleaned_data['body']
            SelectedCity = get_object_or_404(City, slug = cityslug)
            communitypost = CommunityPost(user=user, body=body, community=SelectedCommunity, city=SelectedCity)
            communitypost.save()
            SelectedAthlete.my_conversations.add(communitypost)
            contextdata = {
                'CommunityPost': communitypost
            }
            html = render_to_string('communitypost.html', contextdata, context_instance = RequestContext(request))
            return JsonResponse({'html': html})
        else:
            contextdata = {'form': form}
            return render(request, 'communitytopic/communitypostpage.html', contextdata)
    if request.method == 'GET' and request.is_ajax():
        if request.GET.get('postid'):
            if request.GET.get('verifiedathleteslug'):
                postid = request.GET['postid']
                verifiedathleteslug = request.GET['verifiedathleteslug']
                SelectedAthlete = get_object_or_404(Athlete, slug=verifiedathleteslug)
                Comments = Comment.objects.filter(user__username = SelectedAthlete.user.username).filter(object_pk = postid).order_by('submit_date')
                contextdata = {'comment_list': Comments, 'postid': postid}
                commentshtml = render_to_string("comments/list.html", contextdata, context_instance = RequestContext(request))
                return JsonResponse({'commentshtml': commentshtml})
            else:
                postid = request.GET['postid']
                Comments = Comment.objects.filter(object_pk = postid).order_by('submit_date')
                contextdata = {
                    'comment_list': Comments,
                    'postid': postid
                }
                commentshtml = render_to_string("comments/list.html", contextdata, context_instance = RequestContext(request))
                return JsonResponse({'commentshtml': commentshtml})
        if request.GET.get('postidreq'):
            postidreq = request.GET['postidreq']
            SelectedPost = CommunityPost.objects.get(id = postidreq)
            SelectedPost.delete()
            return JsonResponse({'postID': postidreq})
        if request.GET.get('commentidreq'):
            commentidreq = request.GET['commentidreq']
            comment = get_object_or_404(comments.get_model(), pk=commentidreq, site__pk=settings.SITE_ID)
            perform_delete(request, comment)
            return JsonResponse({'commentID': commentidreq})
    else:
        ''' user is not submitting the form, show the blank community post form '''
        form = CommunityPostForm()
        total_athlete_in_community = SelectedCommunity.athlete_set.all().count()
        SelectedCity = get_object_or_404(City, slug = cityslug)
        if SelectedCity == SelectedAthlete.current_city:
            MakePost = True
        else:
            MakePost = False
        CommunityPostsQuerySet = CommunityPost.objects.filter(community__slug = communityslug).filter(city__slug = cityslug).order_by('-created_at')[:3600]
        Ads = Ad.objects.filter(community__slug = communityslug).filter(city__slug = cityslug).order_by('?')[:2]
        paginator = Paginator(CommunityPostsQuerySet, 10)
        page = request.GET.get('page')
        try:
            CommunityPosts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            CommunityPosts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            CommunityPosts = paginator.page(paginator.num_pages)
        tags = SelectedCommunity.name + ", " + SelectedCity.name
        contextdata = {
            'Community': SelectedCommunity,
            'SelectedAthlete': SelectedAthlete,
            'TotalAthletesInCommunity': total_athlete_in_community,
            'MakePost': MakePost,
            'tags': tags,
            'form': form,
            'CommunityPosts': CommunityPosts,
            'Ads': Ads
        }
        return render(request, 'communitytopic/communitypostpage.html', contextdata)

# AU City Communities
def CityCommunities(request):
    contextdata = {}
    Cities = City.objects.all()
    if Cities.exists():
        contextdata = {
            'Cities': Cities
        }
        return render(request, 'communitylocation/cities.html', contextdata)
    else:
        contextdata = {
            'CitiesError': 'There aren\'t any Cities'
        }
        return render(request, 'communitylocation/cities.html', contextdata)

# AU City Community Post
@login_required
def CityCommunityPostPage(request, cityslug):
    contextdata = {}
    SelectedCity = get_object_or_404(City, slug = cityslug)
    SelectedAthlete = get_object_or_404(Athlete, id=request.user.athlete.id)
    if request.method == 'POST' and request.is_ajax():
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            user = request.user
            body = form.cleaned_data['body']
            communitypost = CommunityPost(user=user, body=body, city=SelectedCity)
            communitypost.save()
            contextdata = {
                'CommunityPost': communitypost
            }
            html = render_to_string('communitypost.html', contextdata, context_instance = RequestContext(request))
            return JsonResponse({'html': html})
        else:
            msg="AJAX post invalid"
            contextdata = {'form': form}
            return render(request, 'communitylocation/citypostpage.html', contextdata)
    if request.method == 'GET' and request.is_ajax():
        if request.GET.get('postid'):
            if request.GET.get('verifiedathleteslug'):
                postid = request.GET['postid']
                verifiedathleteslug = request.GET['verifiedathleteslug']
                SelectedAthlete = get_object_or_404(Athlete, slug=verifiedathleteslug)
                Comments = Comment.objects.filter(user__username = SelectedAthlete.user.username).filter(object_pk = postid).order_by('submit_date')
                contextdata = {
                    'comment_list': Comments,
                    'postid': postid
                }
                commentshtml = render_to_string("comments/list.html", contextdata, context_instance = RequestContext(request))
                return JsonResponse({'commentshtml': commentshtml})
            else:
                postid = request.GET['postid']
                Comments = Comment.objects.filter(object_pk = postid).order_by('submit_date')
                contextdata = {
                    'comment_list': Comments,
                    'postid': postid
                }
                commentshtml = render_to_string("comments/list.html", contextdata, context_instance = RequestContext(request))
                return JsonResponse({'commentshtml': commentshtml})
        if request.GET.get('postidreq'):
            postidreq = request.GET['postidreq']
            SelectedPost = CommunityPost.objects.get(id = postidreq)
            SelectedPost.delete()
            return JsonResponse({'postID': postidreq})
        if request.GET.get('commentidreq'):
            commentidreq = request.GET['commentidreq']
            comment = get_object_or_404(comments.get_model(), pk=commentidreq, site__pk=settings.SITE_ID)
            perform_delete(request, comment)
            return JsonResponse({'commentID': commentidreq})
    else:
        form = CommunityPostForm()
        enricher = Enrich()
        feed = feed_manager.get_feed('citypost', SelectedCity.name.replace(" ", "_"))
        activities = feed.get(limit=25)['results']
        enricher.enrich_activities(activities)
        contextdata = {
            'City': SelectedCity,
            'form': form,
            'activities': activities
        }
        return render(request, 'communitylocation/citypostpage.html', contextdata)






