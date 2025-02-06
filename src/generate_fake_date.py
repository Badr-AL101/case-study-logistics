import json
from faker import Faker
import random
from datetime import datetime, timedelta
import sys

fake = Faker()

# A dictionary mapping cities to a list of their respective zones
egypt_cities_zones = {
    "Cairo": {
        "id": 100,
        "zones": {
            "Maadi": 101,
            "Nasr City": 102,
            "Heliopolis": 103,
            "Zamalek": 104
        }
    },
    "Alexandria": {
        "id": 200,
        "zones": {
            "Mansheya": 201,
            "Sidi Gaber": 202,
            "El Raml": 203,
            "Borg El Arab": 204
        }
    },
    "Giza": {
        "id": 300,
        "zones": {
            "Mohandessin": 301,
            "Agouza": 302,
            "Dokki": 303,
            "Sheikh Zayed City": 304
        }
    },
    "Port Said": {
        "id": 400,
        "zones": {
            "Port Fouad": 401,
            "El-Manakh": 402,
            "El-Sharq": 403,
            "El-Dawahi": 404
        }
    },
    "Suez": {
        "id": 500,
        "zones": {
            "Suez El Gedida": 501,
            "Arbaeen": 502,
            "Ganayen": 503,
            "Faisal": 504
        }
    },
    "Luxor": {
        "id": 600,
        "zones": {
            "Karnak": 601,
            "Luxor City": 602,
            "El Tod": 603,
            "Armant": 604
        }
    },
    "Aswan": {
        "id": 700,
        "zones": {
            "Aswan City": 701,
            "Edfu": 702,
            "Kom Ombo": 703,
            "Daraw": 704
        }
    },
    "Hurghada": {
        "id": 800,
        "zones": {
            "Sahl Hasheesh": 801,
            "El Dahar": 802,
            "Sekalla": 803,
            "El Gouna": 804
        }
    },
    "Mansoura": {
        "id": 900,
        "zones": {
            "Talkha": 901,
            "Mansoura City": 902,
            "El Mahalla El Kubra": 903,
            "Dekernes": 904
        }
    }
}

def choose_city_zone():
    city_name, city_info = random.choice(list(egypt_cities_zones.items()))
    zone_name, zone_id = random.choice(list(city_info['zones'].items()))
    city_id = city_info['id']
    return city_name, city_id, zone_name, zone_id

def create_id():
    return fake.uuid4()

def create_cod():
    amount = random.randint(100, 1000)
    is_paid_back = fake.boolean()
    collected_amount = amount if is_paid_back else random.randint(0, amount)
    return {
        "amount": amount,
        "isPaidBack": is_paid_back,
        "collectedAmount": collected_amount
    }

def create_collected_from_business():
    date = fake.date_time_this_year()
    return {
        "date": date.isoformat(),
        "confirmation": {
            "isConfirmed": fake.boolean(),
            "numberOfSmsTrials": random.randint(0, 5)
        }
    }

def create_address(include_optional=True):
    city_name, city_id, zone_name, zone_id = choose_city_zone()
    address = {
        "second_line": fake.street_address(),
        "city": {
            "_id": city_id,
            "name": city_name
        },
        "zone": {
            "name": zone_name,
            "_id": zone_id
        },
        "district": fake.word(),
        "firstLine": fake.address(),
        "geoLocation": [float(fake.latitude()), float(fake.longitude())]
    }
    if include_optional and fake.boolean():
        address["floor"] = str(random.randint(1, 10))
        address["apartment"] = str(random.randint(1, 50))
    return address

def create_user():
    middle_name = fake.first_name() if fake.boolean() else ""
    return {
        "_id": fake.uuid4(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "middleName": middle_name,
        "phone": fake.phone_number()
    }

def create_tracker():
    tracker_type = random.choice(["SEND", "RECEIVED", "IN-TRANSIT", "DELIVERED", "ORDERED"])
    tracker_info = {
        "trackerId": fake.uuid4(),
        "order_id": str(fake.random_int(min=100000, max=999999)),
        "type": tracker_type
    }
    return tracker_info, tracker_type

def create_star():
    return {
        "_id": fake.uuid4(),
        "name": fake.name(),
        "phone": fake.phone_number()
    }

def create_country():
    return {
        "_id": fake.uuid4(),
        "name": "Egypt",
        "code": "EG"
    }

def generate_record():
    tracker_info, tracker_type = create_tracker()
    created_at = fake.date_time_this_year()
    updated_at = created_at + timedelta(days=random.randint(1, 365))
    
    record = {
        "id": create_id(),
        "cod": create_cod(),
        "collectedFromBusiness": create_collected_from_business(),
        "createdAt": created_at.isoformat(),
        "dropoffAddress": create_address(),
        "pickupAddress": create_address(),
        "receiver": create_user(),
        "tracker": tracker_info,
        "updatedAt": updated_at.isoformat(),
        "country": create_country()
    }
    
    # Optional star
    if tracker_type != "ORDERED":
        record['star'] = create_star()

    return record


def generate_data(count):
    return [generate_record() for _ in range(count)]

def main(data_size="medium"):
    small_range = [5000,9999]
    medium_range = [10000,20000]
    large_range = [25000,50000]
    
    data_range = medium_range

    if data_size.lower() == "small":
        data_range = small_range
    elif data_size.lower() == "large":
        data_range = large_range
    
    n_records = random.randint(data_range[0],data_range[1]) 
    print(f'data size is : {data_size}')
    print(f'number of records to generate is {n_records}')
    
    # Generate and save the data
    data = generate_data(n_records)
    today = datetime.now().strftime("%Y%m%d")
    with open(f'/usr/app/data/data_{today}.json', 'w') as f:
        json.dump(data, f, indent=4)

    print("Data generated and saved to 'data.json'")

if __name__ == '__main__':
    # Check if a command-line argument is provided
    if len(sys.argv) > 1:
        data_size = sys.argv[1]
        main(data_size=data_size)   
    else:
        main()