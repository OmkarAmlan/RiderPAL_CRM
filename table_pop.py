import sqlite3
import json

# JSON data
entry = [
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123456",
            "customer_name": "John Smith",
            "driver_name": "Navjyot",
            "delivery_address": "123 Main St, Anytown, ST 12345",
            "items": [
                {"name": "Chicken Burger", "quantity": 2, "special_instructions": "No mayo"},
                {"name": "French Fries", "quantity": 1, "special_instructions": "Extra crispy"}
            ],
            "order_status": "In Transit",
            "estimated_delivery": "2:30 PM"
        },
        "RIDER_DETAILS": {
            "name": "Navjyot",
            "current_location": "456 Oak Avenue, Anytown, ST 12345",
            "current_coordinates": {"lat": "40.7128", "lng": "-74.0060"},
            "vehicle": "Honda Activa",
            "rating": "4.8"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Restaurant XYZ, 789 Pine St, Anytown, ST 12345",
            "pickup_coordinates": {"lat": "40.7120", "lng": "-74.0050"},
            "delivery_point": "123 Main St, Anytown, ST 12345",
            "delivery_coordinates": {"lat": "40.7140", "lng": "-74.0070"},
            "estimated_distance": "2.5 km",
            "estimated_time": "15 minutes",
            "waypoints": [
                "Take right from Pine St",
                "Continue on Oak Avenue",
                "Left turn onto Main St",
                "Destination will be on your right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123457",
            "customer_name": "Alice Johnson",
            "driver_name": "Rajiv",
            "delivery_address": "78 Elm St, Anytown, ST 12345",
            "items": [
                {"name": "Veg Pizza", "quantity": 1, "special_instructions": "Extra cheese"},
                {"name": "Coke", "quantity": 2, "special_instructions": "Chilled"}
            ],
            "order_status": "Delivered",
            "estimated_delivery": "1:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Rajiv",
            "current_location": "100 Maple Street, Anytown, ST 12345",
            "current_coordinates": {"lat": "40.7138", "lng": "-74.0080"},
            "vehicle": "Suzuki Access",
            "rating": "4.5"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Pizzeria ABC, 50 Maple St, Anytown, ST 12345",
            "pickup_coordinates": {"lat": "40.7115", "lng": "-74.0055"},
            "delivery_point": "78 Elm St, Anytown, ST 12345",
            "delivery_coordinates": {"lat": "40.7150", "lng": "-74.0090"},
            "estimated_distance": "3.0 km",
            "estimated_time": "20 minutes",
            "waypoints": [
                "Head north on Maple St",
                "Turn left at Oak Avenue",
                "Continue straight to Elm St",
                "Destination on the left"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123458",
            "customer_name": "Michael Lee",
            "driver_name": "Amit",
            "delivery_address": "42 Birch Rd, Anytown, ST 12345",
            "items": [
                {"name": "Pasta Alfredo", "quantity": 1, "special_instructions": "Extra sauce"},
                {"name": "Garlic Bread", "quantity": 2, "special_instructions": "Less butter"}
            ],
            "order_status": "Out for Delivery",
            "estimated_delivery": "3:00 PM"
        },
        "RIDER_DETAILS": {
            "name": "Amit",
            "current_location": "200 Cedar Avenue, Anytown, ST 12345",
            "current_coordinates": {"lat": "40.7155", "lng": "-74.0105"},
            "vehicle": "TVS Jupiter",
            "rating": "4.7"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Italiano Resto, 75 Cedar Ave, Anytown, ST 12345",
            "pickup_coordinates": {"lat": "40.7123", "lng": "-74.0068"},
            "delivery_point": "42 Birch Rd, Anytown, ST 12345",
            "delivery_coordinates": {"lat": "40.7162", "lng": "-74.0110"},
            "estimated_distance": "4.0 km",
            "estimated_time": "25 minutes",
            "waypoints": [
                "Proceed straight on Cedar Ave",
                "Turn right onto Birch Rd",
                "Destination will be on the right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123466",
            "customer_name": "Michael Green",
            "driver_name": "Raj Patel",
            "delivery_address": "34 Cherry Ln, Anytown, ST 12347",
            "items": [
                {"name": "Cheeseburger", "quantity": 1, "special_instructions": "No pickles"},
                {"name": "Fries", "quantity": 1, "special_instructions": "Salt only"}
            ],
            "order_status": "Preparing",
            "estimated_delivery": "4:15 PM"
        },
        "RIDER_DETAILS": {
            "name": "Raj Patel",
            "current_location": "Burger Joint, 400 Main St, Anytown, ST 12346",
            "current_coordinates": {"lat": "40.7160", "lng": "-74.0120"},
            "vehicle": "Honda Dio",
            "rating": "4.5"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Burger Joint, 400 Main St, Anytown, ST 12346",
            "pickup_coordinates": {"lat": "40.7160", "lng": "-74.0120"},
            "delivery_point": "34 Cherry Ln, Anytown, ST 12347",
            "delivery_coordinates": {"lat": "40.7135", "lng": "-74.0070"},
            "estimated_distance": "2.7 km",
            "estimated_time": "17 minutes",
            "waypoints": [
                "Head east on Main St",
                "Turn left onto Cherry Ln",
                "Destination on the right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123467",
            "customer_name": "Sarah Wilson",
            "driver_name": "Aisha Khan",
            "delivery_address": "78 Birch St, Anytown, ST 12348",
            "items": [
                {"name": "Pad Thai", "quantity": 1, "special_instructions": "Extra peanuts"},
                {"name": "Thai Iced Tea", "quantity": 1, "special_instructions": "Less sweet"}
            ],
            "order_status": "Ready for Pickup",
            "estimated_delivery": "4:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Aisha Khan",
            "current_location": "Thai Palace, 500 Elm St, Anytown, ST 12347",
            "current_coordinates": {"lat": "40.7140", "lng": "-74.0080"},
            "vehicle": "Hero Maestro",
            "rating": "4.8"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Thai Palace, 500 Elm St, Anytown, ST 12347",
            "pickup_coordinates": {"lat": "40.7140", "lng": "-74.0080"},
            "delivery_point": "78 Birch St, Anytown, ST 12348",
            "delivery_coordinates": {"lat": "40.7115", "lng": "-74.0030"},
            "estimated_distance": "3.1 km",
            "estimated_time": "21 minutes",
            "waypoints": [
                "Go south on Elm St",
                "Right turn onto Birch St",
                "Destination on the left"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123468",
            "customer_name": "Jose Rodriguez",
            "driver_name": "Navdeep Kaur",
            "delivery_address": "123 Oak Rd, Anytown, ST 12346",
            "items": [
                {"name": "Tofu Scramble", "quantity": 1, "special_instructions": "Extra hot sauce"},
                {"name": "Soy Latte", "quantity": 1, "special_instructions": "No foam"}
            ],
            "order_status": "Out for Delivery",
            "estimated_delivery": "5:15 PM"
        },
        "RIDER_DETAILS": {
            "name": "Navdeep Kaur",
            "current_location": "Vegan Cafe, 600 Oak Ave, Anytown, ST 12345",
            "current_coordinates": {"lat": "40.7120", "lng": "-74.0050"},
            "vehicle": "Suzuki Let's",
            "rating": "4.6"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Vegan Cafe, 600 Oak Ave, Anytown, ST 12345",
            "pickup_coordinates": {"lat": "40.7120", "lng": "-74.0050"},
            "delivery_point": "123 Oak Rd, Anytown, ST 12346",
            "delivery_coordinates": {"lat": "40.7155", "lng": "-74.0110"},
            "estimated_distance": "3.5 km",
            "estimated_time": "24 minutes",
            "waypoints": [
                "Drive west on Oak Ave",
                "Turn onto Oak Rd",
                "Destination is on the right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123469",
            "customer_name": "Kim Lee",
            "driver_name": "Vikram Singh",
            "delivery_address": "456 Pine St, Anytown, ST 12347",
            "items": [
                {"name": "Ramen", "quantity": 1, "special_instructions": "Soft egg"},
                {"name": "Sake", "quantity": 1, "special_instructions": "Cold"}
            ],
            "order_status": "In Transit",
            "estimated_delivery": "5:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Vikram Singh",
            "current_location": "700 Pine Ln, Anytown, ST 12346",
            "current_coordinates": {"lat": "40.7100", "lng": "-74.0020"},
            "vehicle": "TVS Wego",
            "rating": "4.7"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Restaurant ABC, 100 Pine Ave, Anytown, ST 12345",
            "pickup_coordinates": {"lat": "40.7110", "lng": "-74.0040"},
            "delivery_point": "456 Pine St, Anytown, ST 12347",
            "delivery_coordinates": {"lat": "40.7130", "lng": "-74.0060"},
            "estimated_distance": "2.9 km",
            "estimated_time": "19 minutes",
            "waypoints": [
                "Continue on Pine Ave",
                "Turn right onto Pine St",
                "Destination on the left"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123470",
            "customer_name": "Emily Carter",
            "driver_name": "Priya Sharma",
            "delivery_address": "789 Elm Rd, Anytown, ST 12348",
            "items": [
                {"name": "Pizza", "quantity": 1, "special_instructions": "Mushroom and pepperoni"},
                {"name": "Lemonade", "quantity": 1, "special_instructions": "Extra ice"}
            ],
            "order_status": "Delivered",
            "estimated_delivery": "6:15 PM"
        },
        "RIDER_DETAILS": {
            "name": "Priya Sharma",
            "current_location": "200 Elm St, Anytown, ST 12347",
            "current_coordinates": {"lat": "40.7145", "lng": "-74.0085"},
            "vehicle": "Honda Activa",
            "rating": "4.9"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Restaurant XYZ, 200 Elm St, Anytown, ST 12346",
            "pickup_coordinates": {"lat": "40.7145", "lng": "-74.0100"},
            "delivery_point": "789 Elm Rd, Anytown, ST 12348",
            "delivery_coordinates": {"lat": "40.7110", "lng": "-74.0020"},
            "estimated_distance": "3.3 km",
            "estimated_time": "22 minutes",
            "waypoints": [
                "Drive south on Elm St",
                "Take a right onto Elm Rd",
                "Destination on the right"
            ]
        }
    },
      {
        "ORDER_DETAILS": {
            "order_id": "ORD123471",
            "customer_name": "Jennifer Martinez",
            "driver_name": "David Lee",
            "delivery_address": "112 Forest Dr, Anytown, ST 12349",
            "items": [
                {"name": "Pasta", "quantity": 1, "special_instructions": "Extra garlic"},
                {"name": "Breadsticks", "quantity": 1, "special_instructions": "With cheese"}
            ],
            "order_status": "Received",
            "estimated_delivery": "6:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "David Lee",
            "current_location": "Italian Place, 321 Maple Ave, Anytown, ST 12348",
            "current_coordinates": {"lat": "40.7150", "lng": "-74.0100"},
            "vehicle": "Yamaha Zuma",
            "rating": "4.6"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Italian Place, 321 Maple Ave, Anytown, ST 12348",
            "pickup_coordinates": {"lat": "40.7150", "lng": "-74.0100"},
            "delivery_point": "112 Forest Dr, Anytown, ST 12349",
            "delivery_coordinates": {"lat": "40.7125", "lng": "-74.0050"},
            "estimated_distance": "2.8 km",
            "estimated_time": "18 minutes",
            "waypoints": [
                "Head north on Maple Ave",
                "Turn left onto Forest Dr",
                "Destination on the left"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123472",
            "customer_name": "Brian Johnson",
            "driver_name": "Sunita Kumar",
            "delivery_address": "223 Hill St, Anytown, ST 12350",
            "items": [
                {"name": "Curry", "quantity": 1, "special_instructions": "Medium spice"},
                {"name": "Rice", "quantity": 1, "special_instructions": "Basmati"}
            ],
            "order_status": "Preparing",
            "estimated_delivery": "7:15 PM"
        },
        "RIDER_DETAILS": {
            "name": "Sunita Kumar",
            "current_location": "Indian Hut, 432 Pine Ln, Anytown, ST 12349",
            "current_coordinates": {"lat": "40.7130", "lng": "-74.0075"},
            "vehicle": "Bajaj Chetak",
            "rating": "4.8"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Indian Hut, 432 Pine Ln, Anytown, ST 12349",
            "pickup_coordinates": {"lat": "40.7130", "lng": "-74.0075"},
            "delivery_point": "223 Hill St, Anytown, ST 12350",
            "delivery_coordinates": {"lat": "40.7105", "lng": "-74.0025"},
            "estimated_distance": "3.2 km",
            "estimated_time": "21 minutes",
            "waypoints": [
                "Travel south on Pine Ln",
                "Take a right turn onto Hill St",
                "Destination on the right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123473",
            "customer_name": "Michelle Davis",
            "driver_name": "Carlos Garcia",
            "delivery_address": "334 River Rd, Anytown, ST 12351",
            "items": [
                {"name": "Enchiladas", "quantity": 1, "special_instructions": "Sour cream"},
                {"name": "Soda", "quantity": 1, "special_instructions": "Lime"}
            ],
            "order_status": "Ready for Pickup",
            "estimated_delivery": "7:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Carlos Garcia",
            "current_location": "Mexican Fiesta, 543 Oak St, Anytown, ST 12350",
            "current_coordinates": {"lat": "40.7110", "lng": "-74.0050"},
            "vehicle": "Hero Electric",
            "rating": "4.7"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Mexican Fiesta, 543 Oak St, Anytown, ST 12350",
            "pickup_coordinates": {"lat": "40.7110", "lng": "-74.0050"},
            "delivery_point": "334 River Rd, Anytown, ST 12351",
            "delivery_coordinates": {"lat": "40.7140", "lng": "-74.0090"},
            "estimated_distance": "3.6 km",
            "estimated_time": "24 minutes",
            "waypoints": [
                "Go west on Oak St",
                "Turn left onto River Rd",
                "Destination is on the right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123474",
            "customer_name": "Christopher Anderson",
            "driver_name": "Deepika Verma",
            "delivery_address": "445 Lake Ave, Anytown, ST 12352",
            "items": [
                {"name": "Burger", "quantity": 1, "special_instructions": "Bacon and cheese"},
                {"name": "Milkshake", "quantity": 1, "special_instructions": "Chocolate"}
            ],
            "order_status": "Out for Delivery",
            "estimated_delivery": "8:15 PM"
        },
        "RIDER_DETAILS": {
            "name": "Deepika Verma",
            "current_location": "Burger Joint, 400 Main St, Anytown, ST 12346",
            "current_coordinates": {"lat": "40.7160", "lng": "-74.0120"},
            "vehicle": "Suzuki Access",
            "rating": "4.5"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Burger Joint, 400 Main St, Anytown, ST 12346",
            "pickup_coordinates": {"lat": "40.7160", "lng": "-74.0120"},
            "delivery_point": "445 Lake Ave, Anytown, ST 12352",
            "delivery_coordinates": {"lat": "40.7115", "lng": "-74.0030"},
            "estimated_distance": "2.9 km",
            "estimated_time": "19 minutes",
            "waypoints": [
                "Head east on Main St",
                "Make a right onto Lake Ave",
                "Destination is on the left"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123475",
            "customer_name": "Angela Thompson",
            "driver_name": "Ethan Jones",
            "delivery_address": "556 Park Pl, Anytown, ST 12353",
            "items": [
                {"name": "Noodles", "quantity": 1, "special_instructions": "Spicy"},
                {"name": "Tea", "quantity": 1, "special_instructions": "Jasmine"}
            ],
            "order_status": "In Transit",
            "estimated_delivery": "8:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Ethan Jones",
            "current_location": "Thai Palace, 500 Elm St, Anytown, ST 12347",
            "current_coordinates": {"lat": "40.7140", "lng": "-74.0080"},
            "vehicle": "Yamaha Ray ZR",
            "rating": "4.8"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Thai Palace, 500 Elm St, Anytown, ST 12347",
            "pickup_coordinates": {"lat": "40.7140", "lng": "-74.0080"},
            "delivery_point": "556 Park Pl, Anytown, ST 12353",
            "delivery_coordinates": {"lat": "40.7135", "lng": "-74.0070"},
            "estimated_distance": "3.3 km",
            "estimated_time": "22 minutes",
            "waypoints": [
                "Go south on Elm St",
                "Take a left onto Park Pl",
                "Destination is on the right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123476",
            "customer_name": "Anthony Garcia",
            "driver_name": "Kiran Patel",
            "delivery_address": "667 School St, Anytown, ST 12354",
            "items": [
                {"name": "Smoothie", "quantity": 1, "special_instructions": "Berry mix"},
                {"name": "Wrap", "quantity": 1, "special_instructions": "Hummus"}
            ],
            "order_status": "Delivered",
            "estimated_delivery": "9:15 PM"
        },
        "RIDER_DETAILS": {
            "name": "Kiran Patel",
            "current_location": "Vegan Cafe, 600 Oak Ave, Anytown, ST 12345",
            "current_coordinates": {"lat": "40.7120", "lng": "-74.0050"},
            "vehicle": "Hero Maestro",
            "rating": "4.6"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Vegan Cafe, 600 Oak Ave, Anytown, ST 12345",
            "pickup_coordinates": {"lat": "40.7120", "lng": "-74.0050"},
            "delivery_point": "667 School St, Anytown, ST 12354",
            "delivery_coordinates": {"lat": "40.7105", "lng": "-74.0025"},
            "estimated_distance": "3.7 km",
            "estimated_time": "25 minutes",
            "waypoints": [
                "Drive west on Oak Ave",
                "Make a turn onto School St",
                "Destination is on the left"
            ]
        }
    },
     {
        "ORDER_DETAILS": {
            "order_id": "ORD123477",
            "customer_name": "Elizabeth Perez",
            "driver_name": "Leena Nair",
            "delivery_address": "778 Pine Ln, Anytown, ST 12355",
            "items": [
                {"name": "Sushi Roll", "quantity": 1, "special_instructions": "Avocado and cucumber"},
                {"name": "Miso Soup", "quantity": 1, "special_instructions": "Tofu"}
            ],
            "order_status": "Received",
            "estimated_delivery": "9:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Leena Nair",
            "current_location": "Restaurant ABC, 100 Pine Ave, Anytown, ST 12345",
            "current_coordinates": {"lat": "40.7110", "lng": "-74.0040"},
            "vehicle": "Suzuki Let's",
            "rating": "4.7"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Restaurant ABC, 100 Pine Ave, Anytown, ST 12345",
            "pickup_coordinates": {"lat": "40.7110", "lng": "-74.0040"},
            "delivery_point": "778 Pine Ln, Anytown, ST 12355",
            "delivery_coordinates": {"lat": "40.7140", "lng": "-74.0090"},
            "estimated_distance": "3.1 km",
            "estimated_time": "20 minutes",
            "waypoints": [
                "Travel south on Pine Ave",
                "Turn right onto Pine Ln",
                "Destination is on the right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123478",
            "customer_name": "Daniel White",
            "driver_name": "Muhammad Ali",
            "delivery_address": "889 Main St, Anytown, ST 12356",
            "items": [
                {"name": "Burger", "quantity": 1, "special_instructions": "Lettuce and tomato"},
                {"name": "Fries", "quantity": 1, "special_instructions": "Ketchup"}
            ],
            "order_status": "Preparing",
            "estimated_delivery": "10:15 PM"
        },
        "RIDER_DETAILS": {
            "name": "Muhammad Ali",
            "current_location": "Burger Joint, 400 Main St, Anytown, ST 12346",
            "current_coordinates": {"lat": "40.7160", "lng": "-74.0120"},
            "vehicle": "TVS Wego",
            "rating": "4.9"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Burger Joint, 400 Main St, Anytown, ST 12346",
            "pickup_coordinates": {"lat": "40.7160", "lng": "-74.0120"},
            "delivery_point": "889 Main St, Anytown, ST 12356",
            "delivery_coordinates": {"lat": "40.7115", "lng": "-74.0030"},
            "estimated_distance": "3.5 km",
            "estimated_time": "23 minutes",
            "waypoints": [
                "Head east on Main St",
                "Destination is on the right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123479",
            "customer_name": "Melissa King",
            "driver_name": "Olivia Green",
            "delivery_address": "990 Oak Ave, Anytown, ST 12357",
            "items": [
                {"name": "Pad Thai", "quantity": 1, "special_instructions": "No shrimp"},
                {"name": "Iced Coffee", "quantity": 1, "special_instructions": "Coconut milk"}
            ],
            "order_status": "Ready for Pickup",
            "estimated_delivery": "10:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Olivia Green",
            "current_location": "Thai Palace, 500 Elm St, Anytown, ST 12347",
            "current_coordinates": {"lat": "40.7140", "lng": "-74.0080"},
            "vehicle": "Honda Dio",
            "rating": "4.8"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Thai Palace, 500 Elm St, Anytown, ST 12347",
            "pickup_coordinates": {"lat": "40.7140", "lng": "-74.0080"},
            "delivery_point": "990 Oak Ave, Anytown, ST 12357",
            "delivery_coordinates": {"lat": "40.7135", "lng": "-74.0070"},
            "estimated_distance": "2.9 km",
            "estimated_time": "19 minutes",
            "waypoints": [
                "Go south on Elm St",
                "Turn left onto Oak Ave",
                "Destination is on the left"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123480",
            "customer_name": "Gary Hall",
            "driver_name": "Peter John",
            "delivery_address": "101 Elm St, Anytown, ST 12358",
            "items": [
                {"name": "Veggie Burger", "quantity": 1, "special_instructions": "Sprouts"},
                {"name": "Lemonade", "quantity": 1, "special_instructions": "No sugar"}
            ],
            "order_status": "Out for Delivery",
            "estimated_delivery": "11:15 PM"
        },
        "RIDER_DETAILS": {
            "name": "Peter John",
            "current_location": "Vegan Cafe, 600 Oak Ave, Anytown, ST 12345",
            "current_coordinates": {"lat": "40.7120", "lng": "-74.0050"},
            "vehicle": "Bajaj Chetak",
            "rating": "4.6"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Vegan Cafe, 600 Oak Ave, Anytown, ST 12345",
            "pickup_coordinates": {"lat": "40.7120", "lng": "-74.0050"},
            "delivery_point": "101 Elm St, Anytown, ST 12358",
            "delivery_coordinates": {"lat": "40.7105", "lng": "-74.0025"},
            "estimated_distance": "3.3 km",
            "estimated_time": "21 minutes",
            "waypoints": [
                "Drive west on Oak Ave",
                "Turn left onto Elm St",
                "Destination is on the right"
            ]
        }
    },
       {
        "ORDER_DETAILS": {
            "order_id": "ORD123481",
            "customer_name": "Helen Young",
            "driver_name": "Sunita Kumar",
            "delivery_address": "222 Cherry St, Anytown, ST 12359",
            "items": [
                {"name": "Sashimi", "quantity": 1, "special_instructions": "Tuna"},
                {"name": "Green Tea", "quantity": 1, "special_instructions": "Hot"}
            ],
            "order_status": "In Transit",
            "estimated_delivery": "11:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Sunita Kumar",
            "current_location": "700 Pine Ln, Anytown, ST 12346",
            "current_coordinates": {"lat": "40.7100", "lng": "-74.0020"},
            "vehicle": "Hero Electric",
            "rating": "4.7"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Restaurant ABC, 100 Pine Ave, Anytown, ST 12345",
            "pickup_coordinates": {"lat": "40.7110", "lng": "-74.0040"},
            "delivery_point": "222 Cherry St, Anytown, ST 12359",
            "delivery_coordinates": {"lat": "40.7140", "lng": "-74.0090"},
            "estimated_distance": "2.7 km",
            "estimated_time": "18 minutes",
            "waypoints": [
                "Continue on Pine Ave",
                "Turn right onto Cherry St",
                "Destination is on the left"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD123482",
            "customer_name": "Jack Hill",
            "driver_name": "Carlos Garcia",
            "delivery_address": "333 Pine Rd, Anytown, ST 12360",
            "items": [
                {"name": "Pizza", "quantity": 1, "special_instructions": "Extra pepperoni"},
                {"name": "Soda", "quantity": 1, "special_instructions": "Orange"}
            ],
            "order_status": "Delivered",
            "estimated_delivery": "12:15 AM"
        },
        "RIDER_DETAILS": {
            "name": "Carlos Garcia",
            "current_location": "200 Elm St, Anytown, ST 12347",
            "current_coordinates": {"lat": "40.7145", "lng": "-74.0085"},
            "vehicle": "Suzuki Let's",
            "rating": "4.9"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Restaurant XYZ, 200 Elm St, Anytown, ST 12346",
            "pickup_coordinates": {"lat": "40.7145", "lng": "-74.0100"},
            "delivery_point": "333 Pine Rd, Anytown, ST 12360",
            "delivery_coordinates": {"lat": "40.7110", "lng": "-74.0020"},
            "estimated_distance": "3.1 km",
            "estimated_time": "20 minutes",
            "waypoints": [
                "Travel south on Elm St",
                "Turn left onto Pine Rd",
                "Destination is on the right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100008",
            "customer_name": "David Rodriguez",
            "driver_name": "Kunal",
            "delivery_address": "123 Main St, Anytown, ST 12345",
            "items": [
                {
                    "name": "Chicken Burger",
                    "quantity": 1,
                    "special_instructions": "No Mayo"
                },
                {
                    "name": "French Fries",
                    "quantity": 1,
                    "special_instructions": "Extra Salt"
                }
            ],
            "order_status": "Delivered",
            "estimated_delivery": "3:30 PM"
        },
        "RIDER_DETAILS": {
            "name": "Kunal",
            "current_location": "234 Pine St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7142",
                "lng": "-74.0069"
            },
            "vehicle": "Suzuki Access",
            "rating": "4.6"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Burger Joint, 345 Oak Avenue, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7119",
                "lng": "-74.0027"
            },
            "delivery_point": "123 Main St, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7157",
                "lng": "-74.0085"
            },
            "estimated_distance": "3.2 km",
            "estimated_time": "24 minutes",
            "waypoints": [
                "Continue on Main St",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100009",
            "customer_name": "Ashley Wilson",
            "driver_name": "Rajiv",
            "delivery_address": "456 Elm St, Anytown, ST 12345",
            "items": [
                {
                    "name": "Veg Pizza",
                    "quantity": 1,
                    "special_instructions": "Extra Cheese"
                },
                {
                    "name": "Soda",
                    "quantity": 2,
                    "special_instructions": "Chilled"
                }
            ],
            "order_status": "In Transit",
            "estimated_delivery": "10:15 AM"
        },
        "RIDER_DETAILS": {
            "name": "Rajiv",
            "current_location": "567 Cedar Lane, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7131",
                "lng": "-74.0051"
            },
            "vehicle": "Yamaha Scooter",
            "rating": "4.7"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Pizzeria ABC, 678 Willow Road, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7108",
                "lng": "-74.0093"
            },
            "delivery_point": "456 Elm St, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7169",
                "lng": "-74.0018"
            },
            "estimated_distance": "4.0 km",
            "estimated_time": "27 minutes",
            "waypoints": [
                "Turn left onto Oak Avenue",
                "Continue on Elm St",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100010",
            "customer_name": "Christopher Garcia",
            "driver_name": "Navjyot",
            "delivery_address": "789 Birch Street, Anytown, ST 12345",
            "items": [
                {
                    "name": "Sushi Roll",
                    "quantity": 1,
                    "special_instructions": "No Wasabi"
                },
                {
                    "name": "Sake",
                    "quantity": 1,
                    "special_instructions": "Cold"
                }
            ],
            "order_status": "Pending",
            "estimated_delivery": "4:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Navjyot",
            "current_location": "890 Main St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7155",
                "lng": "-74.0076"
            },
            "vehicle": "Vespa",
            "rating": "4.8"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Sushi House, 901 Maple Street, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7124",
                "lng": "-74.0034"
            },
            "delivery_point": "789 Birch Street, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7147",
                "lng": "-74.0092"
            },
            "estimated_distance": "3.5 km",
            "estimated_time": "25 minutes",
            "waypoints": [
                "Continue on Birch Street",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100011",
            "customer_name": "Brittany Martinez",
            "driver_name": "Priya",
            "delivery_address": "101 Oak Avenue, Anytown, ST 12345",
            "items": [
                {
                    "name": "Tacos",
                    "quantity": 2,
                    "special_instructions": "Hot Sauce"
                },
                {
                    "name": "Coke",
                    "quantity": 1,
                    "special_instructions": "Ice"
                }
            ],
            "order_status": "Delivered",
            "estimated_delivery": "6:00 PM"
        },
        "RIDER_DETAILS": {
            "name": "Priya",
            "current_location": "222 Elm St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7136",
                "lng": "-74.0058"
            },
            "vehicle": "E-Bike",
            "rating": "4.9"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Taco Time, 333 Cedar Lane, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7113",
                "lng": "-74.0081"
            },
            "delivery_point": "101 Oak Avenue, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7151",
                "lng": "-74.0025"
            },
            "estimated_distance": "3.7 km",
            "estimated_time": "26 minutes",
            "waypoints": [
                "Turn left onto Oak Avenue",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100012",
            "customer_name": "Kevin Anderson",
            "driver_name": "Amit",
            "delivery_address": "444 Pine St, Anytown, ST 12345",
            "items": [
                {
                    "name": "Pad Thai",
                    "quantity": 1,
                    "special_instructions": "Extra Peanuts"
                },
                {
                    "name": "Thai Iced Tea",
                    "quantity": 1,
                    "special_instructions": "Sweet"
                }
            ],
            "order_status": "In Transit",
            "estimated_delivery": "11:30 AM"
        },
        "RIDER_DETAILS": {
            "name": "Amit",
            "current_location": "555 Willow Road, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7127",
                "lng": "-74.0049"
            },
            "vehicle": "Honda Activa",
            "rating": "4.5"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Restaurant XYZ, 666 Birch Street, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7144",
                "lng": "-74.0017"
            },
            "delivery_point": "444 Pine St, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7162",
                "lng": "-74.0084"
            },
            "estimated_distance": "4.2 km",
            "estimated_time": "28 minutes",
            "waypoints": [
                "Turn right onto Maple Street",
                "Turn left onto Pine St",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100013",
            "customer_name": "Amanda Thomas",
            "driver_name": "Sneha",
            "delivery_address": "777 Maple Street, Anytown, ST 12345",
            "items": [
                {
                    "name": "Ramen",
                    "quantity": 1,
                    "special_instructions": "Soft Boiled Egg"
                },
                {
                    "name": "Green Tea",
                    "quantity": 1,
                    "special_instructions": None
                }
            ],
            "order_status": "Pending",
            "estimated_delivery": "7:15 PM"
        },
        "RIDER_DETAILS": {
            "name": "Sneha",
            "current_location": "888 Main St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7106",
                "lng": "-74.0035"
            },
            "vehicle": "Suzuki Access",
            "rating": "4.8"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Sushi House, 999 Elm St, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7129",
                "lng": "-74.0096"
            },
            "delivery_point": "777 Maple Street, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7148",
                "lng": "-74.0019"
            },
            "estimated_distance": "3.9 km",
            "estimated_time": "27 minutes",
            "waypoints": [
                "Turn left onto Oak Avenue",
                "Continue on Maple Street",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100014",
            "customer_name": "Ryan White",
            "driver_name": "Vikram",
            "delivery_address": "111 Willow Road, Anytown, ST 12345",
            "items": [
                {
                    "name": "Burrito",
                    "quantity": 1,
                    "special_instructions": "No Beans"
                },
                {
                    "name": "Horchata",
                    "quantity": 1,
                    "special_instructions": "Less Sugar"
                }
            ],
            "order_status": "Delivered",
            "estimated_delivery": "1:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Vikram",
            "current_location": "222 Birch Street, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7141",
                "lng": "-74.0071"
            },
            "vehicle": "Yamaha Scooter",
            "rating": "4.7"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Taco Time, 333 Oak Avenue, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7117",
                "lng": "-74.0029"
            },
            "delivery_point": "111 Willow Road, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7165",
                "lng": "-74.0098"
            },
            "estimated_distance": "4.4 km",
            "estimated_time": "29 minutes",
            "waypoints": [
                "Turn right onto Maple Street",
                "Turn left onto Willow Road",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100015",
            "customer_name": "Stephanie Hall",
            "driver_name": "Deepika",
            "delivery_address": "444 Cedar Lane, Anytown, ST 12345",
            "items": [
                {
                    "name": "Chicken Curry",
                    "quantity": 1,
                    "special_instructions": "Medium Spicy"
                },
                {
                    "name": "Naan",
                    "quantity": 2,
                    "special_instructions": None
                }
            ],
            "order_status": "In Transit",
            "estimated_delivery": "8:30 PM"
        },
        "RIDER_DETAILS": {
            "name": "Deepika",
            "current_location": "555 Pine St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7133",
                "lng": "-74.0053"
            },
            "vehicle": "Vespa",
            "rating": "4.6"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Restaurant XYZ, 666 Maple Street, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7110",
                "lng": "-74.0095"
            },
            "delivery_point": "444 Cedar Lane, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7159",
                "lng": "-74.0016"
            },
            "estimated_distance": "4.1 km",
            "estimated_time": "28 minutes",
            "waypoints": [
                "Turn left onto Oak Avenue",
                "Continue on Cedar Lane",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100016",
            "customer_name": "Nicholas Turner",
            "driver_name": "Rohan",
            "delivery_address": "777 Main St, Anytown, ST 12345",
            "items": [
                {
                    "name": "Pizza",
                    "quantity": 1,
                    "special_instructions": "No Olives"
                },
                {
                    "name": "Lemonade",
                    "quantity": 1,
                    "special_instructions": "Extra Lemon"
                }
            ],
            "order_status": "Pending",
            "estimated_delivery": "2:00 PM"
        },
        "RIDER_DETAILS": {
            "name": "Rohan",
            "current_location": "888 Elm St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7121",
                "lng": "-74.0041"
            },
            "vehicle": "E-Bike",
            "rating": "4.9"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Pizzeria ABC, 999 Birch Street, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7139",
                "lng": "-74.0079"
            },
            "delivery_point": "777 Main St, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7167",
                "lng": "-74.0022"
            },
            "estimated_distance": "3.6 km",
            "estimated_time": "25 minutes",
            "waypoints": [
                "Turn right onto Willow Road",
                "Continue on Main St",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100017",
            "customer_name": "Angela Baker",
            "driver_name": "Anjali",
            "delivery_address": "901 Birch Street, Anytown, ST 12345",
            "items": [
                {
                    "name": "Tacos",
                    "quantity": 3,
                    "special_instructions": "Mild Sauce"
                },
                {
                    "name": "Horchata",
                    "quantity": 1,
                    "special_instructions": None
                }
            ],
            "order_status": "Delivered",
            "estimated_delivery": "9:15 AM"
        },
        "RIDER_DETAILS": {
            "name": "Anjali",
            "current_location": "123 Pine St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7107",
                "lng": "-74.0037"
            },
            "vehicle": "Honda Activa",
            "rating": "4.5"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Taco Time, 234 Maple Street, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7135",
                "lng": "-74.0063"
            },
            "delivery_point": "901 Birch Street, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7153",
                "lng": "-74.0089"
            },
            "estimated_distance": "3.3 km",
            "estimated_time": "24 minutes",
            "waypoints": [
                "Turn left onto Oak Avenue",
                "Continue on Birch Street",
                "Destination will be on your left/right"
            ]
        }
    },
        {
        "ORDER_DETAILS": {
            "order_id": "ORD100018",
            "customer_name": "Brandon King",
            "driver_name": "Kunal",
            "delivery_address": "124 Main St, Anytown, ST 12345",
            "items": [
                {
                    "name": "Chicken Burger",
                    "quantity": 1,
                    "special_instructions": "No Lettuce"
                },
                {
                    "name": "Fries",
                    "quantity": 1,
                    "special_instructions": "Extra Ketchup"
                }
            ],
            "order_status": "In Transit",
            "estimated_delivery": "3:45 PM"
        },
        "RIDER_DETAILS": {
            "name": "Kunal",
            "current_location": "235 Pine St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7143",
                "lng": "-74.0070"
            },
            "vehicle": "Suzuki Access",
            "rating": "4.6"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Burger Joint, 346 Oak Avenue, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7120",
                "lng": "-74.0028"
            },
            "delivery_point": "124 Main St, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7158",
                "lng": "-74.0086"
            },
            "estimated_distance": "3.3 km",
            "estimated_time": "25 minutes",
            "waypoints": [
                "Continue on Main St",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100019",
            "customer_name": "Isabella Lewis",
            "driver_name": "Rajiv",
            "delivery_address": "457 Elm St, Anytown, ST 12345",
            "items": [
                {
                    "name": "Veg Pizza",
                    "quantity": 1,
                    "special_instructions": "No Mushrooms"
                },
                {
                    "name": "Soda",
                    "quantity": 2,
                    "special_instructions": "Chilled"
                }
            ],
            "order_status": "Pending",
            "estimated_delivery": "10:30 AM"
        },
        "RIDER_DETAILS": {
            "name": "Rajiv",
            "current_location": "568 Cedar Lane, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7132",
                "lng": "-74.0052"
            },
            "vehicle": "Yamaha Scooter",
            "rating": "4.7"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Pizzeria ABC, 679 Willow Road, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7109",
                "lng": "-74.0094"
            },
            "delivery_point": "457 Elm St, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7170",
                "lng": "-74.0019"
            },
            "estimated_distance": "4.1 km",
            "estimated_time": "28 minutes",
            "waypoints": [
                "Turn left onto Oak Avenue",
                "Continue on Elm St",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100020",
            "customer_name": "Jonathan Lee",
            "driver_name": "Navjyot",
            "delivery_address": "790 Birch Street, Anytown, ST 12345",
            "items": [
                {
                    "name": "Sushi Roll",
                    "quantity": 1,
                    "special_instructions": "No Ginger"
                },
                {
                    "name": "Sake",
                    "quantity": 1,
                    "special_instructions": "Cold"
                }
            ],
            "order_status": "Delivered",
            "estimated_delivery": "4:50 PM"
        },
        "RIDER_DETAILS": {
            "name": "Navjyot",
            "current_location": "891 Main St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7156",
                "lng": "-74.0077"
            },
            "vehicle": "Vespa",
            "rating": "4.8"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Sushi House, 902 Maple Street, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7125",
                "lng": "-74.0035"
            },
            "delivery_point": "790 Birch Street, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7148",
                "lng": "-74.0093"
            },
            "estimated_distance": "3.6 km",
            "estimated_time": "26 minutes",
            "waypoints": [
                "Continue on Birch Street",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100021",
            "customer_name": "Samantha Hill",
            "driver_name": "Priya",
            "delivery_address": "102 Oak Avenue, Anytown, ST 12345",
            "items": [
                {
                    "name": "Tacos",
                    "quantity": 2,
                    "special_instructions": "Hot Sauce"
                },
                {
                    "name": "Coke",
                    "quantity": 1,
                    "special_instructions": "Ice"
                }
            ],
            "order_status": "In Transit",
            "estimated_delivery": "6:10 PM"
        },
        "RIDER_DETAILS": {
            "name": "Priya",
            "current_location": "223 Elm St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7137",
                "lng": "-74.0059"
            },
            "vehicle": "E-Bike",
            "rating": "4.9"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Taco Time, 334 Cedar Lane, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7114",
                "lng": "-74.0082"
            },
            "delivery_point": "102 Oak Avenue, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7152",
                "lng": "-74.0026"
            },
            "estimated_distance": "3.8 km",
            "estimated_time": "27 minutes",
            "waypoints": [
                "Turn left onto Oak Avenue",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100022",
            "customer_name": "Joshua Wright",
            "driver_name": "Amit",
            "delivery_address": "445 Pine St, Anytown, ST 12345",
            "items": [
                {
                    "name": "Pad Thai",
                    "quantity": 1,
                    "special_instructions": "Extra Peanuts"
                },
                {
                    "name": "Thai Iced Tea",
                    "quantity": 1,
                    "special_instructions": "Sweet"
                }
            ],
            "order_status": "Pending",
            "estimated_delivery": "11:45 AM"
        },
        "RIDER_DETAILS": {
            "name": "Amit",
            "current_location": "556 Willow Road, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7128",
                "lng": "-74.0050"
            },
            "vehicle": "Honda Activa",
            "rating": "4.5"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Restaurant XYZ, 667 Birch Street, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7145",
                "lng": "-74.0018"
            },
            "delivery_point": "445 Pine St, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7163",
                "lng": "-74.0085"
            },
            "estimated_distance": "4.3 km",
            "estimated_time": "29 minutes",
            "waypoints": [
                "Turn right onto Maple Street",
                "Turn left onto Pine St",
                "Destination will be on your left/right"
            ]
        }
    },
    {
        "ORDER_DETAILS": {
            "order_id": "ORD100023",
            "customer_name": "Madison Green",
            "driver_name": "Sneha",
            "delivery_address": "778 Maple Street, Anytown, ST 12345",
            "items": [
                {
                    "name": "Ramen",
                    "quantity": 1,
                    "special_instructions": "Soft Boiled Egg"
                },
                {
                    "name": "Green Tea",
                    "quantity": 1,
                    "special_instructions": None
                }
            ],
            "order_status": "Delivered",
            "estimated_delivery": "7:30 PM"
        },
        "RIDER_DETAILS": {
            "name": "Sneha",
            "current_location": "889 Main St, Anytown, ST 12345",
            "current_coordinates": {
                "lat": "40.7107",
                "lng": "-74.0036"
            },
            "vehicle": "Suzuki Access",
            "rating": "4.8"
        },
        "ROUTE_DETAILS": {
            "pickup_point": "Sushi House, 900 Elm St, Anytown, ST 12345",
            "pickup_coordinates": {
                "lat": "40.7130",
                "lng": "-74.0097"
            },
            "delivery_point": "778 Maple Street, Anytown, ST 12345",
            "delivery_coordinates": {
                "lat": "40.7149",
                "lng": "-74.0020"
            },
            "estimated_distance": "4.0 km",
            "estimated_time": "28 minutes",
            "waypoints": [
                "Turn left onto Oak Avenue",
                "Continue on Maple Street",
                "Destination will be on your left/right"
            ]
        }
    }
]


# Sample item prices
item_prices = {
    "Chicken Burger": 5.99,
    "French Fries": 2.99,
    "Fries":2.99,
    "Veg Pizza": 4.99,
    "Coke": 1.99,
    "Pasta Alfredo": 3.99,
    "Garlic Bread": 2.99,
    "Samosas": 2.50,
    "Mango Lassi": 3.50,
    "Burrito": 7.50,
    "Guacamole": 4.00,
    "Sushi Platter": 15.00,
    "Miso Soup": 4.50,
    "Pizza": 12.00,
    "Tacos": 3.00,
    "Horchata": 3.00,
    "Ramen": 10.00,
    "Green Tea": 2.75,
    "Chicken Curry": 9.50,
    "Naan": 2.00,
    "Cheeseburger": 6.50,
    "Pad Thai": 11.00,
    "Thai Iced Tea": 4.00,
    "Tofu Scramble": 8.00,
    "Soy Latte": 4.50,
    "Sake": 7.00,
    "Lemonade": 2.50,
    "Pasta": 9.00,
    "Breadsticks": 3.50,
    "Curry": 8.50,
    "Rice": 3.00,
    "Enchiladas": 8.00,
    "Soda": 2.00,
    "Burger": 7.00,
    "Milkshake": 5.00,
    "Noodles": 9.50,
    "Tea": 3.00,
    "Smoothie": 6.00,
    "Wrap": 7.50,
    "Sushi Roll": 6.50,
    "Sashimi": 18.00,
    "Veggie Burger": 6.00,
    "Iced Coffee": 4.00
}
# Connect to SQLite database
conn = sqlite3.connect("delivery.db")
cursor = conn.cursor()

# Create tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS order_details (
    order_id TEXT PRIMARY KEY,
    customer_name TEXT,
    driver_name TEXT,
    delivery_address TEXT,
    order_status TEXT,
    estimated_delivery TEXT,
    restaurant_name TEXT DEFAULT 'George',
    order_price REAL
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,
    item_name TEXT,
    quantity INTEGER,
    special_instructions TEXT,
    item_price REAL,
    FOREIGN KEY(order_id) REFERENCES order_details(order_id)
);

CREATE TABLE IF NOT EXISTS rider_details (
    name TEXT,
    current_location TEXT,
    lat TEXT,
    lng TEXT,
    vehicle TEXT,
    rating TEXT
);

CREATE TABLE IF NOT EXISTS route_details (
    order_id TEXT,
    pickup_point TEXT,
    pickup_lat TEXT,
    pickup_lng TEXT,
    delivery_point TEXT,
    delivery_lat TEXT,
    delivery_lng TEXT,
    estimated_distance TEXT,
    estimated_time TEXT,
    FOREIGN KEY(order_id) REFERENCES order_details(order_id)
);

CREATE TABLE IF NOT EXISTS waypoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,
    waypoint TEXT,
    FOREIGN KEY(order_id) REFERENCES order_details(order_id)
);
""")

# Insert data
for data in entry:
    order = data["ORDER_DETAILS"]
    rider = data["RIDER_DETAILS"]
    route = data["ROUTE_DETAILS"]

    # Calculate order price
    order_price = sum(item_prices[item["name"]] * item["quantity"] for item in order["items"])

    # Insert into order_details
    cursor.execute("""
    INSERT INTO order_details (order_id, customer_name, driver_name, delivery_address, order_status, estimated_delivery, order_price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order["order_id"], order["customer_name"], order["driver_name"], order["delivery_address"], order["order_status"], order["estimated_delivery"], order_price))

    # Insert into order_items
    for item in order["items"]:
        cursor.execute("""
        INSERT INTO order_items (order_id, item_name, quantity, special_instructions, item_price)
        VALUES (?, ?, ?, ?, ?)
        """, (order["order_id"], item["name"], item["quantity"], item["special_instructions"], item_prices[item["name"]]))

    # Insert into rider_details
    cursor.execute("""
    INSERT INTO rider_details (name, current_location, lat, lng, vehicle, rating)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (rider["name"], rider["current_location"], rider["current_coordinates"]["lat"], rider["current_coordinates"]["lng"], rider["vehicle"], rider["rating"]))

    # Insert into route_details
    cursor.execute("""
    INSERT INTO route_details (order_id, pickup_point, pickup_lat, pickup_lng, delivery_point, delivery_lat, delivery_lng, estimated_distance, estimated_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (order["order_id"], route["pickup_point"], route["pickup_coordinates"]["lat"], route["pickup_coordinates"]["lng"], route["delivery_point"], route["delivery_coordinates"]["lat"], route["delivery_coordinates"]["lng"], route["estimated_distance"], route["estimated_time"]))

    # Insert into waypoints
    for waypoint in route["waypoints"]:
        cursor.execute("""
        INSERT INTO waypoints (order_id, waypoint)
        VALUES (?, ?)
        """, (order["order_id"], waypoint))

# Commit and close
conn.commit()
conn.close()
print("✅ All tables populated successfully!")