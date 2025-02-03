from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import json
import os
from typing import Dict, List

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

class WasteCategory:
    ORGANIC = "Organic"
    RECYCLABLE = "Recyclable"
    HAZARDOUS = "Hazardous"
    GENERAL = "General"

    @staticmethod
    def get_all():
        return [WasteCategory.ORGANIC, WasteCategory.RECYCLABLE, 
                WasteCategory.HAZARDOUS, WasteCategory.GENERAL]

class WasteEntry:
    def __init__(self, category: str, weight: float, description: str):
        self.category = category
        self.weight = weight
        self.description = description
        self.date = datetime.now()

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "weight": self.weight,
            "description": self.description,
            "date": self.date.isoformat()
        }

class WasteManagementSystem:
    def __init__(self):
        self.waste_entries: List[WasteEntry] = []
        self.tips = {
            WasteCategory.ORGANIC: [
                "Start composting kitchen waste",
                "Plan meals to reduce food waste",
                "Store food properly to extend shelf life"
            ],
            WasteCategory.RECYCLABLE: [
                "Rinse containers before recycling",
                "Flatten cardboard boxes",
                "Check local recycling guidelines"
            ],
            WasteCategory.HAZARDOUS: [
                "Use eco-friendly alternatives",
                "Dispose at designated facilities",
                "Never mix different chemicals"
            ],
            WasteCategory.GENERAL: [
                "Use reusable bags and containers",
                "Avoid single-use items",
                "Buy products with less packaging"
            ]
        }
        self.load_data()

    def add_waste_entry(self, category: str, weight: float, description: str) -> None:
        entry = WasteEntry(category, weight, description)
        self.waste_entries.append(entry)
        self.save_data()

    def get_statistics(self) -> Dict[str, float]:
        stats = {cat: 0.0 for cat in WasteCategory.get_all()}
        for entry in self.waste_entries:
            stats[entry.category] += entry.weight
        return stats

    def get_tips(self, category: str) -> List[str]:
        return self.tips.get(category, [])

    def save_data(self) -> None:
        data = {
            "entries": [entry.to_dict() for entry in self.waste_entries]
        }
        with open("waste_data.json", "w") as f:
            json.dump(data, f, indent=2)

    def load_data(self) -> None:
        if not os.path.exists("waste_data.json"):
            return
        try:
            with open("waste_data.json", "r") as f:
                data = json.load(f)
                for entry_data in data["entries"]:
                    entry = WasteEntry(
                        entry_data["category"],
                        entry_data["weight"],
                        entry_data["description"]
                    )
                    entry.date = datetime.fromisoformat(entry_data["date"])
                    self.waste_entries.append(entry)
        except Exception as e:
            print(f"Error loading data: {e}")

    def get_sorted_entries(self):
        return sorted(self.waste_entries, key=lambda x: x.date, reverse=True)

# Initialize the waste management system
system = WasteManagementSystem()

@app.route('/')
def index():
    stats = system.get_statistics()
    total = sum(stats.values())
    return render_template('index.html', 
                         stats=stats, 
                         total=total)

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        try:
            category = request.form['category']
            weight = float(request.form['weight'])
            if weight <= 0:
                raise ValueError("Weight must be positive")
            description = request.form['description']
            
            system.add_waste_entry(category, weight, description)
            flash('Waste entry added successfully!', 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'error')
    
    return render_template('add_entry.html', categories=WasteCategory.get_all())

@app.route('/tips/<category>')
def tips(category):
    if category not in WasteCategory.get_all():
        flash('Invalid category!', 'error')
        return redirect(url_for('index'))
    tips_list = system.get_tips(category)
    return render_template('tips.html', category=category, tips=tips_list)

@app.route('/entries')
def entries():
    sorted_entries = system.get_sorted_entries()
    return render_template('entries.html', entries=sorted_entries)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)