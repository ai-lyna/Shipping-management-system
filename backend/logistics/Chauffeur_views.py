import json
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render
from .models import Chauffeur
from django.core.paginator import Paginator

def chauffeur_info(request):
    return JsonResponse({
        "nom": "string",
        "prenom": "string",
        "numPermis": "string",
        "telephone": "string",
        "email": "string",
        "adresse": "string",
        "disponibilite": "boolean",
    })


def chauffeur_data(request):
    table_fields = ["nom", "prenom", "numPermis", "telephone", "disponibilite"]
    chauf = Chauffeur.objects.all().order_by("id")  
    sort_order = request.GET.get('sort', 'new')  

    if sort_order == 'old':
        chauf = Chauffeur.objects.all().order_by('id')  
    else:
        chauf = Chauffeur.objects.all().order_by('-id')  
    paginator = Paginator(chauf, 12) 
    page_nbr = request.GET.get("page") 
    page_obj = paginator.get_page(page_nbr) 

    all_data = [
        {
            "id": c.id,
            "nom": c.nom,
            "prenom": c.prenom,
            "numPermis": c.numPermis,
            "telephone": c.telephone,
            "disponibilite": c.disponibilite,
            
        } for c in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {"page_obj": page_obj, "chauffeurs": page_obj, "table_name": "Chauffeurs", "data_structure" : all_data , "headers": table_fields , "sort_order": sort_order})


def chauffeur_id_view(request, chauffeur_id):
    try:
        chauffeur = Chauffeur.objects.get(id=chauffeur_id)
        data = {
            "id": chauffeur.id,
            "nom": chauffeur.nom,
            "prenom": chauffeur.prenom,
            "numPermis": chauffeur.numPermis,
            "telephone": chauffeur.telephone,
            "email": chauffeur.email,
            "disponibilite": chauffeur.disponibilite,
            "adresse": chauffeur.adresse,
            "date_creation": chauffeur.date_creation.strftime("%Y-%m-%d %H:%M"),
        }
        return JsonResponse(data)
    except Chauffeur.DoesNotExist:
        return JsonResponse({"error": "Chauffeur not found"}, status=404)
    
    
def update_chaffeur(request, chauffeur_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            chauffeur = Chauffeur.objects.get(id=chauffeur_id)
            chauffeur.nom = data.get("nom", chauffeur.nom)
            chauffeur.prenom = data.get("prenom", chauffeur.prenom)
            chauffeur.numPermis = data.get("numPermis", chauffeur.numPermis)
            chauffeur.telephone = data.get("telephone", chauffeur.telephone)
            chauffeur.email = data.get("email", chauffeur.email)
            chauffeur.adresse = data.get("adresse", chauffeur.adresse)
            if "disponibilite" in data:
                chauffeur.disponibilite = data["disponibilite"] in [True, "true", "True", 1]
            chauffeur.save()
            
            return JsonResponse({
                "id": chauffeur.id,
                "nom": chauffeur.nom,
                "prenom": chauffeur.prenom,
                "numPermis": chauffeur.numPermis,
                "telephone": chauffeur.telephone,
                "disponibilite": chauffeur.disponibilite,
            })
        except Chauffeur.DoesNotExist:
            return JsonResponse({"error": "Chauffeur not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_chaffeur(request):
    if request.method == "POST":
        data = json.loads(request.body)

        chauffeur = Chauffeur.objects.create(
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            numPermis=data.get("numPermis"),
            telephone=data.get("telephone"),
            disponibilite=data.get("disponibilite", True),
            email=data.get("email"),
            adresse=data.get("adresse"),
        )

        return JsonResponse({
            "id": chauffeur.id,
            "nom": chauffeur.nom,
            "prenom": chauffeur.prenom,
            "numPermis": chauffeur.numPermis,
            "telephone": chauffeur.telephone,
            "disponibilite": chauffeur.disponibilite,
            "email": chauffeur.email,
            "adresse": chauffeur.adresse,
            "date_creation": chauffeur.date_creation.strftime("%Y-%m-%d %H:%M"),
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_chauffeur(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Chauffeur.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg":"chauffeurs deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)


def search_chaffeur(request):
    query = request.GET.get('search').strip()
    chauffeurs = Chauffeur.objects.all() 

    if query:
        chauffeurs = Chauffeur.objects.filter(
            Q(id__icontains=query) | Q(nom__icontains=query) | Q(prenom__icontains=query)
        )

    return render(request, "pages/tables/chauffeurs.html", {"chauffeurs": chauffeurs}, {"query": query})