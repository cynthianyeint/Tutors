from PIL import Image
from tuition.settings import VALID_COURSE_IMAGE_FILETYPES

__author__ = 'nyantun'

from django import forms
from tutors.models import CourseImageUpload


class ImageForm(forms.ModelForm):
    images = forms.ImageField(label='Image')

    class Meta:
        model = CourseImageUpload
        fields = ('images', )

    def clean_images(self):
        image = self.cleaned_data.get('images', False)
        if image:
            img_format = Image.open(image.file).format
            image.file.seek(0)
            if img_format.lower() in VALID_COURSE_IMAGE_FILETYPES:
                return image
        raise forms.ValidationError('FileType not supported: only upload jpeg and jpg.')