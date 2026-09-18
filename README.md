# 17 – Masterblog API

## Aufgabe
Der Blog wird zu einer **REST-API**: Das Backend (Flask, Port 5002) liefert
und verändert Beiträge als JSON. Ein getrenntes Frontend (Port 5001) ruft die
API mit JavaScript (`fetch`) auf. Die API ist mit **Swagger** dokumentiert.

## Dateien
- `backend/backend_app.py` – die API
- `backend/static/masterblog.json` – Swagger-Beschreibung der API
- `frontend/frontend_app.py` – liefert die Webseite aus
- `frontend/templates/index.html`, `frontend/static/main.js`, `styles.css`

## Endpunkte
| Methode | URL | Aufgabe | Statuscodes |
|---|---|---|---|
| GET | `/api/posts` | alle Beiträge, optional `?sort=title\|content&direction=asc\|desc` | 200, 400 |
| POST | `/api/posts` | neuen Beitrag anlegen (`title`, `content` Pflicht) | 201, 400 |
| PUT | `/api/posts/<id>` | Beitrag ändern (fehlende Felder bleiben gleich) | 200, 404 |
| DELETE | `/api/posts/<id>` | Beitrag löschen | 200, 404 |
| GET | `/api/posts/search?title=...&content=...` | Beiträge suchen | 200 |
| GET | `/api/docs` | Swagger-Oberfläche | – |

## Wichtige Fachbegriffe
- **REST-API:** Ressourcen (hier: Posts) haben eine URL, die HTTP-Methode
  sagt, was passieren soll (GET lesen, POST anlegen, PUT ändern, DELETE löschen).
- **Statuscodes:** 201 = angelegt, 400 = fehlerhafte Anfrage, 404 = nicht gefunden.
- **`jsonify` / `request.get_json()`:** Python-Daten als JSON senden bzw.
  JSON aus der Anfrage lesen. `silent=True` verhindert einen Absturz bei
  ungültigem JSON.
- **CORS:** Der Browser blockiert Anfragen an einen anderen Port, außer der
  Server erlaubt es. `CORS(app)` setzt die nötigen Header.
- **Sortieren mit `key=` und `reverse=`:** `sorted(..., key=lambda p: p[sort].lower())`.
- **Swagger / OpenAPI:** Maschinenlesbare API-Beschreibung, aus der eine
  klickbare Testoberfläche entsteht (`flask-swagger-ui`).

## Starten
    pip install -r requirements.txt
    python3 backend/backend_app.py     # API auf http://localhost:5002
    python3 frontend/frontend_app.py   # Webseite auf http://localhost:5001
    # Swagger: http://localhost:5002/api/docs
