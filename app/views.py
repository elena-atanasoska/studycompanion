from django.shortcuts import render

# Create your views here.
from app.models import Comment


def your_view(request):
    comments = Comment.objects.all()
    return render(request, 'index.html', {'comments': comments})


