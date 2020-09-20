import requests
import json
from app.firebase import get_firebase_db
import time
import numpy as np
from numpy import linalg as LA
from testing import id_to_idx


def create_get(coords, access_token = "pk.eyJ1IjoibXJmM2xpeCIsImEiOiJjazN5czZzNG0xM2h1M2twNjdydDdkYWxxIn0.erELJKvEEqZev409Z01L3g"):
    get_str = "https://api.mapbox.com/directions/v5/mapbox/driving/"
    for c in coords:
        get_str += f"{c[1]}%2C{c[0]}%3B"
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

    db = get_firebase_db()
    trucks = db.child("trucks").get().val()

    coords = []
    payload = 0
    for i, d_id in enumerate(destination_IDs):
        if i == 0:
            idx = id_to_idx(d_id,"facilities")
            lat = trucks[idx]['currentLocationLat']
            long = trucks[idx]['currentLocationLon']
            coords.append([lat, long])
        elif i == len(destination_IDs)-1:
            idx = id_to_idx(d_id,"facilities")
            lat = facilities[idx]['locationLat']
            long = facilities[idx]['locationLog']
            coords.append([lat, long])
        else:
            idx = id_to_idx(d_id,"pickups")
            lat = pickups[idx]['locationLat']
            long = pickups[idx]['locationLog']
            payload += pickups[idx]['payload']
            coords.append([lat, long])
    route, duration = mapbox_call(create_get(coords))
    return route, duration, payload


def calc_pick_ups(indices, threshold = 0, alpha = 2):
    db = get_firebase_db()
    pickups = db.child("pickups").get().val()
    _, base_duration, _ = from_to(id_to_idx(indides[0]),id_to_idx(indides[1]))
    for p in pickups:
        route, duration, payload = from_to(id_to_idx(indides[0]),id_to_idx(p["id"]),id_to_idx(indices[1]))
        if alpha*payload/duration > threshold:
            possible_pickups.append((alpha*payload/duration,p["id"],route,duration))
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


def angle_from_route(route):
    angle = []
    for i in range(len(route) - 1):
        vector_1 = [0, 1]
        vector_2 = [
            route[i][0] - route[i + 1][0],
            route[i][1] - route[i + 1][1]
        ]

        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        
        angle.append(np.arccos(dot_product))
    angle.append(np.arccos(dot_product))

def main():
    # r = requests.delete('http://127.0.0.1:5000/api/trucks')
    r = requests.delete('http://127.0.0.1:5000/api/trucks')

    r = requests.post('http://127.0.0.1:5000/api/trucks', data={
        'userId': '321',
        'currentLocationLon': 5.75766658782959,
        'currentLocationLat': 5.67044448852539,
        'homeLocationLon': 5.75766658782959,
        'homeLocationLat': 5.67044448852539,
        'payload': 'concret',
        'maxLoad': '1',
        'angle': '0',
        'route': ''
    })

    r = requests.post('http://127.0.0.1:5000/api/trucks', data={
        'userId': '321',
        'currentLocationLon': 11.4774446487427,
        'currentLocationLat': 10.9261665344238,
        'homeLocationLon': 11.4774446487427,
        'homeLocationLat': 10.9261665344238,
        'payload': 'concret',
        'maxLoad': '1',
        'angle': '0',
        'route': ''
    })

    r = requests.post('http://127.0.0.1:5000/api/trucks', data={
        'userId': '321',
        'currentLocationLon': 11.4774446487427,
        'currentLocationLat': 10.9261665344238,
        'homeLocationLon': 11.4774446487427,
        'homeLocationLat': 10.9261665344238,
        'payload': 'concret',
        'maxLoad': '1',
        'angle': '0',
        'route': ''
    })

    from_tos = [
        [0, 5],
        # [1, 6],
        [1, 7],
        # [2, 8],
        [2, 9],
    ]
    routes = []
    durations = []
    trucks = []
    # angles = []

    for i, l in enumerate(from_tos):
        route, duration, payload = from_to(l)
        # print(route, interpolate_route(route), sep="\n*********\n")
        # print(len(route), len(interpolate_route(route)))

        # route = interpolate_route(route)

        route = route + route[::-1]
        # angle = angle_from_route(route)

        # print(angle)

        r = requests.put('http://127.0.0.1:5000/api/trucks/' + str(i), data={
            'userId': '321',
            'currentLocationLon': route[0][0],
            'currentLocationLat': route[0][1],
            'homeLocationLon': route[0][1],
            'homeLocationLat': route[0][0],
            'payload': 'concret',
            'maxLoad': '1',
            'angle': 0, #angle[0],
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
                    'angle': 0, #angles[j][i],
                    'route': json.dumps(routes[j])
                })

    return 0

if __name__ == '__main__':
    main()
