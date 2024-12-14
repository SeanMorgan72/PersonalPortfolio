from django.db import models

class ErrorViewModel(models.Model):
    request_id = models.CharField(max_length=255)

    @property
    def show_request_id(self):
        """
        Whether the request ID should be shown in the error page.

        :return: True if the request ID should be shown, False otherwise
        :rtype: bool
        """
        return bool(self.request_id)

