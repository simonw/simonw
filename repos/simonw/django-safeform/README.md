django_safeform
===============

CSRF protection for Django implemented at the form level - no middleware 
required.

There are two steps to protecting a django.forms form:

1. Wrap it with the SafeForm class decorator. This adds a hidden csrf_token 
   field to it along with validation logic for checking if that token has 
   the correct value. It also changes the signature of the form class 
   slightly, see example below.
2. Apply the @csrf_protect middleware to the view containing the form. This 
   ensures that a _csrf_cookie is correctly set.

Run "./manage.py runserver" in the examples folder to start a Django server 
demonstrating the functionality of the library. Use "./manage.py test" in the 
same directory to run the unit tests.

Example usage::

    from django import forms
    from django.http import HttpResponse
    from django.shortcuts import render_to_response
    from django_safeform import SafeForm, csrf_protect
    
    class ChangePasswordForm(forms.Form):
        password = forms.CharField(widget = forms.PasswordInput)
        password2 = forms.CharField(widget = forms.PasswordInput)
    ChangePasswordForm = SafeForm(ChangePasswordForm)
    
    @csrf_protect
    def change_password(request):
        form = ChangePasswordForm(request) # A
        if request.method == 'POST':
            form = ChangePasswordForm(request, request.POST)
            if form.is_valid():
                # ... change the user's password here
                return HttpResponse('Thank you')
        return render_to_response('change_password.html', {
            'form': form,
        })

Note that the form constructor signature has changed - we now pass the request
object as the first argument.

Status and discussion
---------------------

This code is still being actively developed (the version number should really 
be 0.2, not 2.0) and discussed on the django-developers mailing list:

 - Thread: http://groups.google.com/group/django-developers/browse_thread/thread/3d2dc750082103dc/
 - Detailed critique by Luke Plant: http://groups.google.com/group/django-developers/msg/502475adb9f138d5

Revision history
----------------

v2.0.0 - 18 September 2009

Breaks backward compatibility with previous release - no longer changes the 
form constructor signature to take just the request object and decide whether 
or not to bind the form based on the request method. You now need to make that 
decision yourself in your view code (just as you do with regular Django 
forms). All examples and tests have been updated.

Added CsrfTestCase to test_utils, to simplify testing of CSRF protected forms.

v1.0.1 - 17 September 2009

Documentation fixes.

v1.0.0 - 17 September 2009

Initial release.

Installation
------------

django-safeform is in PyPI: http://pypi.python.org/pypi/django-safeform ::

    pip install django-safeform
    - OR -
    easy_install django-safeform

Custom form templates
---------------------

If your template uses one of the form rendering helper methods such as 
{{ form.as_p }} the hidden csrf_token field will be output automatically. If 
you are rendering the form using a custom template you will need to remember 
to output that field in your template explicitly. Here's an example::

    <form action="/change-password/" method="post">
        {{ form.non_field_errors }}
        <div{% if form.password.errors %} class="errors"{% endif %}>
            <label for="id_password">New password</label>
            {{ form.password }}
        </div>
        <div{% if form.password2.errors %} class="errors"{% endif %}>
            <label for="id_password2">Confirm password</label>
            {{ form.password2 }}
        </div>
        <div>{{ form.csrf_token }}<input type="submit" value="Change"></div>
    </form>

Note the {{ form.csrf_token }} replacement variable just before the submit 
button - this will output a hidden form field containing the correct value.

You should also be sure to include {{ form.non_field_errors }} somewhere in 
your template - this is where the "Form session expired - please resubmit" 
message will be displayed should the CSRF check fail for some reason.

Protecting forms that do not use django.forms
---------------------------------------------

If you are not using the django.forms framework - for example you are writing 
forms with hand-written HTML and pulling submitted data directly from 
request.POST - you can still add CSRF protection to your forms using the 
@csrf_protect decorator in conjunction with the csrf_utils module::

    from django_safeform import csrf_protect, csrf_utils
    
    @csrf_protect
    def hand_rolled(request):
        if request.method == 'POST':
            csrf_token = request.POST.get('csrf_token', '')
            if not csrf_utils.validate_csrf_token(csrf_token, request):
                return HttpResponse('Invalid CSRF token')
            else:
                return HttpResponse('OK')
        else:
            return HttpResponse("""
            <form action="." method="post">
            <input type="text" name="name">
            <input type="hidden" name="csrf_token" value="%s">
            </form>
            """ % csrf_utils.new_csrf_token(request))

It is your responsibility to include a hidden form field with the value from 
csrf_utils.new_csrf_token(request) in your form, and to check that token when 
the form is submitted using csrf_utils.validate_csrf_token.

You could also use CsrfForm to protect hand-written forms, as explained in 
the next section.

Protecting formsets / multiple forms on the same page
-----------------------------------------------------

If you have multiple forms on the page and they are each contained in separate
<form> elements, you should ensure each one has a csrf_token field, most 
likely by configuring each one using the SafeForm class decorator.

If you have multiple django.forms forms within a single <form> element (for 
example, if you are using formsets) you still only need to include a single 
csrf_token field for the overall form. In this case, rather than applying the 
SafeForm decorator to each of the form classes, it makes more sense to have a 
single standalone SafeForm instance within the overall form. The CsrfForm 
class is designed to handle this exact use-case. Here's how to use it::
    
    from django import forms
    from django.forms.formsets import formset_factory
    from django_safeform import csrf_protect, CsrfForm
    from django.http import HttpResponse
    
    class PersonForm(forms.Form):
        name = forms.CharField(max_length = 100)
        email = forms.EmailField()
    
    PersonFormSet = formset_factory(PersonForm, extra=3)
    
    @csrf_protect
    def formset(request):
        csrf_form = CsrfForm(request)
        formset = PersonFormSet()
        if request.method == 'POST':
            csrf_form = CsrfForm(request, request.POST)
            formset = PersonFormSet(request.POST)
            if csrf_form.is_valid() and formset.is_valid():
                return HttpResponse('Valid: %s' % ', '.join([
                    '%(name)s [%(email)s]' % form.cleaned_data 
                    for form in formset.forms
                    if form.cleaned_data
                ]))
        return render_to_response('formset.html', {
            'csrf_form': csrf_form,
            'formset': formset,
        })

The formset is used in the same way as usual. The CSRF protection is 
implemented entirely by the separate CsrfForm instance. In the template, the 
CsrfForm should be output using {{ csrf_form }} like this::

    <form action="." method="post">
        {{ csrf_form }}
        {% for form in formset.forms %}
            {{ form.as_p }}
        {% endfor %}
        <p>
            {{ formset.management_form }}
            <input type="submit">
        </p>
    </form>

The {{ csrf_form }} template tag specifies where the hidden input field 
containing the form token should be included. Should a CSRF failure occur, it 
also specifies where the <ul class="errorlist"> containing the CSRF failure 
message should be displayed.

If you want to include the hidden input field in a different location to the 
error message, you can use {{ csrf_form.csrf_token }} to output the hidden 
field and {{ csrf_form.non_field_errors }} to output the error message::

    <form action="." method="post">
        {{ csrf_form.non_field_errors }}
        {% for form in formset.forms %}
            {{ form.as_p }}
        {% endfor %}
        <p>
            {{ formset.management_form }}
            {{ csrf_form.csrf_token }}
            <input type="submit">
        </p>
    </form>


Changing the CSRF error message
-------------------------------

The default message shown to the user if the CSRF check fails is::

    Form session expired - please resubmit

The wording here is deliberately a bit vague - most users will have no idea 
what a "CSRF failure" is, but users have probably seen "session expired" 
messages before. A "form session" seems like a reasonable metaphor for what 
is going on under the hood.

If you dislike this message, you can over-ride it in your call to the 
SafeForm class decorator::

    ChangePasswordForm = SafeForm(ChangePasswordForm,
        invalid_message='CSRF check failed'
    )

Handling Ajax
-------------

By default, Ajax requests do NOT have CSRF protection applied to them - they 
will be ignored by the form validator, which looks out for any requests where 
request.is_ajax() returns True (i.e. requests which have a X-Requested_With
header set to XMLHttpRequest). This custom header is set by most common Ajax 
libraries. Protection is not needed here because it is not possible to forge 
HTTP headers when committing a CSRF attack using an HTML form.

If you are ultra-paranoid and want to apply CSRF protection even to requests 
with that header, you can disable the Ajax special case like this::

    ChangePasswordForm = SafeForm(ChangePasswordForm,
        ajax_skips_check=False
    )

If you do this, you will need to ensure the csrf_token is included in Ajax
POST requests yourself. One way to do this would be to read the token out of 
the first hidden input field with name="csrf_token" using the JavaScript DOM.

Enhancing security
------------------

By default, the form tokens served up in hidden fields are valid for POST 
submissions to any form on the site (for the user with that cookie) and never 
expire. You can limit the scope of the tokens in two ways - by tying them to 
a specific form, or by causing them to expire after a number of seconds.

To tie a token to one specific form, simply pass an identifier argument to 
the SafeForm decorator::

    ChangePasswordForm = SafeForm(ChangePasswordForm,
        identifier='change-password'
    )

Tokens generated for that form will now only allow submissions back to the 
same form. If you are using the csrf_utils module directly (in a hand-rolled 
form for example) you should pass identifier arguments to both the 
new_csrf_token and validate_csrf_token functions::

    token = csrf_utils.new_csrf_token(request, identifier='my-custom-form')
    # ... later ...
    token_ok = csrf_utils.validate_csrf_token(
        token, request, identifier='my-custom-form'
    )
    if not token_ok:
        return HttpResponse('Invalid CSRF token')

To cause your form tokens to expire, use the expire_after argument in your 
call to the SafeForm class decorator::

    ChangePasswordForm = SafeForm(ChangePasswordForm,
        identifier='change-password',
        expire_after=24 * 60 * 60 # Expire after 24 hours
    )

If using csrf_utils directly, pass that argument to the validate_csrf_token 
function::

    token_ok = csrf_utils.validate_csrf_token(
        token, request, identifier='my-custom-form', expire_after=24 * 60 * 60
    )

The default expire_after value is set by the CSRF_TOKENS_EXPIRE_AFTER setting,
which defaults to None. If you want all of your CSRF tokens to expire, add 
this to your settings.py file::

    CSRF_TOKENS_EXPIRE_AFTER = 24 * 60 * 60

When a token expires, the user will see the CSRF error message described above
but will not lose their form submission, so don't worry too much about the 
consequences of setting a strict timeout.

Protecting GET forms
--------------------

The examples so far have all been for forms submitted using the POST verb. It 
is also possible to protect GET forms against CSRF, but you should very rarely
need to do this. HTTP specifies that actions submitted via GET should be 
idempotent, which is generally interpreted as ruling that they should not 
cause state changes to your system. As such, an authenticated GET request 
should not be able to cause any damage.

Many GET forms are specifically designed to allow links from other sites to 
trigger an action - search forms for example. If your application has GET 
requests that require CSRF protection you should probably rethink the design 
of your application.

If you decide you do need to add CSRF protection to a GET form, you should be 
aware that it is much easier for csrf_tokens used in GET requests to "leak"
to an external attacker. URLs show up in Browser referral headers, so links 
to external sites from your CSRF protected GET page will inadvertently pass 
the token on to those sites. Your users may also accidentally share their 
CSRF tokens by pasting them in to e-mails or bookmarking them on link sharing 
sites.

Consequently, any CSRF tokens used in GET forms should take advantage of the 
extra security features documented above - they should use an identifier to 
lock the token down just to that form and should specify a strict expiry time 
to limit the damage that can be caused should the token accidentally leak.

Unit testing
------------

Properly unit testing CSRF protection is significantly more complicated than 
a regular unit test, as you need to first GET the initial form, then extract 
the csrf_token field from it, then submit that as part of the POST. The unit 
tests that ship with django_safeform show how to do this.

You can shortcut this process by using CsrfTestCase as the base class for your
unit tests. This swaps in an alternative Client implementation which causes 
POST requests using client.post() to automatically include a valid CSRF token.

Here's an example test using CsrfTestCase::

    from django_safeform import test_utils
    
    class SubmitTestCase(test_utils.CsrfTestCase):
        def test_submission_with_correct_csrf_token_works(self):
            response = self.client.post('/safe-basic-form/', {
                'name': 'Test',
            })
            self.assertEqual(response.content, 'Valid: Test')

If you are using the CsrfTestCase subclass but you do NOT wish to include the 
csrf_token automatically in one of your tests, pass a csrf=False argument to 
the client.post() method::

    def test_submission_without_csrf_token(self):
        response = self.client.post('/safe-basic-form/', {
            'name': 'Test',
        }, csrf=False)
        self.assert_(CSRF_INVALID_MESSAGE in response.content)

If you are protecting your forms with a custom form identifier, you should 
pass that identifier as the csrf argument::

    def test_change_password(self):
        response = self.client.post('/change-password/', {
            'password': 'new-password',
            'password2': 'new-password',
        }, csrf='change-password')
        # ...

If you are already using your own custom TestCase subclass and do not wish to 
use CsrfTestCase, you can instantiate the special client in your own setUp
method::
    
    from django_safeform import test_utils
    from django.test import TestCase
    
    class MyTestCaseSubclass(TestCase):
        def setUp(self):
            self.client = test_utils.CsrfClient()

Design notes
------------

Apps shipped with Django, in particular the admin, MUST be secure against CSRF 
no matter what the user's configuration is (so dependency on middleware alone 
is a problem).

Secure by default for user code would be nice, but in its absence explicitly 
raising developer awareness of CSRF is probably a good thing.

Should not be tied to sessions - some developers might not be using them.

Should not require the form framework - hand-rolled forms should be easy to 
protect too.

The original idea was to have an alternative Form base class called SafeForm - 
this was replaced with a class decorator when we realised that we would 
otherwise also need to provide SafeModelForm, SafeFormSet and so on.

Credits
-------

This library was developed from a discussion with Russell Keith-Magee, 
Andrew Godwin and Armin Ronacher at the DjangoCon 2009 sprints, and improved 
based on extensive feedback from Luke Plant on the django-developers mailing 
list.

TODO
----

 - Figure out what to do about protecting forms which already alter the 
   Form constructor signature themselves.
 - _csrf_token_from_request should throw error if cookie has not been set by 
   the csrf_protect decorator.
 - Improved support for unit testing CSRF protected forms.

Alternative approaches
----------------------

Pure middleware:
 - breaks with etags
 - rewrites HTML
 - doesn't work with streaming
 - you have to decorate things as exempt
 - potential leakage of external forms
 - XHTML v.s. HTML

Middleware and template tags and RequestContext:
 - uses a view middleware
 - applying by default is error prone
 - if user disables middleware, admin becomes insecure
 - requires RequestContext
 - form submissions are lost on CSRF failure
