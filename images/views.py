import logging

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from images.forms import UploadForm
from images.models import Image
from images.tables import ImageTable


logger = logging.getLogger(__name__)

import os
from django.shortcuts import render


def gif_view(request):
    # Change this to the directory where your GIFs are stored
    gif_dir = '/path/to/gifs'

    # Use the os module to get a list of all files in the gif_dir
    gif_files = os.listdir(gif_dir)

    # Filter the list of files to only include GIFs
    gifs = [f for f in gif_files if f.endswith('.gif')]

    # Generate the URL for each GIF using the MEDIA_URL setting
    gif_urls = [settings.MEDIA_URL + gif for gif in gifs]

    # Pass the list of GIF URLs to the template as a context variable
    return render(request, 'gifs.html', {'gifs': gif_urls})

def index_view(request):
    images = Image.objects.all()
    image_table = ImageTable(images)
    upload_form = UploadForm()

    return render(request, 'images/index.html', {
        'images': images,
        'image_table': image_table,
        'upload_form': upload_form,
    })


@require_http_methods(["POST"])
def upload_view(request):
    upload_form = UploadForm(data=request.POST, files=request.FILES)

    if upload_form.is_valid():
        upload_form.save(commit=True)
    else:
        logger.warning("Something went wrong with uploading the file.")
        logger.warning(request.POST)
        logger.warning(request.FILES)

    return redirect('images-index')
