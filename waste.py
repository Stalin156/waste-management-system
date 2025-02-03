import datetime
import json
import os
from typing import Dict, List, Optional

class WasteCategory:
    ORGANIC = "Organic"
    RECYCLABLE = "Recyclable"
    HAZARDOUS = "Hazardous"
    GENERAL = "General"

class WasteEntry:
    def __init__(self, category: str, weight: float, description: str):
        self.category = category
        self.weight = weight
        self.description = description
        self.date = datetime.datetime.now()

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
        print(f"\nWaste entry added successfully!")

    def get_statistics(self) -> Dict[str, float]:
        stats = {cat: 0.0 for cat in [WasteCategory.ORGANIC, WasteCategory.RECYCLABLE, 
                                    WasteCategory.HAZARDOUS, WasteCategory.GENERAL]}
        
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
                    entry.date = datetime.datetime.fromisoformat(entry_data["date"])
                    self.waste_entries.append(entry)
        except Exception as e:
            print(f"Error loading data: {e}")

def main():
    system = WasteManagementSystem()
    
    while True:
        print("\n=== Waste Management System ===")
        print("1. Add Waste Entry")
        print("2. View Statistics")
        print("3. Get Tips")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            print("\nWaste Categories:")
            print("1. Organic")
            print("2. Recyclable")
            print("3. Hazardous")
            print("4. General")
            
            cat_choice = input("Select category (1-4): ")
            categories = {
                "1": WasteCategory.ORGANIC,
                "2": WasteCategory.RECYCLABLE,
                "3": WasteCategory.HAZARDOUS,
                "4": WasteCategory.GENERAL
            }
            
            if cat_choice in categories:
                try:
                    weight = float(input("Enter weight (kg): "))
                    description = input("Enter description: ")
                    system.add_waste_entry(categories[cat_choice], weight, description)
                except ValueError:
                    print("Invalid weight! Please enter a number.")
            else:
                print("Invalid category choice!")
        
        elif choice == "2":
            stats = system.get_statistics()
            print("\n=== Waste Statistics ===")
            for category, weight in stats.items():
                print(f"{category}: {weight:.2f} kg")
            
            total = sum(stats.values())
            print(f"\nTotal waste: {total:.2f} kg")
        
        elif choice == "3":
            print("\nSelect category for tips:")
            print("1. Organic")
            print("2. Recyclable")
            print("3. Hazardous")
            print("4. General")
            
            cat_choice = input("Select category (1-4): ")
            categories = {
                "1": WasteCategory.ORGANIC,
                "2": WasteCategory.RECYCLABLE,
                "3": WasteCategory.HAZARDOUS,
                "4": WasteCategory.GENERAL
            }
            
            if cat_choice in categories:
                tips = system.get_tips(categories[cat_choice])
                print(f"\nTips for {categories[cat_choice]} waste:")
                for i, tip in enumerate(tips, 1):
                    print(f"{i}. {tip}")
            else:
                print("Invalid category choice!")
        
        elif choice == "4":
            print("\nThank you for using the Waste Management System!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()