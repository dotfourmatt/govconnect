from django.views.generic import TemplateView


class RegisterHelpView(TemplateView):
    template_name = "govconnect/register_help.html"
