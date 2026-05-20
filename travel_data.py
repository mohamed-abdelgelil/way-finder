# travel_data.py
# Egypt Travel Data - Single source of truth for all travel information

DESTINATIONS = {
    "cairo": {
        "name": "Cairo",
        "description": "Egypt's sprawling capital, home to the Pyramids of Giza and the Egyptian Museum.",
        "region": "Lower Egypt"
    },
    "luxor": {
        "name": "Luxor",
        "description": "Ancient Thebes, featuring the Valley of the Kings and Karnak Temple.",
        "region": "Upper Egypt"
    },
    "aswan": {
        "name": "Aswan",
        "description": "A serene Nile city known for Philae Temple, felucca rides, and Nubian culture.",
        "region": "Upper Egypt"
    },
    "alexandria": {
        "name": "Alexandria",
        "description": "Mediterranean port city with rich Greco-Roman history and the modern Bibliotheca Alexandrina.",
        "region": "Lower Egypt"
    },
    "hurghada": {
        "name": "Hurghada",
        "description": "Red Sea resort town famous for world-class diving, snorkeling, and sandy beaches.",
        "region": "Red Sea"
    }
}

HOTELS = {
    "cairo": [
        {"name": "Marriott Mena House", "price_per_night": 250, "rating": 4.8},
        {"name": "Cairo Budget Inn", "price_per_night": 45, "rating": 3.5},
        {"name": "Kempinski Nile Hotel", "price_per_night": 180, "rating": 4.5},
    ],
    "luxor": [
        {"name": "Sofitel Winter Palace", "price_per_night": 220, "rating": 4.7},
        {"name": "Nile Valley Hotel", "price_per_night": 55, "rating": 3.8},
    ],
    "aswan": [
        {"name": "Sofitel Legend Old Cataract", "price_per_night": 300, "rating": 4.9},
        {"name": "Basma Hotel", "price_per_night": 70, "rating": 4.0},
    ],
    "alexandria": [
        {"name": "Four Seasons San Stefano", "price_per_night": 200, "rating": 4.6},
        {"name": "Alexander The Great Hotel", "price_per_night": 60, "rating": 3.7},
    ],
    "hurghada": [
        {"name": "Steigenberger Al Dau Beach", "price_per_night": 150, "rating": 4.4},
        {"name": "Sea Star Beau Rivage", "price_per_night": 65, "rating": 3.9},
    ],
}

RESTAURANTS = {
    "cairo": [
        {"name": "Abou El Sid", "cuisine_type": "Egyptian", "price_range": 30},
        {"name": "Sequoia", "cuisine_type": "Mediterranean", "price_range": 55},
        {"name": "Zooba", "cuisine_type": "Egyptian Street Food", "price_range": 12},
    ],
    "luxor": [
        {"name": "Sofra Restaurant", "cuisine_type": "Egyptian", "price_range": 20},
        {"name": "Al Moudira Restaurant", "cuisine_type": "Middle Eastern", "price_range": 45},
    ],
    "aswan": [
        {"name": "The Terrace", "cuisine_type": "International", "price_range": 40},
        {"name": "Nubian House", "cuisine_type": "Nubian", "price_range": 18},
    ],
    "alexandria": [
        {"name": "Balbaa Village", "cuisine_type": "Seafood", "price_range": 25},
        {"name": "White and Blue", "cuisine_type": "Greek-Egyptian", "price_range": 35},
    ],
    "hurghada": [
        {"name": "Moby Dick", "cuisine_type": "Seafood", "price_range": 30},
        {"name": "The Lodge", "cuisine_type": "International", "price_range": 22},
    ],
}

ACTIVITIES = {
    "cairo": [
        {"name": "Pyramids of Giza Tour", "description": "Guided tour of the Great Pyramids and Sphinx", "cost": 60},
        {"name": "Egyptian Museum Visit", "description": "Explore ancient artifacts and mummies", "cost": 25},
        {"name": "Khan El Khalili Bazaar Walk", "description": "Wander through Cairo's historic market district", "cost": 10},
    ],
    "luxor": [
        {"name": "Valley of the Kings", "description": "Explore royal tombs of ancient pharaohs", "cost": 50},
        {"name": "Karnak Temple Tour", "description": "Visit the vast ancient temple complex", "cost": 40},
    ],
    "aswan": [
        {"name": "Philae Temple Visit", "description": "Boat ride to the island temple of Isis", "cost": 35},
        {"name": "Felucca Nile Cruise", "description": "Traditional sailboat ride on the Nile at sunset", "cost": 20},
    ],
    "alexandria": [
        {"name": "Bibliotheca Alexandrina Tour", "description": "Visit the modern library and its museums", "cost": 15},
        {"name": "Qaitbay Citadel Visit", "description": "Explore the 15th-century Mediterranean fortress", "cost": 10},
    ],
    "hurghada": [
        {"name": "Red Sea Snorkeling Trip", "description": "Boat trip to coral reefs with snorkeling gear", "cost": 45},
        {"name": "Desert Safari by Quad Bike", "description": "Quad bike adventure through the Eastern Desert", "cost": 55},
    ],
}
