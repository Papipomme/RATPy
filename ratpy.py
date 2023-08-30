import json,codecs,requests

with open('api_key', 'r') as api_key:
    API_KEY = api_key.readline()
REQUEST_HEADERS = {
    "Accept": "application/json",
    "apikey": API_KEY
}
BASE_URL = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring"

line_names: dict = {}
stop_names: dict = {}
transport_modes: dict = {}

def get_lines_from_stop(stop_id: str) -> list:
    """Takes a string which is the IDFM id of the stop and returns a list of strings representing the IDFM ids of the lines
    at the stop."""
    lines: list = []

    stop_name = get_stop_name(stop_id)

    with codecs.open("static\\ratp_arrets.json", "r", "utf-8-sig") as read_file:
        data = json.load(read_file)
        
        for stop in data:
            if str(stop['stop_name']) == stop_name:
                lines.append(stop['route_id'])

    return lines

def get_line_name(line_id: str) -> str:
    """Takes a string which reprensents a line's id and returns the long line name."""
    
    if line_id in line_names:
        return line_names[line_id]

    with codecs.open("static\\ratp_lignes.json", "r", "utf-8-sig") as read_file:
        data = json.load(read_file)
        
        for line in data:
            if line['ID_Line'] == line_id:
                line_names[line_id] = line["Name_Line"]
                return line["Name_Line"]
            
        return "Unknown"

def get_stop_name(stop_id: str):
    """Takes a string wich represents a IDFM stop id and returns the stop's name."""
    
    if stop_id in stop_names:
        return stop_names[stop_id]
    
    with codecs.open("static\\ratp_arrets.json", "r", "utf-8-sig") as read_file:
        data = json.load(read_file)
        
        for stop in data:
            if str(stop['stop_id']) == stop_id:
                stop_names[stop_id] = stop["stop_name"]
                return stop["stop_name"]
            
        return "Unknown"

def get_transport_mode(line_id: str) -> str:
    """Takes a string which represents a line's id and returns the transport mode of that specific line."""

    if line_id in transport_modes:
        return transport_modes[line_id]
    
    with codecs.open("static\\ratp_lignes.json", "r", "utf-8-sig") as read_file:
        data = json.load(read_file)
        
        for line in data:
            if line['ID_Line'] == line_id:
                transport_modes[line_id] = line["TransportMode"]
                return line["TransportMode"]
            
        return "Unknown"

lines = get_lines_from_stop("39532")
print(lines)
print( get_stop_name("39532") )
for line in lines:
    print(get_line_name(line), get_transport_mode(line))

def get_next(line_id, stop_id):
    url = BASE_URL + "?MonitoringRef=STIF:StopPoint:Q:" + stop_id + ":" + "&LineRef=STIF:Line::" + line_id + ":"

    req = requests.get(url, headers=REQUEST_HEADERS)
    print('Status', req)
    print(req.content)

get_next("C01141", "7789")