import json
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Trajet



def trajet_info(request):
    return JsonResponse({
        "kilometrage": "number",
        "duree": "duration (HH:MM:SS)",
        "consommation_carb": "number"
    })



def trajet_data(request):

    table_fields = ["kilometrage", "duree", "consommation_carb"]

    trajets = Trajet.objects.all().order_by("-id")

    sort_order = request.GET.get("sort", "new")
    if sort_order == "old":
        trajets = trajets.order_by("id")
    else:
        trajets = trajets.order_by("-id")

    paginator = Paginator(trajets, 12)
    page_nbr = request.GET.get("page")
    page_obj = paginator.get_page(page_nbr)

    all_data = [
        {
            "id": t.id,
            "kilometrage": t.kilometrage,
            "duree": str(t.duree),
            "consommation_carb": t.consommation_carb
        }
        for t in page_obj.object_list
    ]

    return render(request, "pages/main.html", {
        "page_obj": page_obj,
        "trajets": page_obj,
        "table_name": "Trajets",
        "data_structure": all_data,
        "headers": table_fields,
        "sort_order": sort_order
    })



def trajet_id_view(request, trajet_id):
    try:
        t = Trajet.objects.get(id=trajet_id)
        return JsonResponse({
            "id": t.id,
            "kilometrage": t.kilometrage,
            "duree": str(t.duree),
            "consommation_carb": t.consommation_carb
        })
    except Trajet.DoesNotExist:
        return JsonResponse({"error": "Trajet not found"}, status=404)



def create_trajet(request):
    if request.method == "POST":
        data = json.loads(request.body)

        trajet = Trajet.objects.create(
            kilometrage=data.get("kilometrage"),
            duree=data.get("duree"),
            consommation_carb=data.get("consommation_carb")
        )

        return JsonResponse({
            "id": trajet.id,
            "kilometrage": trajet.kilometrage,
            "duree": str(trajet.duree),
            "consommation_carb": trajet.consommation_carb
        })

    return JsonResponse({"error": "Invalid request"}, status=400)



def update_trajet(request, trajet_id):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            trajet = Trajet.objects.get(id=trajet_id)
            trajet.kilometrage = data.get("kilometrage", trajet.kilometrage)
            trajet.duree = data.get("duree", trajet.duree)
            trajet.consommation_carb = data.get(
                "consommation_carb", trajet.consommation_carb
            )
            trajet.save()

            return JsonResponse({
                "id": trajet.id,
                "kilometrage": trajet.kilometrage,
                "duree": str(trajet.duree),
                "consommation_carb": trajet.consommation_carb
            })
        except Trajet.DoesNotExist:
            return JsonResponse({"error": "Trajet not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)



def delete_trajets(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Trajet.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg": "trajets deleted"})

    return JsonResponse({"error": "Invalid request"}, status=400)
