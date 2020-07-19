from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize= value.size
    if filesize > 2097152:
        raise ValidationError(f"The maximum file size that can be uploaded is 2mb but found {round(filesize*0.00000095367432,1)}mb")
    else:
        return value


def validate_file_extension(value):
	return FileExtensionValidator(["html"])(value)


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension,validate_file_size])

