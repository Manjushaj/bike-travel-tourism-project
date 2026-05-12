from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'bikeroute_secret_2026'

# Sample data
ROUTES = [
    {
        "id": 1,
        "name": "Ooty → Kodaikanal",
        "state": "Tamil Nadu",
        "date": "Apr 18, 2025",
        "duration": "3 days",
        "type": "Solo",
        "level": "Beginner",
        "spots": 8,
        "price": 4200,
        "guide": "Ravi Kumar",
        "guide_rating": 4.9,
        "guide_rides": 120,
        "guide_cert": ["Mechanic certified", "First-aid trained"],
        "color": "#1a3a2a",
        "includes": ["Guide with full tool kit", "Puncture & chain repair", "Emergency contact service"],
        "itinerary": [
            {"day": 1, "title": "Ooty to Kothagiri", "desc": "Scenic climb through tea gardens, 45km, mild elevation gain."},
            {"day": 2, "title": "Kothagiri to Kodaikanal", "desc": "Technical descent, forest trail, 60km. Guide carries spare tubes."},
            {"day": 3, "title": "Kodaikanal Exploration", "desc": "Leisure ride around the lake. Optional group photo stop."}
        ]
    },
    {
        "id": 2,
        "name": "Chennai Coastal Loop",
        "state": "ECR Route",
        "date": "Apr 22, 2025",
        "duration": "1 day",
        "type": "Group",
        "level": "Beginner",
        "spots": 6,
        "price": 1800,
        "guide": "Suresh Pillai",
        "guide_rating": 4.8,
        "guide_rides": 97,
        "guide_cert": ["First-aid trained"],
        "color": "#0d2233",
        "includes": ["Guide with full tool kit", "Puncture repair", "Emergency contact"],
        "itinerary": [
            {"day": 1, "title": "Marina to Mahabalipuram", "desc": "Coastal highway ride, 60km, flat terrain. Sunrise start."}
        ]
    },
    {
        "id": 3,
        "name": "Munnar High Altitude",
        "state": "Kerala",
        "date": "May 3, 2025",
        "duration": "6 days",
        "type": "Solo",
        "level": "Advanced",
        "spots": 4,
        "price": 9500,
        "guide": "Arjun Menon",
        "guide_rating": 5.0,
        "guide_rides": 203,
        "guide_cert": ["Altitude specialist", "Mechanic certified", "First-aid trained"],
        "color": "#2d1a0a",
        "includes": ["Guide with full tool kit", "Puncture & chain repair", "Emergency contact service", "Altitude support"],
        "itinerary": [
            {"day": 1, "title": "Kochi to Munnar Base", "desc": "Ghat roads climb, 120km, moderate difficulty."},
            {"day": 2, "title": "Munnar Tea Estates Loop", "desc": "45km loop through highest tea gardens in India."},
            {"day": 3, "title": "Top Station Challenge", "desc": "60km hard climb to 2100m elevation. Guide support essential."},
            {"day": 4, "title": "Eravikulam Descent", "desc": "Thrilling 80km descent through national park."},
            {"day": 5, "title": "Mattupetty Dam Circuit", "desc": "40km easy day with scenic lake views."},
            {"day": 6, "title": "Return Kochi", "desc": "Final 120km descent to sea level."}
        ]
    },
    {
        "id": 4,
        "name": "Hampi Heritage Ride",
        "state": "Karnataka",
        "date": "May 10, 2025",
        "duration": "2 days",
        "type": "Group",
        "level": "Beginner",
        "spots": 10,
        "price": 3200,
        "guide": "Kiran Reddy",
        "guide_rating": 4.7,
        "guide_rides": 85,
        "guide_cert": ["Mechanic certified"],
        "color": "#2a1a00",
        "includes": ["Guide with full tool kit", "Puncture repair", "Emergency contact"],
        "itinerary": [
            {"day": 1, "title": "Hospet to Hampi", "desc": "35km flat ride through boulder landscapes."},
            {"day": 2, "title": "Hampi Temple Circuit", "desc": "30km exploring ancient ruins on bike."}
        ]
    },
    {
        "id": 5,
        "name": "Coorg Coffee Trail",
        "state": "Karnataka",
        "date": "May 18, 2025",
        "duration": "4 days",
        "type": "Solo",
        "level": "Intermediate",
        "spots": 5,
        "price": 6800,
        "guide": "Priya Nair",
        "guide_rating": 4.9,
        "guide_rides": 156,
        "guide_cert": ["Mechanic certified", "First-aid trained", "Nature guide"],
        "color": "#0a2a1a",
        "includes": ["Guide with full tool kit", "Puncture & chain repair", "Emergency contact service", "Coffee estate entry"],
        "itinerary": [
            {"day": 1, "title": "Madikeri Entry", "desc": "Arrival and 25km warm-up through mist."},
            {"day": 2, "title": "Estate Loops", "desc": "Coffee and cardamom plantation trails, 55km."},
            {"day": 3, "title": "Iruppu Falls Route", "desc": "Forest trail to waterfall, 40km."},
            {"day": 4, "title": "Brahmagiri Hills", "desc": "Summit attempt, 50km hard climb."}
        ]
    },
    {
        "id": 6,
        "name": "Rajasthan Desert Ride",
        "state": "Rajasthan",
        "date": "Nov 5, 2025",
        "duration": "7 days",
        "type": "Group",
        "level": "Advanced",
        "spots": 6,
        "price": 14500,
        "guide": "Vikram Singh",
        "guide_rating": 5.0,
        "guide_rides": 310,
        "guide_cert": ["Mechanic certified", "First-aid trained", "Desert navigation"],
        "color": "#2a1500",
        "includes": ["Guide with full tool kit", "Full mechanical support", "Emergency contact service", "Desert camp stays"],
        "itinerary": [
            {"day": 1, "title": "Jaipur to Ajmer", "desc": "90km highway ride through pink city outskirts."},
            {"day": 2, "title": "Ajmer to Pushkar", "desc": "Short 15km leg, explore lake town."},
            {"day": 3, "title": "Pushkar to Jodhpur", "desc": "180km through Thar desert edge."},
            {"day": 4, "title": "Jodhpur Blue City Loop", "desc": "City exploration by bike, 40km."},
            {"day": 5, "title": "Jodhpur to Jaisalmer", "desc": "290km desert highway, iconic golden hour."},
            {"day": 6, "title": "Sam Sand Dunes Circuit", "desc": "Off-road desert trail, 60km."},
            {"day": 7, "title": "Return Jodhpur", "desc": "Final 290km return leg."}
        ]
    }
]

BOOKINGS = []

@app.route('/')
def home():
    return render_template('index.html', routes=ROUTES)

@app.route('/trip/<int:trip_id>')
def trip_detail(trip_id):
    trip = next((r for r in ROUTES if r['id'] == trip_id), None)
    if not trip:
        return redirect(url_for('home'))
    return render_template('trip_detail.html', trip=trip)

@app.route('/book/<int:trip_id>', methods=['POST'])
def book(trip_id):
    trip = next((r for r in ROUTES if r['id'] == trip_id), None)
    if not trip:
        return jsonify({'success': False})
    
    data = request.form
    riders = int(data.get('riders', 1))
    booking = {
        'id': f'BK{random.randint(10000, 99999)}',
        'trip': trip['name'],
        'name': data.get('name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'riders': riders,
        'total': trip['price'] * riders + int(trip['price'] * riders * 0.05),
        'guide': trip['guide'],
        'date': trip['date']
    }
    BOOKINGS.append(booking)
    return render_template('confirmation.html', booking=booking, trip=trip)

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/search')
def search():
    q = request.args.get('q', '').lower()
    level = request.args.get('level', '')
    rtype = request.args.get('type', '')
    results = ROUTES
    if q:
        results = [r for r in results if q in r['name'].lower() or q in r['state'].lower()]
    if level:
        results = [r for r in results if r['level'] == level]
    if rtype:
        results = [r for r in results if r['type'] == rtype]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
