from django.shortcuts import render

def favoris_view(request):
    
    return render(request, 'pages/Favoris.html')
