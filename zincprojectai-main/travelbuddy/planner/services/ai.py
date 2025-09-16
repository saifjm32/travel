from __future__ import annotations

import json
import os
from typing import Dict, Any


def _stub_itinerary(trip) -> Dict[str, Any]:
    num_days = (trip.end_date - trip.start_date).days + 1
    days = []
    for i in range(num_days):
        day_num = i + 1
        days.append({
            "day": day_num,
            "items": [
                {"time": "morning", "place": f"Top spot {day_num}", "note": "Coffee and walk"},
                {"time": "afternoon", "place": f"Museum {day_num}", "note": "Culture time"},
                {"time": "evening", "place": f"Local eats {day_num}", "note": "Dinner"},
            ]
        })
    return {
        "destination": trip.destination,
        "days": days,
        "tips": [
            "Book attractions early.",
            "Use public transit passes for savings.",
        ],
    }


def generate_itinerary(trip) -> Dict[str, Any]:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return _stub_itinerary(trip)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = (
            "Generate a concise JSON itinerary for a trip. Schema: "
            "{destination: string, days: [{day: number, items: [{time: string, place: string, note: string}]}], tips: string[]}"
            f". Origin: {trip.origin}. Destination: {trip.destination}. Dates: {trip.start_date} to {trip.end_date}. "
            f"Budget: {trip.budget_amount or ''} {trip.budget_currency or ''}. Transport: {trip.transport_prefs or ''}. "
            f"Taxi airport->hotel: {trip.taxi_airport_to_hotel}. Travelers: "
            + ", ".join([f"{t.age}/{t.gender}" for t in trip.travelers.all()])
            + ". Return ONLY JSON."
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You return only valid minified JSON for itineraries."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        text = resp.choices[0].message.content.strip()
        try:
            data = json.loads(text)
        except Exception:
            # try to extract JSON substring
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1 and end > start:
                data = json.loads(text[start:end + 1])
            else:
                data = _stub_itinerary(trip)
        return data
    except Exception:
        return _stub_itinerary(trip)


