import requests
import json
from app.firebase import get_firebase_db
import time
import numpy as np
from numpy import linalg as LA

def create_get(lat_start, long_start, lat_end, long_end,access_token = "pk.eyJ1IjoibXJmM2xpeCIsImEiOiJjazN5czZzNG0xM2h1M2twNjdydDdkYWxxIn0.erELJKvEEqZev409Z01L3g"):
    get_str = f"https://api.mapbox.com/directions/v5/mapbox/driving/{lat_start}%2C{long_start}%3B{lat_end}%2C{long_end}?alternatives=false&geometries=geojson&steps=true&access_token={access_token}"
    return get_str

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

def from_to(start_id, end_id):
    db = get_firebase_db()
    facilities = db.child("facilities").get().val()
    lat_start = facilities[start_id]['locationLat']
    long_start = facilities[start_id]['locationLog']
    lat_end = facilities[end_id]['locationLat']
    long_end = facilities[end_id]['locationLog']

    route, duration = mapbox_call(create_get(lat_start, long_start, lat_end, long_end))

    return route + [[lat_end, long_end]], duration

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

    for (f, t) in from_tos:
        route, duration = from_to(f, t)
        print(route, interpolate_route(route), sep="\n*********\n")
        print(len(route), len(interpolate_route(route)))

        route = interpolate_route(route)

        route = route + route[::-1]

        r = requests.post('http://127.0.0.1:5000/api/trucks', data={
            'userId': '321',
            'currentLocationLon': route[0][1],
            'currentLocationLat': route[0][0],
            'homeLocationLon': route[0][1],
            'homeLocationLat': route[0][0],
            'payload': 'concret',
            'maxLoad': '1',
            'angle': '0'
        })

        print(r.status_code)

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
                    'currentLocationLon': routes[j][i][1],
                    'currentLocationLat': routes[j][i][0],
                    'homeLocationLon': truck['homeLocationLon'],
                    'homeLocationLat': truck['homeLocationLat'],
                    'payload': truck['payload'],
                    'maxLoad': truck['maxLoad'],
                    'angle': truck['angle']
                })

    return 0

if __name__ == '__main__':
    main()
