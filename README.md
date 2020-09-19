# hackzurich2020
Hack Zürich Repo for LafargeHolcim Challenge

```bash
# Everytime starting the server
export FLASK_APP=app
export FLASK_ENV=development
flask run

# First time run this:
flask init-db

# Fill database with mock data
flask insert-mock-data-db
```

## Endpoints

**Bold** endpoints need to be implemented.

- [x] **Show all pickups: GET /api/pickups**
- [ ] Show specific pickup: GET /api/pickups/{id}
- [x] **Store pickup: POST /api/pickups**
- [ ] **Edit pickup: PUT /api/pickups/{id}** <!-- Accept and reject pickups -->
- [ ] Delete pickup: DELETE /api/pickups/{id}
- [x] **Show all fahrten: GET /api/fahrten**
- [ ] Show specific fahrt: GET /api/fahrten/{id}
- [x] **Store fahrt: POST /api/fahrten**
- [ ] Edit fahrt: PUT /api/fahrten/{id}
- [ ] Delete fahrt: DELETE /api/fahrten/{id}
- [x] **Show all facilities: GET /api/facilities**
- [ ] Show specific facility: GET /api/facilities/{id}
- [ ] Store facility: POST /api/facilities
- [ ] Edit facility: PUT /api/facilities/{id}
- [ ] Delete facility: DELETE /api/facilities/{id}
