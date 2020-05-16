class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One time configuration and initialization
    
    def __call__(self, request):
        """
        Code to be executed for each request
        before the view are called
        """

        response = self.get_response(request)

        """
        Code to be executed for each request
        before the view are called
        """
        return response
    def process_view(self, request, view_func, *view_args, **view_kargs):
        """
        called just before Django calls the view.
        Return either none or HttpResponse
        """
        if request.user.is_authenticated:
            request.role = None
            groups = request.user.groups.all()
            if groups:
                request.role = groups[0].name
    # def process_exception(self, request, exception):
    #     """
    #     called for the response if exception
    #     is raised by view.
    #     return either none or HttpRsponse
    #     """
    #     pass
    # def process_template_response(self, request, response):
    #     """
    #     request - HttpRequest object
    #     response - TemplateResponse object
    #     return template response
    #     use this for changing template or context 
    #     it it is needed
    #     """
    #     pass