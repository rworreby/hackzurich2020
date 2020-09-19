# hackzurich2020
Hack Zürich Repo for LafargeHolcim Challenge 

```
# Everytime starting the server
export FLASK_APP=app
export FLASK_ENV=development
flask run

# First time run this:
flask init-db
```

## Endpoints

**Bold** endpoints need to be implemented.

**Show all pickups: GET /api/pickups**
Show specific pickup: GET /api/pickups/{id}
**Store pickup: POST /api/pickups**
**Edit pickup: PUT /api/pickups/{id}** <!-- Accept and reject pickups -->
Delete pickup: DELETE /api/pickups/{id}

**Show all fahrten: GET /api/fahrten**
Show specific fahrt: GET /api/fahrten/{id}
**Store fahrt: POST /api/fahrten**
Edit fahrt: PUT /api/fahrten/{id}
Delete fahrt: DELETE /api/fahrten/{id}

**Show all facilities: GET /api/facilities**
Show specific facility: GET /api/facilities/{id}
Store facility: POST /api/facilities
Edit facility: PUT /api/facilities/{id}
Delete facility: DELETE /api/facilities/{id}