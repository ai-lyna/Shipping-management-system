import json
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render
from .models import Client
from django.core.paginator import Paginator

def client_info(request):
    return JsonResponse({
        "nom": "string",
        "prenom": "string",
        "telephone": "string",
        "email": "string",
        "solde": "number",
    })



def client_data(request):

    table_fields = ["nom", "prenom", "telephone", "email", "solde"]
    
    cli = Client.objects.all().order_by("id")  
    sort_order = request.GET.get('sort', 'new')  

    if sort_order == 'old':
        cli = Client.objects.all().order_by('date_creation')  
    else:
        cli = Client.objects.all().order_by('-date_creation')  
    paginator = Paginator(cli, 12) 
    page_nbr = request.GET.get("page") 
    page_obj = paginator.get_page(page_nbr) 

    all_data = [
        {
            "id": c.id,
            "nom": c.nom,
            "prenom": c.prenom,
            "telephone": c.telephone,
            "email": c.email,
            "solde": c.solde,
        } for c in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {"page_obj": page_obj, "clients": page_obj, "table_name": "Clients", "data_structure" : all_data , "headers": table_fields , "sort_order": sort_order})


def client_id_view(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
        data = {
            "id": client.id,
            "nom": client.nom,
            "prenom": client.prenom,
            "telephone": client.telephone,
            "email": client.email,
            "solde": str(client.solde),
            "date_creation": client.date_creation.strftime("%Y-%m-%d %H:%M"),
        }
        return JsonResponse(data)
    except Client.DoesNotExist:
        return JsonResponse({"error": "Client not found"}, status=404)
    
    
def update_client(request, client_id):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            client = Client.objects.get(id=client_id)
            client.nom = data.get("nom", client.nom)
            client.prenom = data.get("prenom", client.prenom)
            client.telephone = data.get("telephone", client.telephone)
            client.email = data.get("email", client.email)
            client.solde = data.get("solde", client.solde)
            client.save()
            
            return JsonResponse({
                "id": client.id,
                "nom": client.nom,
                "prenom": client.prenom,
                "telephone": client.telephone,
                "email": client.email,
                "solde": client.solde
            })
        except Client.DoesNotExist:
            return JsonResponse({"error": "Client not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_client(request):
    if request.method == "POST":
        data = json.loads(request.body)

        client = Client.objects.create(
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            telephone=data.get("telephone"),
            email=data.get("email"),
            solde=data.get("solde", 0)
        )

        return JsonResponse({
            "id": client.id,
            "nom": client.nom,
            "prenom": client.prenom,
            "telephone": client.telephone,
            "email": client.email,
            "solde": client.solde,
            "date_creation": client.date_creation.strftime("%Y-%m-%d %H:%M")
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_clients(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Client.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg":"clients deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)


def search_client(request):
    query = request.GET.get('search').strip()
    clients = Client.objects.all() 

    if query:
        clients = Client.objects.filter(
            Q(id__icontains=query) | Q(nom__icontains=query) | Q(prenom__icontains=query)
        )

    return render(request, "pages/tables/clients.html", {"clients": clients}, {"query": query})