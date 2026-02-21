from pymongo import MongoClient
import json
from datetime import datetime

# Connection Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["evon_nosql_db"]
telemetry = db["ride_telemetry"]

def is_authorized(sid):
    """Check against the master JSON list before allowing NoSQL logs."""
    try:
        with open('students_demo.json', 'r') as f:
            data = json.load(f)
            return any(s['student_id'] == sid and s.get('authorized') for s in data)
    except FileNotFoundError:
        return False

def nosql_menu():
    while True:
        print("\n--- EVON NOSQL TELEMETRY TERMINAL ---")
        print("1. Start Ride Log (CREATE)")
        print("2. Fetch Ride Data (READ)")
        print("3. Update Sensor Sync (UPDATE)")
        print("4. Delete Log (DELETE)")
        print("5. Fleet Battery Analytics (AGGREGATE)")
        print("6. Exit")
        
        choice = input("\nSelect Protocol: ")

        if choice == '1':
            sid = input("Enter Authorized Student ID: ")
            if is_authorized(sid):
                rid = input("New Ride ID: ")
                telemetry.insert_one({
                    "ride_id": rid, 
                    "student_id": sid, 
                    "battery_level": 100, 
                    "status": "ACTIVE"
                })
                print(">>> Document Created.")
            else:
                print(">>> Access Denied: ID not in Master List.")

        elif choice == '2':
            sid = input("Enter Student ID to Query: ")
            
            # Use .find() to get a cursor of all matching documents
            # Ensure sid is treated as a string to match the 'is_authorized' input
            results = list(telemetry.find({"student_id": str(sid)}))
            
            if not results:
                print(f"\n>>> SYSTEM_NOTIFY: No telemetry packets found for ID {sid}.")
                print(">>> Suggestion: Initialize a ride (Option 1) first.")
            else:
                print(f"\n" + "—"*20)
                print(f" TELEMETRY DATA: {sid} ")
                print("—"*20)
                for r in results:
                    # Formatting the output for your screenshots
                    status_icon = "🟢" if r.get('status') == "ACTIVE" else "🔴"
                    print(f"{status_icon} RIDE_ID: {r.get('ride_id', 'N/A')}")
                    print(f"   ⚡ BATT: {r.get('battery_level')}%")
                    print(f"   📅 SYNC: {r.get('timestamp')}")
                    print("—"*20)

        elif choice == '5':
            # AGGREGATE: Demonstrate the NoSQL Aggregation Pipeline
            pipeline = [
                {"$match": {"status": "ACTIVE"}},
                {"$group": {"_id": None, "avg_batt": {"$avg": "$battery_level"}}}
            ]
            result = list(telemetry.aggregate(pipeline))
            print(f">>> Avg Battery Level: {result[0]['avg_batt']}%" if result else "No Active Rides.")

        elif choice == '6': break

nosql_menu()