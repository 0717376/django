from django.shortcuts import render


# Create your views here.
def posts_list(request):
    n = ['Sergey', 'Dasha', 'Pasha', 'Masha']
    return render(request, 'blog/index.html', context ={'names': n})