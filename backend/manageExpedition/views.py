from django.shortcuts import redirect, render
from .forms import ExpeditionForm
from .forms import TourneeForm
from .forms import FactureForm
from .models import Expedition, Tournee , Facture
from django.core.paginator import Paginator


def afficher_expedition(request): #url done 
    exp = Expedition.objects.all().order_by("id")
    paginator = Paginator(exp, 12)  
    page_nbr = request.GET.get("page")
    page = paginator.get_page(page_nbr)
    return render(request,"journalExp.html",{"page": page})




def rechercher_expedition(request) :
    if request.method == "GET" :
        query= request.GET.get('searchField') # asm l field tae html

    if query :
        expeditions = Expedition.objects.filter(id__contains = query)
        
        if expeditions :
            return render(request,"searchExp.html",{"expeditions":expeditions})
    return render(request,"journalExp.html")



def ajouter_expedition(request): #url done 
    if request.method == "POST":
        form = ExpeditionForm(request.POST)

        if form.is_valid() :
            form.save()
            form = ExpeditionForm()
            return render(request, "ajouterExp.html", {"form": form})
    else :
        form = ExpeditionForm()
        return render (request , "ajouterExp.html" , {"form":form})
    



def edit_expedition(request,pk): #url done 
    exp = Expedition.objects.get(id=pk)
    if request.method == 'POST':
            form = ExpeditionForm(request.POST,instance=exp)
            if form.is_valid() :
                form.save()
                return redirect("liste exp")
    
    else :
        form = ExpeditionForm(instance=exp)
        return render(request,"expEdit.html",{"form":form})
    

def delete_expedition(request,pk): #url done 
    exp =Expedition.objects.get(id=pk)
    if request.method== 'GET' :
        exp.delete()
    return redirect("liste exp")



def selected_row_info(request,pk): #url done 
    exp = Expedition.objects.get(id=pk)
    return render (request,"infoExp.html", {"exp":exp})


def selected_row_info_to_print(request,pk): #url done 
    exp = Expedition.objects.get(id=pk)
    return render (request,"infoExpPrint.html", {"exp":exp})



# Here start views tae Tournee ---------------------------------------------------------------------------------------

def afficher_tournee(request): #url done 
    exp = Tournee.objects.all().order_by("id")
    paginator = Paginator(exp, 12)  
    page_nbr = request.GET.get("page")
    page = paginator.get_page(page_nbr)
    return render(request,"journalTournee.html",{"page": page})




def rechercher_tournee(request) :
    if request.method == "GET" :
        query= request.GET.get('searchField') # asm l field tae html

    if query :
        tournee = Tournee.objects.filter(id__contains = query)
        
        if tournee :
            return render(request,"searchTournee.html",{"tournee":tournee})
    return render(request,"journalTournee.html")



def ajouter_tournee(request): #url done 
    if request.method == "POST":
        form = TourneeForm(request.POST)

        if form.is_valid() :
            form.save()
            form = TourneeForm()
            return render(request, "ajouterTour.html", {"form": form})
    else :
        form = TourneeForm()
        return render (request , "ajouterTour.html" , {"form":form})
    



def edit_tournee(request,pk): #url done 
    tour = Tournee.objects.get(id=pk)
    if request.method == 'POST':
            form = TourneeForm(request.POST,instance=tour)
            if form.is_valid() :
                form.save()
                return redirect("liste tournee")
    
    else :
        form = TourneeForm(instance=tour)
        return render(request,"tourneEdit.html",{"form":form})
    

def delete_tournee(request,pk): #url done 
    tour =Tournee.objects.get(id=pk)
    if request.method== 'GET' :
        tour.delete()
    return redirect("liste tournee")



def selected_row_info(request,pk): #url done 
    tour = Tournee.objects.get(id=pk)
    return render (request,"infoTournee.html", {"tour":tour})



#Here start views tae facture ----------------------------------------------------------------


def afficher_facture(request): #url done 
    fact = Facture.objects.all().order_by("id")
    paginator = Paginator(fact, 12)  
    page_nbr = request.GET.get("page")
    page = paginator.get_page(page_nbr)
    return render(request,"journalFacture.html",{"page": page})




def rechercher_facture(request) :
    if request.method == "GET" :
        query= request.GET.get('searchField') # asm l field tae html

    if query :
        fact = Facture.objects.filter(id__contains = query)
        
        if fact :
            return render(request,"searchFacture.html",{"fact":fact})
    return render(request,"journalFacture.html")



def ajouter_facture(request): #url done 
    if request.method == "POST":
        form = FactureForm(request.POST)

        if form.is_valid() :
            form.save()
            form = FactureForm()
            return render(request, "ajouterFacture.html", {"form": form})
    else :
        form = FactureForm()
        return render (request , "ajouterFacture.html" , {"form":form})
    



def edit_facture(request,pk): #url done 
    fact = Facture.objects.get(id=pk)
    if request.method == 'POST':
            form = FactureForm(request.POST,instance=fact)
            if form.is_valid() :
                form.save()
                return redirect("liste facture")
    
    else :
        form = FactureForm(instance=fact)
        return render(request,"factureEdit.html",{"form":form})
    

def delete_facture(request,pk): #url done 
    fact =Facture.objects.get(id=pk)
    if request.method== 'GET' :
        fact.delete()
    return redirect("liste facture")



def selected_row_info(request,pk): #url done 
    fact = Facture.objects.get(id=pk)
    return render (request,"infoFacture.html", {"fact":fact})


def selected_row_info_to_print(request,pk): #url done 
    fact = Facture.objects.get(id=pk)
    return render (request,"infoFacturePrint.html", {"fact":fact})