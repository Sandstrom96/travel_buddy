"""Airport and hotel data for major Japanese cities"""

AIRPORTS = {
    "osaka": [
        {
            "code": "KIX",
            "name": "Kansai Inernational Airport",
            "latitude": 34.4347,
            "longitude": 135.2441,
            "distance_to_city_center_km": 50
        },
        {
            "code": "ITM",
            "name": "Osaka itami Airport",
            "latitude": 34.7855,
            "longitude": 135.4384,
            "distance_to_city_center_km": 15
        }
    ],
    "tokyo": [
        {
            "code": "NTR",
            "name": "Narita International Airport",
            "latitude": 35.7720,
            "longitude": 140.3929,
            "distance_to_city_center_km": 70
        },
        {
            "code": "HND",
            "name": "Tokyo Haneda Airport",
            "latitude": 35.5494,
            "longitude": 139.7798,
            "distance_to_city_center_km": 20

        }
    ],
    "kyoto": [
        {
            "code": "KIX",
            "name": "Kansai International Airport",
            "latitude": 34.4347,
            "longitude": 135.2441,
            "distance_to_city_center_km": 95
        },
        {
            "code": "ITM",
            "name": "Osaka Itami Airport",
            "latitude": 34.7855,
            "longitude": 135.4384,
            "distance_to_city_center_km": 55
        }
    ]
}

HOTEL_AREAS = {
    "osaka": [
        {
            "name": "Dotonbori / Namba",
            "latitude": 34.6686,
            "longitude": 135.5018,
            "description": "Vibrant entertaiment district with shopping and dining"
        },
        {
            "name": "Umeda / Osaka Station",
            "latitude": 34.7024,
            "longitude": 135.4959,
            "description": "Major business and transport hub with modern hotels"
        },
        {
            "name": "Shin-Osaka",
            "latitude": 34.7335,
            "longitude": 135.5003,
            "description": "Convenient for Shinkansen connections"
        }
    ],
    "tokyo": [
        {
            "name": "Shinjuku",
            "latitude": 35.6896,
            "longitude": 139.7006,
            "description": "Bustling area with skyscrapers, shopping, and nighlife"
        },
        {
            "name": "Shibuya",
            "latitude": 35.6595,
            "longitude": 139.7004,
            "description": "Trendy district famous for the Shibuya crossing"
        },
        {
            "name": "Asakusa",
            "latitude": 35.7148,
            "longitude": 139.7967,
            "description": "Traditional area near Sensoji Temple"
        }
    ],
    "kyoto": [
        {
            "name": "Kyoto Station Area",
            "latitude": 34.9859,
            "longitude": 135.7581,
            "description": "Central location with easy access to trains"
        },
        {
            "name": "Gion / DownTown",
            "latitude": 35.0036,
            "longitude": 135.7750,
            "description": "Historic geisha district with traditional atmosphere"
        },
        {
            "name": "Arashiyama",
            "latitude": 35.0094,
            "longitude": 135.6686,
            "description": "Scenic area with bamboo groves and temples"
        }
    ]
}