from django.shortcuts import render, redirect
from django.views import View
from . import tasks
from django.contrib import messages


class Home(View):
    def get(self, request):
        return render(request, 'core/home.html')


class Bucket(View):
    template_name = 'core/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})


class BucketDeleteObject(View):
    def get(self, request, name):
        tasks.delete_bucket_objetc_task.delay(name)
        messages.success(request, f'"{name}" deleted success', 'info')
        return redirect('core:bkt-home')


class BucketDownloadObject(View):
    def get(self, request, name):
        tasks.download_bucket_object_task.delay(name)
        messages.success(request, f'"{name}" download success', 'info')
        return redirect('core:bkt-home')
