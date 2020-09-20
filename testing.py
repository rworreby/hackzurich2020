import requests
import json
from app.firebase import get_firebase_db


def id_to_idx(id,key):
    if key == "facilities":
        db = get_firebase_db()
        items = db.child("facilities").get().val()
    elif key == "pickups":
        db = get_firebase_db()
        items = db.child("pickups").get().val()
    else:
        db = get_firebase_db()
        items = db.child("trucks").get().val()

    for idx, i in enumerate(items):
        if i["id"] == id:
            return idx
    print(f"{key}-id {id} not found.")
    return None

def create_get(coords, access_token = "pk.eyJ1IjoibXJmM2xpeCIsImEiOiJjazN5czZzNG0xM2h1M2twNjdydDdkYWxxIn0.erELJKvEEqZev409Z01L3g"):
    get_str = "https://api.mapbox.com/directions/v5/mapbox/driving/"
    for c in coords:
        get_str += f"{c[0]}%2C{c[1]}%3B"
    return get_str[:-3] + f"?alternatives=false&geometries=geojson&steps=true&access_token={access_token}"

def mapbox_call(get_str):
    res = requests.get(get_str)
    if res.status_code == 200:
        res = json.loads(res._content)
        route = res['routes'][0]['geometry']['coordinates']
        duration = res['routes'][0]['duration']
        return  route, duration/60
    else:
        print(res.status_code, res.reason)
        return 0

def from_to(destination_IDs):
    with open('data.json','r') as file:
        destinations = json.load(file)
    coords = []
    payload = 0
    for i, d_id in enumerate(destination_IDs):
        if i == 0:
            lat = destinations['trucks'][d_id]['currentLocationLat']
            long = destinations['trucks'][d_id]['currentLocationLon']
            coords.append([lat, long])
        elif i == len(destination_IDs)-1:
            lat = destinations['facilities'][d_id]['locationLat']
            long = destinations['facilities'][d_id]['locationLog']
            coords.append([lat, long])
        else:
            lat = destinations['pickups'][d_id]['locationLat']
            long = destinations['pickups'][d_id]['locationLog']
            payload += destinations['pickups'][d_id]['payload']
            coords.append([lat, long])
    route, duration = mapbox_call(create_get(coords))
    return route, duration, payload

def calc_pick_ups(threshold = 0, alpha = 2):
    pickup_ids = get_pickups() # Firebase magic happens here
    _, base_duration, _ = from_to([1,5])
    for pid in pickup_ids:
        route, duration, payload = from_to([1,pid,5])
        if 1/duration > threshold:
            possible_pickups.append((alpha*payload/duration,pid,route,duration))
    best_pickup_factor, best_id, route, duration = max(possible_pickups,key=lambda pp: pp[0])
    if best_pickup_factor > threshold:
        return best_id, route, duration
    else:
        return None

def main():
    # route 0-3
    # route, duration = from_to(0, 3)
    # print(len(route), duration)
    # route 0-4
    # route, duration = from_to(0, 4)
    # print(len(route), duration)
    # route 1-5
    route, duration, payload = from_to([1, 5])
    print(len(route), duration, payload)
    route, duration, payload = from_to([1, 0, 5])
    print(len(route), duration, payload)
    route, duration, payload = from_to([1, 0, 1, 5])
    print(len(route), duration, payload)
    return 0

if __name__ == '__main__':
    main()
