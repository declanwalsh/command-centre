import requests
# http://docs.python-requests.org/en/master/
# requests is a HTTP request library

# Replace with your own information:
api_key = 'l7xxde410bb18efd4606a34b29ce3439e689'         
shared_secret = '79c1f1b9af3b4682ae4cc780ca75b952'

# Leave these:
payload = 'grant_type=client_credentials&scope=user'
auth_url = 'api.transport.nsw.gov.au/auth/oauth/v2/token'

# Send a POST request to get the token back:
token_response = requests.post(('https://{}:{}@{}').format(api_key, shared_secret, auth_url), params=payload)

bearer_token = "Bearer " + token_response.json()['access_token']
print(bearer_token)

# Set the headers for our next request:
headers = {"Authorization":bearer_token}

bus_positions = requests.get('https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses', headers=headers)
print("Retrieved {} bytes").format(len(bus_positions.content))

from google.transit import gtfs_realtime_pb2
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(bus_positions.content)

for entity in feed.entity[:5]:
    print(entity.vehicle.position.latitude,
          entity.vehicle.position.longitude,
          entity.vehicle.position.bearing,
          entity.vehicle.position.speed,
          entity.vehicle.trip.route_id[5:]
         )

import csv
positions_output = [] # a list of lists for bus position data

# put each bus's key data into the list
for entity in feed.entity:
    positions_output.append([entity.vehicle.timestamp,
                             entity.id,
                             entity.vehicle.trip.route_id, 
                             entity.vehicle.trip.trip_id,
                             entity.vehicle.trip.start_time,
                             entity.vehicle.trip.start_date,
                             entity.vehicle.position.latitude, 
                             entity.vehicle.position.longitude,
                             entity.vehicle.position.bearing,
                             entity.vehicle.position.speed,
                             entity.vehicle.position.speed*3.6, #speed in km/h, for convenience
                             entity.vehicle.trip.schedule_relationship, 
                             entity.vehicle.congestion_level,
                             entity.vehicle.occupancy_status,
                             entity.vehicle.trip.route_id[5:] # extracting the route number with string slicing
                            ])

# write the bus position data to the positions.csv
with open("positions.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp','vehicle_id','route_id','trip_id',
                     'start_time','start_date','latitude','longitude',
                     'bearing','speed_ms','speed_kmh', 'schedule_relationship','congestion_level',
                     'occupancy_status','route_number'])
    writer.writerows(positions_output)
