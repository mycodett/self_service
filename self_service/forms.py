from django import forms
from .models import Notification
from .models import Feedback

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()  # To upload the Excel file



class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['heading', 'content']

        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'feedback']

