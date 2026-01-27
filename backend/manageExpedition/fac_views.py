import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Facture
from django.core.paginator import Paginator


def facture_info(request):
    return JsonResponse({
        "id_client": "number",
        "date_fact": "YYYY-MM-DD",
    })


def facture_data(request):

    table_fields = ["id_client", "date_fact", "montant_HT", "montant_TTC"]
    
    search_value = "" 
    factures = Facture.objects.all().order_by("id") 

    if 'search' in request.GET:
        search_value = request.GET['search']
        if search_value:  
            factures = Facture.objects.filter(id_client__nom__istartswith=search_value)

    sort_order = request.GET.get('sort', 'new')  

    if sort_order == 'old':
        factures = factures.order_by('id')  
    else:
        factures = factures.order_by('-id')  

    paginator = Paginator(factures, 12) 
    page_nbr = request.GET.get("page") 
    page_obj = paginator.get_page(page_nbr) 

    all_data = [
        {
            "id": f.id,
            "id_client": f.id_client.id,
            "date_fact": f.date_fact.strftime("%Y-%m-%d"),
            "montant_HT": f.montant_HT,
            "montant_TTC": f.montant_TTC,
        } for f in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {
        "page_obj": page_obj,
        "factures": page_obj,
        "table_name": "Factures",
        "data_structure": all_data,
        "headers": table_fields,
        "sort_order": sort_order,
        "query": search_value
    })


def facture_id_view(request, facture_id):
    try:
        f = Facture.objects.get(id=facture_id)
        data = {
            "id": f.id,
            "id_client": f.id_client.id,
            "date_fact": f.date_fact.strftime("%Y-%m-%d"),
            "montant_HT": f.montant_HT,
            "montant_TTC": f.montant_TTC,
        }
        return JsonResponse(data)
    except Facture.DoesNotExist:
        return JsonResponse({"error": "Facture not found"}, status=404)
    
    
def update_facture(request, facture_id):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            f = Facture.objects.get(id=facture_id)

            from backend.clients.models import Client
            if "id_client" in data:
                f.id_client = Client.objects.get(id=data["id_client"])
            f.save()
            
            return JsonResponse({
                "id": f.id,
                "id_client": f.id_client.id,
                "date_fact": f.date_fact.strftime("%Y-%m-%d"),
                "montant_HT": f.montant_HT,
                "montant_TTC": f.montant_TTC,
            })
        except Facture.DoesNotExist:
            return JsonResponse({"error": "Facture not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_facture(request):
    if request.method == "POST":
        data = json.loads(request.body)

        from backend.clients.models import Client

        f = Facture.objects.create(
            id_client=Client.objects.get(id=data.get("id_client"))
        )

        return JsonResponse({
            "id": f.id,
            "id_client": f.id_client.id,
            "date_fact": f.date_fact.strftime("%Y-%m-%d"),
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_factures(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Facture.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg": "factures deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)