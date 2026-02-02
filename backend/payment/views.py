from django.shortcuts import render

import json
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render
from .models import Payment
from django.core.paginator import Paginator

def payment_info(request):
    return JsonResponse({
        "client": "number",
        "facture": "number",
        "typePaiement": {
            "type": "choice",
            "choices": [
                {"value": "partiel", "label": "Partiel"},
                {"value": "total", "label": "Total"},
            ]
        },
        "datePaiement": "string",
        "soldePaye": "number",

    })


def payment_data(request):

    table_fields = ["client", "facture", "typePaiement", "datePaiement", "soldePaye"]
    
    payments = Payment.objects.all().order_by("id")  
    sort_order = request.GET.get('sort', 'new')  

    if sort_order == 'old':
         payments = Payment.objects.all().order_by('datePaiement')  
    else:
        payments = Payment.objects.all().order_by('-datePaiement')  
    paginator = Paginator(payments, 12) 
    page_nbr = request.GET.get("page") 
    page_obj = paginator.get_page(page_nbr) 

    all_data = [
        {
            "id": p.id,
            "client": p.client,
            "facture": p.facture,
            "Type": p.typePaiement,
            "Date": p.datePaiement,
            "Versement": p.soldePaye,
        } for p in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {"page_obj": page_obj, "payments": page_obj, "table_name": "Payment", "data_structure" : all_data , "headers": table_fields , "sort_order": sort_order})


def payment_id_view(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        data = {
            "id": payment.id,
            "client": payment.client,
            "facture": payment.facture,
            "Type": payment.typePaiement,
            "Date": payment.datePaiement,
            "Versement": payment.soldePaye,
            "date_creation": payment.date_creation.strftime("%Y-%m-%d %H:%M"),
        }
        return JsonResponse(data)
    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment not found"}, status=404)
    
    
def update_payment(request, payment_id):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            payment = Payment.objects.get(id=payment_id)
            payment.client = data.get("client", payment.client)
            payment.facture = data.get("facture", payment.facture)
            payment.typePaiement = data.get("Type", payment.typePaiement)
            payment.datePaiement = data.get("Date", payment.datePaiement)
            payment.soldePaye = data.get("Versement", payment.soldePaye)
            payment.save()
            
            return JsonResponse({
                "id": payment.id,
                "client": payment.client,
                "facture": payment.facture,
                "Type": payment.typePaiement,
                "Date": payment.datePaiement,
                "Versement": payment.soldePaye
            })
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        payment = Payment.objects.create(
            client = data.get("client"),
            facture = data.get("facture"),
            typePaiement = data.get("Type"),
            datePaiement = data.get("Date"),
            soldePaye = data.get("Versement", 0)
        )

        return JsonResponse({
            "id": payment.id,
            "client": payment.client,
            "facture": payment.facture,
            "Type": payment.typePaiement,
            "Date": payment.datePaiement,
            "Versement": payment.soldePaye,
            "date_creation": payment.date_creation.strftime("%Y-%m-%d %H:%M")
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_payment(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Payment.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg":"payments deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)


def search_payment(request):
    query = request.GET.get('search').strip()
    payment = Payment.objects.all() 

    if query:
        payment = Payment.objects.filter(
            Q(id__icontains=query) | Q(typePaiement__icontains=query)
        )

    return render(request, "pages/tables/payment.html", {"payments": payment}, {"query": query})