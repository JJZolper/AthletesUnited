import json
from django import http
from django.apps import apps
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from athletesunited import comments
import athletesunited.comments
from athletesunited.comments.forms import FluentCommentForm
from athletesunited.comments import signals
from athletesunited.comments.views.utils import next_redirect, confirmation_view

class CommentPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """
    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("comments/400-debug.html", {"why": why})

@csrf_protect
@require_POST
def post_comment_ajax(request, using=None):
    """
    Post a comment, via an Ajax call.
    """
    if not request.is_ajax():
        return HttpResponseBadRequest("Expecting Ajax call")
    
    # This is copied from django.contrib.comments.
    # Basically that view does too much, and doesn't offer a hook to change the rendering.
    # The request object is not passed to next_redirect for example.
    #
    # This is a separate view to integrate both features. Previously this used django-ajaxcomments
    # which is unfortunately not thread-safe (it it changes the comment view per request).
    
    
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.athlete.get_full_name()
    
    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = apps.get_model(ctype)
        # model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
        # Hold on to the community post this new comment is being made to for the purpose of checking if the user is verified.
        targetPost = target
    except TypeError:
        return CommentPostBadRequest(
             "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
             "The given content-type %r does not resolve to a valid model." % \
                 escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
             "No object matching content-type %r and object PK %r exists." % \
                 (escape(ctype), escape(object_pk)))
    except (ValueError, ValidationError) as e:
        return CommentPostBadRequest(
             "Attempting go get content-type %r and object PK %r exists raised %s" % \
                 (escape(ctype), escape(object_pk), e.__class__.__name__))

    # Do we want to preview the comment?
    # preview = "preview" in data
    
    # Construct the comment form
    form = FluentCommentForm(target, data=data)
    
    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
             "The comment form failed security verification: %s" % \
                 escape(str(form.security_errors())))

    # If there are errors or if we requested a preview show the comment
    # if preview:
        # comment = form.get_comment_object() if not form.errors else None
        # return _ajax_result(request, form, "preview", comment, object_id=object_pk)
    if form.errors:
        return _ajax_result(request, form, "post", object_id=object_pk)

    # Otherwise create the comment
    comment = form.get_comment_object()
    comment.ip_address = request.META.get("REMOTE_ADDR", None)
    if request.user.is_authenticated():
        comment.user = request.user
        comment.user_name = request.user.athlete.get_full_name()
        comment.user_url = request.user.athlete.get_url()
        # Check whether or not the user making the comment is verified, if so add them to the list of verified individuals having commented on the post object.
        if request.user.athlete.isVerified == True:
            targetPost.verifiedUsers.add(request.user)
        # A similar concept to the above for verified could be used to push out to a feed when a user makes a comment and we want to show wich posts they've interacted with.
        request.user.athlete.myconversations.add(targetPost)

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(
        sender  = comment.__class__,
        comment = comment,
        request = request
    )
    
    for (receiver, response) in responses:
        if response is False:
            return CommentPostBadRequest(
                 "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_posted.send(
        sender  = comment.__class__,
        comment = comment,
        request = request
    )

    return _ajax_result(request, form, "post", comment, object_id=object_pk)


def _ajax_result(request, form, action, comment=None, object_id=None):
    # Based on django-ajaxcomments, BSD licensed.
    # Copyright (c) 2009 Brandon Konkle and individual contributors.
    #
    # This code was extracted out of django-ajaxcomments because
    # django-ajaxcomments is not threadsafe, and it was refactored afterwards.
    
    success = True
    json_errors = {}
    
    if form.errors:
        for field_name in form.errors:
            field = form[field_name]
            #json_errors[field_name] = _render_errors(field)
        success = False
    
    json_return = {
        'success': success,
        'action': action,
        'errors': json_errors,
        'object_id': object_id,
    }
    
    if comment is not None:
        context = {
            'comment': comment,
            'action': action,
            'preview': (action == 'preview'),
        }
        comment_html = render_to_string('comments/comment.html', context, context_instance=RequestContext(request))
        
        json_return.update({
           'html': comment_html,
           'comment_id': comment.id,
           'parent_id': None,
           'is_moderated': not comment.is_public,   # is_public flags changes in comment_will_be_posted
        })

    json_response = json.dumps(json_return)
    return HttpResponse(json_response, content_type="application/json")

'''
def _render_errors(field):
    """
    Render form errors in crispy-forms style.
    """
    template = '{0}/layout/field_errors.html'.format(appsettings.CRISPY_TEMPLATE_PACK)
    return render_to_string(template, {
                            'field': field,
                            'form_show_errors': True,
                            })
'''


