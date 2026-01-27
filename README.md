![Project_Image](swift.png)


## Table of contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Architecture and Design Choices](#architecture-and-design-choices)
- [Usage](#usage)
- [Tech stack](#tech-stack)
- [Setup & Run](#setup--run)

## Overview
This project is an information system for a transport and delivery company.  
It handles clients, expeditions, tours, billing, payments, and incidents.



## Project Structure
```mermaid
graph LR
    A[transport-management-system] --> B[manage.py]
    A --> C[requirements.txt]
    A --> D[db.sqlite3]
    A --> E[package.json]
    A --> F[package-lock.json]
    A --> G[README.md]
    A --> H[.gitignore]
    A --> I[backend--contains apps]
    A --> J[config]
    A --> K[frontend]
    A --> L[node_modules]
    I --> M1[clients]
    I --> M2[historique]
    I --> M3[incidents]
    I --> M4[logistics]
    I --> M5[manageExpedition]
    I --> M6[manageColis]
    I --> M7[manageDestination]
    I --> M8[reclamations]
    I --> M9[typeservice]
    I --> M10[trajet]
    I --> M11[tarification]
    J --> J1[__init__.py]
    J --> J2[asgi.py]
    J --> J3[settings.py]
    J --> J4[urls.py]
    J --> J5[wsgi.py]
    K --> K1[static]
    K --> K2[templates]
    L --> L1[bootstrap-icons]
    L --> L2[.package-lock.json]
    K2 -->K3[components]
    K2 -->K4[pages]
    K3 -->K5[.html components]
    K4 -->K6[dashboard.html]
    K4 -->K7[favoris.html]
    K4 -->K8[main.html]
    N1[models.py]
    N2[views.py]
    N3[urls.py]
    N4[admin.py]
    M1 --> N1
    M1 --> N2
    M1 --> N3
    M1 --> N4
    M2 --> N1
    M2 --> N2
    M2 --> N3
    M2 --> N4
    M3 --> N1
    M3 --> N2
    M3 --> N3
    M3 --> N4
    M4 --> N1
    M4 --> N2
    M4 --> N3
    M4 --> N4
    M5 --> N1
    M5 --> N2
    M5 --> N3
    M5 --> N4
    M6 --> N1
    M6 --> N2
    M6 --> N3
    M6 --> N4
    M7 --> N1
    M7 --> N2
    M7 --> N3
    M7 --> N4
    M8 --> N1
    M8 --> N2
    M8 --> N3
    M8 --> N4
    M9 --> N1
    M9 --> N2
    M9 --> N3
    M9 --> N4
    M10 --> N1
    M10 --> N2
    M10 --> N3
    M10 --> N4
    M11 --> N1
    M11 --> N2
    M11 --> N3
    M11 --> N4

```


## Architecture and Design Choices
- MVC pattern (Model–View–Controller)
- Separation between business logic and presentation
- Centralized database access via Django ORM
### High level architecture diagram
```mermaid
graph LR
    subgraph Frontend [Client Layer]
        direction TB
        A[Web Browser / User Interface]
        B[HTML, CSS, JS, Bootstrap]
        C[AJAX requests / JSON responses]
        A --> B --> C
    end
    subgraph Backend [Server Layer: Django]
        direction TB
        D[Business Logic / Controllers]
        E[JSON API Endpoints]
        D --> E
    end
    subgraph Database [Database Layer]
        F[(SQLite3 Database)]
    end
    C -->|AJAX / JSON| E
    E --> D
    D -->|ORM Queries| F
```
### User Flow Diagram
```mermaid
flowchart LR
    Navigation["Navigation"]
    Navigation -->|Navigate| Features["Favorite"]
    Navigation -->|Navigate| TablesData["Tables & Data"]
    Navigation -->|Navigate| Expeditions["Gestion des Expéditions"]
    Navigation -->|Navigate| Facturation["Facturation & Paiement"]
    Navigation -->|Navigate| Incidents["Gestion des Incidents"]
    Navigation -->|Navigate| Reclamations["Gestion des Réclamations"]
    TablesData --> Client[Table client]
    TablesData --> Chauffeurs[Table Chauffeurs]
    TablesData --> Vehicule[Table Vehicule]
    TablesData --> Destination[Table Destination]
    TablesData --> Typeservice[Table Typeservice]
    TablesData --> Tarification[Table Tarification]
    Client --> Ops
    Chauffeurs --> Ops
    Vehicule --> Ops
    Destination --> Ops
    Typeservice --> Ops
    Tarification --> Ops
    Expeditions --> expedition[Table expedition]
    Expeditions --> Tournee[Table Tournee]
    Tournee --> Ops["Create / View / Modify / Delete / Search / Sort"]
    expedition --> Ops["Create / View / Modify / Delete / Search / Sort"]
    Facturation --> facture[Table facture]
    Facturation --> paiement[Table paiement]
    facture --> Ops
    paiement --> Ops
    Incidents --> Ops
    Reclamations --> Ops
    Navigation --> |Navigate|Dashboard[Dashboard]
```



## Usage

### 1. Access the Application

- Start the development server:
```bash
python manage.py runserver
```

- Open a browser and go to: `http://127.0.0.1:8000`

### 2. Navigate Modules

* **Clients:** view, add, edit, or delete client records.
* **Chauffeur & Vehicule:** view, add, edit, or delete logistics records.
* **Expeditions:** manage shipments, track statuses.
* **Tours:** assign drivers and vehicles.
* **Billing & Payments:** manage invoices and payments.
* **Incidents & Reclamations:** log and track incidents or complaints.

### 3. Module Overview

* **Clients:** manage client information (CRUD operations) and track account balances.
* **Expeditions:** register shipments with **automatically calculated costs** based on:

```
Montant total = Tarif de base + (Poids × Tarif poids) + (Volume × Tarif volume)
```

* **Tours:** assign shipments to drivers and vehicles, track delivery routes.
* **Billing & Payments:** generate invoices, calculate taxes, track partial/full payments, and update client balances automatically.
* **Incidents & Reclamations:** log issues and complaints, associate with shipments, and track resolution status.
* **Analysis & Reporting:** generate dashboards with  delivery success rates, top clients, top drivers, high-incident areas..

### 4. Common Actions

* **CRUD operations:** add, edit, delete records for all tables.
* **Search & Filter:** query all tables and filter based on certain criteria (OLD and NEW).
* **Sort & Pagination:** organize large datasets efficiently.
* **JSON:** all backend responses are returned in JSON format, ready for frontend consumption.

Example JSON response for a client:

```json
    {
        "nom": "string",
        "prenom": "string",
        "telephone": "string",
        "email": "string",
        "solde": "number",
    }
```

### 4. Business Logic Highlights

* **Automatic cost calculation:** shipping costs consider weight, volume, service type, and destination.
* **Tracking & status updates:** shipment statuses evolve : *en transit → en centre de tri → en cours de livraison → livré / échec de livraison*.
* **Invoice & payment management:** partial payments update client balance; 
* **Route management:** tours group shipments, assign drivers/vehicles, and log route metrics (distance, fuel, incidents).

### 5. Developer Tips

* All modules follow the **Django MVC pattern**.
* Each app has `models.py`, `views.py`, `urls.py`, `admin.py`.
* All views return responses in JSON format for data exchange with the user interface.
* Only one table/module example is shown, however all other modules behave similarly.



## Tech stack
- **Backend:** Django (Python 3)  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap  
- **Database:** SQLite3  
- **Dynamic interactions:** AJAX  
- **Conception :** Looping, Visual paradigm


## Setup & Run
1. Clone the repository:  
```bash
git clone <repo-url>
```
2. Install dependencies 
```bash
pip install -r requirements.txt
```
3. Apply migrations
```bash 
python manage.py migrate
```
4. Run the development server
```bash
python manage.py runserver
```
5. Access the project at : http://127.0.0.1:8000

