from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
import logging

# Configure logger
logger = logging.getLogger(__name__)

def index(request):
    """
    View function to render the index page.

    Args:
        request (Request): the Django request object

    Returns:
        HttpResponse: the rendered index page
    """
    logger.info("Rendering the index page")
    return render(request, 'home/index.html')

def privacy(request):
    """
    View function to render the privacy page.

    Args:
        request (Request): the Django request object

    Returns:
        HttpResponse: the rendered privacy page
    """
    logger.info("Rendering the privacy page")
    return render(request, 'home/privacy.html')

def error(request):
    """
    View function to render the error page.

    Args:
        request (Request): the Django request object

    Returns:
        HttpResponse: the rendered error page with the request ID in the context
    """
    request_id = request.META.get('HTTP_X_REQUEST_ID', '')
    context = {'request_id': request_id}
    logger.error(f"Error page rendered with Request ID: {request_id}")
    return render(request, 'shared/error.html', context)

# Dynamic dispatch function for controller and action routing
def dispatch(request, controller, action, id=None):
    """
    Dynamic dispatch function for controller and action routing.

    Args:
        request (Request): the Django request object
        controller (str): the controller name
        action (str): the action name
        id (str): the optional ID parameter

    Returns:
        HttpResponse: the rendered page based on the controller and action

    Raises:
        Http404: when the route is not found
    """
    
    try:
        # Map controller and action to view functions
        if controller.lower() == "home" and action.lower() == "index":
            return index(request)
        elif controller.lower() == "home" and action.lower() == "privacy":
            return privacy(request)
        elif controller.lower() == "home" and action.lower() == "error":
            return error(request)
        else:
            return HttpResponse(f"Controller: {controller}, Action: {action}, ID: {id}")
    except Exception as e:
        logger.exception("An error occurred while dispatching")
        raise Http404("Route not found")

def send_contact_email(request):
    """
    View function to send contact email.

    Args:
        request (Request): the Django request object

    Returns:
        HttpResponse: the response to the request, either a success message or an error message

    Notes:
        This function expects a POST request and extracts the following parameters from the request:
            - name
            - email
            - message
        It then sends an email using the send_mail function and returns a success response.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send the email
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'sean.morgan0323@gmail.com',  # Replace with your email address
            ['sean.morgan0323@gmail.com'],  # Replace with the recipient's email address
            fail_silently=False,
        )

        # Return a success response
        return HttpResponse('Email sent successfully!')
    else:
        return HttpResponse('Invalid request method.')

