import asyncio
import json

import websockets
from asgiref.sync import async_to_sync, sync_to_async
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string

from BackendCommunicationGateway.poll_api_gateway import PollApiGateway, Response
from Mappers.mappers import ArgumentMapperError
from Serializers.data_adapter import Adapter
from FrontendPollApi.__init__ import template_mapper, form_argument_mapper, chart_data_serializer, \
    form_model_serializer, SUPPORTED_METHODS, user


# Create your views here.
def home(request):
    return render(request, 'home.html', context={'operations': SUPPORTED_METHODS, 'server_user': user})


def vote(request):
    try:
        electable_id = request.GET.get('electableID')
    except KeyError:
        electable_id = 0

    try:
        poll_id = request.GET.get('pollID')
    except KeyError:
        poll_id = 0

    response = get_specific_response('vote', {'electableID': electable_id, 'pollID': poll_id})
    if response.status != 0:
        html_message = create_html_message(response.content, response.status)
    else:
        html_message = create_html_message(response.content, response.status)
    return HttpResponse(html_message, 200)


def poll_details(request):
    """
    Renders poll data into a detail page

    :return: JsonResponse with parameters **data** (for charts), **html_message** and
    **charts** html (initialization of chart html)
    """
    # Get the operation
    try:
        op = request.GET.get('op')
    except KeyError:
        op = ""

    if op == "getPoll" and "getPollWithImageSource" in SUPPORTED_METHODS:
        op = "getPollWithImageSource"

    # Get the required arguments for the given operation
    req_args = form_argument_mapper.get_form_attributes(op)

    # Get the arguments send by request
    sent_args = json.loads(request.GET.get('args'))

    # Initialize new dictionary containing all arguments
    args = {}
    for key in req_args.keys():
        try:
            # Fetch the given argument into new dict
            arg = sent_args[key]
            args[key] = arg
        except KeyError:
            # Set empty string if doesn't exist
            args[key] = ""

    # Get server response to operation with given args
    response = get_specific_response(op, args)

    # If error render message
    if response.status != 0:
        html_message = create_html_message(response.content, response.status)
        return JsonResponse({'data': None, 'html_message': html_message}, status=200)

    # If there was no data
    if response.content is None or response.content == "" or response.content == {}:
        html_message = render_to_string('poll_details.html', context={'model': None,
                                                                      'message': "The server returned no data"})
        return JsonResponse({'data': None, 'html_message': html_message}, status=200)

    # Get poll model from response dicts
    poll_model = Adapter.adaptContent(response)
    if type(poll_model) == list:
        poll_model = poll_model[0]

    # Get chart data with poll model
    chart_data = chart_data_serializer.poll_pie_chart(poll_model)

    # If there is no chart data then there are no votes, hence we set the appropriate message
    if chart_data is None or chart_data == {}:
        html_message = render_to_string('poll_details.html', context={'model': poll_model,
                                                                      'message': "There are no votes on this poll yet"})
        # Return the json response with empty chart data
        return JsonResponse({'data': chart_data, 'charts': None, 'html_message': html_message}, status=200)

    # Return the response with the correct data
    html_message = render_to_string('poll_details.html', context={'model': poll_model})  # The default html
    charts = render_to_string('pie_chart_renderer.html', context={'charts': poll_model.election.regions})  # The charts
    return JsonResponse({'data': chart_data, 'charts': charts, 'html_message': html_message}, status=200)


def get_arg_form(request):
    """
    Retrieves the operation from the request body and creates a html Form with the arguments required.

    :return: HttpResponse with Form
    """
    try:
        operation = request.GET.get("op")
        arguments = form_argument_mapper.get_form_attributes(operation)
    except (KeyError, ArgumentMapperError):
        err_msg = create_html_message("The operation requested couldn't be found", 400)
        return HttpResponse(err_msg, 200)

    html_response = render_to_string('form_creator.html', context={'argument_dict': arguments})
    return HttpResponse(html_response, 200)


def receive_data(request):
    """
    This is the default fetch method which is used to fetch any data using the 'available operations' tab.

    :param request: The default request containing an operation and form arguments in it's body
    :return: HTML object rendered with mapped html or an error message.
    """
    # Get the response from server
    response = get_response(request)
    # If the operation was logout or login we must set the user logged in status
    if response.operation == "logout" and response.status == 0:
        user.is_authenticated = False

    if response.operation == "login" and response.status == 0:
        user.is_authenticated = True

    # If the response returned an error
    if response.status != 0:
        # Render error message
        html_error_message = create_html_message(response.content, response.status)
        return HttpResponse(html_error_message, status=200)

    # If there is no content
    if response.content is None or response.content == "" or response.content == {}:
        # Render no data found error message
        html_error_message = create_html_message("No data found.", 400)
        return HttpResponse(html_error_message, status=200)

    # If there was data create models from the data
    models = Adapter.adaptContent(response)

    # If the template used for the operation is message.html we send 'message' attribute to the template
    if template_mapper.get_template(response.operation) == 'message.html':
        html_response = render_to_string(template_mapper.get_template(response.operation), context={'message': models})
    else:
        # other wise we make sure our models are in a list and render them with 'models' attribute to template
        if not type(models) is list:
            models = [models]

        html_response = render_to_string(template_mapper.get_template(response.operation), context={'models': models})

    return HttpResponse(html_response, status=200)


def get_response(request) -> Response:
    """
    This method fetches the operation and arguments to send to PollAPI from the request
    and sends back the response object containing status, content and operation

    :returns Response:
    """

    op = None
    args = None
    # Getting arguments
    if request.method == "GET":
        op, args = get_op_args(request)

    elif request.method == "POST":
        op, args = post_op_args(request)

    # Creating a new event loop
    loop = asyncio.new_event_loop()

    # Passing the event loop to the gateway api for execution (gets completed internally)
    gateway = PollApiGateway(loop)
    if op == 'login':
        response = gateway.log_in(args)
    else:
        response = gateway.get_request(op, args)

    return response


def get_specific_response(operation: str, arguments: dict) -> Response:
    """
    This method sends back the response object containing status, content and operation from the poll api server.

    :returns Response:
    """
    # Creating a new event loop
    loop = asyncio.new_event_loop()

    # Passing the event loop to the gateway api for execution (gets completed internally)
    gateway = PollApiGateway(loop)
    if operation == 'login':
        response = gateway.log_in(arguments)
    else:
        response = gateway.get_request(operation, arguments)

    return response


def logout(request):
    """
    Logs out user if logged in and redirects to home page.

    :param request: WSGIRequest
    :return: redirect to home
    """
    # Get logout response from server
    response = get_specific_response('logout', {})
    # If error
    if response.status != 0:
        # Set django error message
        messages.add_message(request, messages.WARNING, response.content)
        return redirect('home')
    else:
        # If not error and there is content
        if response.content:
            messages.add_message(request, messages.SUCCESS, response.content)
        else:
            # if no error but there is no content
            messages.add_message(request, messages.SUCCESS, "Logout successful")

    # Set the use to logged out
    user.is_authenticated = False
    return redirect('home')


def login(request):
    """
    **POST** to view: Request a login to server. \n
    **GET** to view: Request login page. \n

    Post retrieves auth arguments from **post request** body and then sends a login request to server.

    :returns: redirect to homepage or render login page
    """
    # The arguments required in the form
    args = form_argument_mapper.get_form_attributes('login')
    if request.method == "GET":
        # fetch models from form serializer
        form_models = form_model_serializer.model_form(args)

        # render login page
        return render(request, 'login.html', context={'form_models': form_models, 'server_user': user})

    if request.method == "POST":
        # Try a login
        sent_args = {}  # Input arguments received from the form
        for arg in args.keys():
            try:
                # get the argument
                sent_args[arg] = request.POST.get(arg)
            except KeyError:
                # Happens only if the form is on incorrect format
                err = "Missing value of attribute %s" % arg
                print(err)
                messages.add_message(request, messages.WARNING, err)

        # Creating a new event loop
        loop = asyncio.new_event_loop()
        # Injecting the loop
        gateway = PollApiGateway(loop)
        # Sending login request to server
        response = gateway.log_in(sent_args)

        if response.status != 0:
            # Get form models with the values the user has sent in inputs
            form_models = form_model_serializer.model_form(args, sent_args)
            # Add an error message
            messages.add_message(request, messages.WARNING, response.content)
            # Render login page again
            return render(request, 'login.html', context={'form_models': form_models, 'server_user': user})

        # If the operation was successful set success message and redirect to home page
        messages.add_message(request, messages.SUCCESS, response.content)
        user.is_authenticated = True
        return redirect('home')


def register(request):
    """
        **POST** to view: Request registration with form args to server. \n
        **GET** to view: Request registration page. \n

        Post retrieves form arguments from **post request** body and then sends a registration request to server.

        :returns: redirect to login if successful or renders registration page with error message
        """
    # Arguments required for the registration form
    args = form_argument_mapper.get_form_attributes('createUser')
    if request.method == "GET":
        # Get the form models to render in the template using the arguments required
        form_models = form_model_serializer.model_form(args)
        # render the registration page with empty values
        return render(request, 'register.html', context={'form_models': form_models, 'server_user': user})

    if request.method == "POST":
        # Attempt a registration with the given form inputs
        sent_args = {}  # Retrieves the argument inputs in form
        for arg in args.keys():
            try:
                # set attribute value in the sent args dictionary
                sent_args[arg] = request.POST.get(arg)
            except KeyError:
                # This should only happen if the form is in incorrect format (missing form input in the actual form)
                err = "Missing value of attribute %s" % arg
                # add a message (django messages) that gets rendered in the template
                messages.add_message(request, messages.WARNING, err)  # add error message, this is a django module
                # redirect to registration page again
                return redirect('register')

        # The operation name of registering
        operation = "createUser"

        # Get a response from server
        response = get_specific_response(operation, sent_args)

        # If the response is an error
        if response.status != 0:
            # Get the form models with the user input values
            form_models = form_model_serializer.model_form(args, sent_args)
            # Add a message to the django messages to render in template
            messages.add_message(request, messages.WARNING, response.content)
            # render the registration page again
            return render(request, 'register.html', context={'form_models': form_models, 'server_user': user})

        # Registration was successful redirect to login
        else:
            messages.add_message(request, messages.SUCCESS, response.content)
            return redirect('login')


def create_html_message(message: str, response_status) -> str:
    """
    Creates a html string from a message. Takes response status as argument to assert which template to use.

    :param message: Takes the message as string
    :param response_status: The status of the received response
    :return: returns a string of html
    """
    # if error message render error html
    if response_status != 0:
        return render_to_string('error_message.html', context={'message': message})
    else:
        # Render success html
        return render_to_string('message.html', context={'message': message})


def get_op(request) -> str:
    try:
        op = request.GET.get("op")
    except KeyError:
        raise KeyError("op not found.")
    return op


def get_op_args(request) -> tuple:
    """
    Retrieves operation and arguments from **get request** body

    :returns: tuple (op: str, args: dict)
    """
    try:
        op = request.GET.get("op")
    except KeyError:
        raise KeyError("op not found.")
    try:
        args = request.GET.get("args")
        args = json.loads(args)
    except KeyError:
        raise KeyError("args not found.")
    except ValueError:
        return op, {}

    return op, args


def post_op_args(request):
    """
    Retrieves operation and arguments from **post request** body

    :returns: tuple (op: str, args: dict)
    """
    try:
        op = request.POST.get("op")
    except KeyError:
        raise KeyError("op not found.")
    try:
        args = request.POST.get("args")
        args = json.loads(args)
    except KeyError:
        raise KeyError("args not found.")
    except ValueError:
        return op, {}

    return op, args


# TODO: Add views for all methods
# TODO: Figure out a smart solution for ajax call url mapping
