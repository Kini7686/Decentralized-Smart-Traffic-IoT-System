import pandas as pd
import random
from datetime import datetime, timedelta

# NYC & US Highway locations
locations = [
    "I-95 Exit 15", "I-87 Exit 7A", "Brooklyn Bridge",
    "Times Square", "George Washington Bridge", "Wall Street",
    "Manhattan Downtown", "Lincoln Tunnel", "Queens Blvd",
    "Bronx Terminal Market", "Staten Island Ferry"
]

# State & Phone Area Codes
state_areas = {
    "NY": ["212", "315", "332", "516", "518", "585", "607", "631", "646", "680", "716", "718", "838", "845", "914", "917", "929"],
    "CA": ["209", "213", "310", "415", "424", "442", "510", "559", "562", "619", "626", "650", "657", "661", "707", "714", "747", "805", "818", "858", "909"],
    "TX": ["210", "214", "254", "281", "325", "346", "361", "409", "430", "432", "469", "512", "682", "713", "726", "737", "806", "817", "830", "832", "903"],
    "FL": ["305", "321", "352", "386", "407", "448", "561", "689", "727", "754", "772", "786", "813", "850", "863", "904", "941", "954"],
    "NJ": ["201", "551", "609", "640", "732", "848", "856", "862", "908", "973"],
    "IL": ["217", "224", "309", "312", "331", "447", "464", "618", "630", "708", "773", "779", "815", "847", "872"]
}

def random_plate():
    st = random.choice(list(state_areas.keys()))
    letters = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numbers = random.randint(1000, 9999)
    return f"{st}-{letters}{numbers}", st

def random_phone(state):
    code = random.choice(state_areas[state])   # area code (e.g. 917)
    prefix = random.randint(200, 999)         # first 3 digits after area
    line = random.randint(0, 9999)            # last 4 digits
    return f"+1-{code}-{prefix}-{line:04d}"

def random_email(plate):
    name = plate.replace("-", "").lower()
    domains = ["gmail.com", "yahoo.com", "outlook.com", "icloud.com"]
    return f"{name}@{random.choice(domains)}"

def random_time():
    start = datetime(2025, 11, 27, random.randint(6, 22), random.randint(0, 59))
    duration = random.randint(10, 60)
    end = start + timedelta(minutes=duration)
    return start.isoformat(), end.isoformat()

data = []

for _ in range(500):
    plate, state = random_plate()
    phone = random_phone(state)
    email = random_email(plate)

    entry = random.choice(locations)
    exit = random.choice(locations)
    while exit == entry:
        exit = random.choice(locations)

    entry_time, exit_time = random_time()

    speed_limit = random.choice([50, 60, 65, 70, 75, 80])
    speed_kmph = round(random.uniform(speed_limit - 15, speed_limit + 20) * 1.60934, 2)
    speed_limit_kmph = round(speed_limit * 1.60934, 2)

    data.append([
        plate, phone, email, entry, exit, entry_time, exit_time,
        speed_kmph, speed_limit_kmph
    ])

df = pd.DataFrame(data, columns=[
    "plate", "phone", "email", "entry_point", "exit_point",
    "entry_time", "exit_time",
    "speed_kmph", "speed_limit_kmph"
])

df.to_csv("us_traffic_data.csv", index=False)
print("✔ Updated dataset with PHONE + EMAIL (500 rows)")
