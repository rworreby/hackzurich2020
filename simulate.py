import requests
import json
from app.firebase import get_firebase_db
import time
import numpy as np
from numpy import linalg as LA


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
    db = get_firebase_db()
    facilities = db.child("facilities").get().val()

    db = get_firebase_db()
    pickups = db.child("pickups").get().val()

    coords = []
    payload = 0
    for i, d_id in enumerate(destination_IDs):
        if i == 0 or i == len(destination_IDs)-1:
            lat = facilities[d_id]['locationLat']
            long = facilities[d_id]['locationLog']
            coords.append([lat, long])
        else:
            lat = pickups[d_id]['locationLat']
            long = pickups[d_id]['locationLog']
            payload += pickups[d_id]['payload']
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


def interpolate_route(route):
    # TODO: do the thing...
    step_size = 0.0001
    interpolated_route = []

    interpolated_route.append(route[0])
    for step in route:
        distance = LA.norm(step, 2)
        if distance > step_size:
            lon = step[0]
            lat = step[1]
            interpolated_route.append([lon, lat])
        else:
            interpolated_route.append(step)

    return route

def main():
    r = requests.delete('http://127.0.0.1:5000/api/trucks')

    from_tos = [
        [1, 5],
        # [1, 6],
        [2, 7],
        # [2, 8],
        [2, 9],
    ]
    routes = []
    durations = []
    trucks = []

    for l in from_tos:
        route, duration, payload = from_to(l)
        # print(route, interpolate_route(route), sep="\n*********\n")
        # print(len(route), len(interpolate_route(route)))

        # route = interpolate_route(route)

        # route = route + route[::-1]

        r = requests.post('http://127.0.0.1:5000/api/trucks', data={
            'userId': '321',
            'currentLocationLon': route[0][0],
            'currentLocationLat': route[0][1],
            'homeLocationLon': route[0][1],
            'homeLocationLat': route[0][0],
            'payload': 'concret',
            'maxLoad': '1',
            'angle': '0',
            'route': json.dumps(route)
        })

        truck = r.json()
        routes.append(route)
        durations.append(duration)
        trucks.append(truck)

    max_length = 0
    for route in routes:
        if max_length < len(route):
            max_length = len(route)

    for i in range(max_length):
        time.sleep(0.1)

        for j, truck in enumerate(trucks):
            if i < len(routes[j]):
                r = requests.put('http://127.0.0.1:5000/api/trucks/'+str(truck['id']), data={
                    'userId': truck['userId'],
                    'currentLocationLon': routes[j][i][0],
                    'currentLocationLat': routes[j][i][1],
                    'homeLocationLon': truck['homeLocationLon'],
                    'homeLocationLat': truck['homeLocationLat'],
                    'payload': truck['payload'],
                    'maxLoad': truck['maxLoad'],
                    'angle': truck['angle'],
                    'route': json.dumps(routes[j])
                })

    return 0

if __name__ == '__main__':
    main()
