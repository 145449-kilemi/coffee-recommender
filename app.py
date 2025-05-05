from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify  
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime
from flask_login import login_user
from flask import request
import logging
from sqlalchemy import text
from logging.handlers import RotatingFileHandler
import pandas as pd
import pickle
import sqlite3

# Create Flask app and configure

app = Flask(__name__)
app.secret_key = '6bc5fb61beac3d105cfd4f647c2cc560'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/User/OneDrive - Strathmore University/Desktop/COFFEE-20241010T112042Z-001/COFFEE/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Initialize Migrate
migrate = Migrate(app, db)

class AssociationRules(db.Model):
    __tablename__ = 'association_rules'

    id = db.Column(db.Integer, primary_key=True)
    antecedents = db.Column(db.String, nullable=False)
    consequents = db.Column(db.String, nullable=False)
    support = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    lift = db.Column(db.Float, nullable=False)
    # Add other fields if they exist in your table

    def __repr__(self):
        return f'<AssociationRules {self.antecedents} -> {self.consequents}>'
# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

        # Method to set the password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define Coffee Equipment model
class CoffeeEquipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(200))

# List of equipment data
equipment_data = [
    {
        "Name": "Aeropress",
        "description": "Portable, Compact coffee maker.",
        "price": 30.00,
        "stock_quantity": 15,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Aeropress.jpg"
    },
    {
        "Name": "Cold Brew Coffee Maker",
        "description": "1.5 liters, Glass.",
        "price": 40.00,
        "stock_quantity": 12,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Cold Brew Coffee Maker.jpg"
    },
    {
        "Name": "Drip Coffee Maker",
        "description": "12-Cup, Programmable coffee machine.",
        "price": 60.00,
        "stock_quantity": 9,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Drip Coffee Maker.jpg"
    },
    {
        "Name": "Espresso Machine",
        "description": "High-quality espresso machine for coffee lovers.",
        "price": 499.99,
        "stock_quantity": 10,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Espresso Machine.jpg"
    },
    {
        "Name": "French Press",
        "description": "1-liter, Glass French press.",
        "price": 25.00,
        "stock_quantity": 7,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/French Press.jpg"
    },
    {
        "Name": "Iced Coffee Brewer",
        "description": "Cold brew system.",
        "price": 45.00,
        "stock_quantity": 6,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Iced Coffee Brewer.jpg"
    },
    {
        "Name": "Moka Pot",
        "description": "Stovetop Espresso Maker.",
        "price": 24.99,
        "stock_quantity": 5,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Moka Pot.jpg"
    },
    {
        "Name": "Nitro Cold Brew Dispenser",
        "description": "Cold-brew, nitrogen infusion system.",
        "price": 64.00,
        "stock_quantity": 8,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Nitro Cold Brew Dispenser.jpg"
    },
    {
        "Name": "Pour-over Brewer",
        "description": "Ceramic, Drip-style brewer.",
        "price": 25.00,
        "stock_quantity": 4,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Pour-over Brewer.jpg"
    },
    {
        "Name": "Siphon Coffee Maker",
        "description": "Glass, 5-cup siphon brewer.",
        "price": 79.99,
        "stock_quantity": 7,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Siphon Coffee Maker.jpg"
    },
    {
        "Name": "Single Serve Coffee Maker",
        "description": "K-cup system coffee maker.",
        "price": 99.99,
        "stock_quantity": 15,
        "last_updated": datetime.now(),
        "image_path": "img/brewing_equipment/Single Serve Coffee Maker.png"
    },
    {
        "Name": "Espresso Grinder",
        "description": "40 grind settings.",
        "price": 129.99,
        "stock_quantity": 10,
        "last_updated": datetime.now(),
        "image_path": "img/grinding_equipment/Espresso Grinder.png"
    },
    {
        "Name": "Coffee Grinder",
        "description": "200W motor coffee grinder.",
        "price": 49.99,
        "stock_quantity": 20,
        "last_updated": datetime.now(),
        "image_path": "img/grinding_equipment/Coffee Grinder.png"
    },
    {
        "Name": "Burr Grinder",
        "description": "Steel burrs, 40 settings grinder.",
        "price": 89.99,
        "stock_quantity": 8,
        "last_updated": datetime.now(),
        "image_path": "img/grinding_equipment/Burr Grinder.jpg"
    },
    {
        "Name": "Milk Frother",
        "description": "Electric, Stainless Steel frother.",
        "price": 35.00,
        "stock_quantity": 15,
        "last_updated": datetime.now(),
        "image_path": "img/milk_and_steaming_tools/Milk Frother.png"
    },
    {
        "Name": "Water Filter System",
        "description": "Reduces impurities, 6 months.",
        "price": 59.99,
        "stock_quantity": 7,
        "last_updated": datetime.now(),
        "image_path": "img/water_management/Water Filter System.png"
    },
    {
        "Name": "Shot Glasses",
        "description": "2 oz, Glass shot glasses.",
        "price": 15.00,
        "stock_quantity": 30,
        "last_updated": datetime.now(),
        "image_path": "img/tamping_and_measuring_tools/Shot Glasses.png"
    },
    {
        "Name": "Milk Frother Cleaning Solution",
        "description": "Specialized cleaning solution.",
        "price": 12.99,
        "stock_quantity": 20,
        "last_updated": datetime.now(),
        "image_path": "img/cleaning_and_maintenance/Milk Frother Cleaning Solution.png"
    },
    {
        "Name": "Coffee Cups",
        "description": "6oz, Porcelain coffee cups.",
        "price": 25.00,
        "stock_quantity": 40,
        "last_updated": datetime.now(),
        "image_path": "img/serving_and_accessories/Coffee Cups.jpg"
    },
    {
        "Name": "Ice Maker",
        "description": "Compact ice maker, 26 lbs/day.",
        "price": 129.99,
        "stock_quantity": 3,
        "last_updated": datetime.now(),
        "image_path": "img/cold_beverage_and_miscellaneous/Ice Maker.png"
    },
    {
        "Name": "POS System",
        "description": "Touchscreen, Wi-Fi enabled POS system.",
        "price": 200.00,
        "stock_quantity": 5,
        "last_updated": datetime.now(),
        "image_path": "img/pos_and_shop_operations/POS System.jpg"
    },
    {
        "Name": "Cash Register",
        "description": "Advanced features, multi-drawer cash register.",
        "price": 150.00,
        "stock_quantity": 10,
        "last_updated": datetime.now(),
        "image_path": "img/pos_and_shop_operations/Cash Register.jpg"
    },
    {
        "Name": "Receipt Printer",
        "description": "Thermal, 80mm receipt printer.",
        "price": 120.00,
        "stock_quantity": 7,
        "last_updated": datetime.now(),
        "image_path": "img/pos_and_shop_operations/Receipt Printer.jpg"
    },
    {
        "Name": "Freezers",
        "description": "Upright, 5.0 cu ft freezer.",
        "price": 300.00,
        "stock_quantity": 4,
        "last_updated": datetime.now(),
        "image_path": "img/storage_equipment/Freezers.jpg"
    },
    {
        "Name": "Refrigerators",
        "description": "Energy-efficient, 18 cu ft refrigerator.",
        "price": 450.00,
        "stock_quantity": 3,
        "last_updated": datetime.now(),
        "image_path": "img/storage_equipment/Refrigerators.jpg"
    },
    {
        "Name": "Coffee Bean Storage Bins",
        "description": "Large capacity, BPA-free bins for coffee beans.",
        "price": 20.00,
        "stock_quantity": 25,
        "last_updated": datetime.now(),
        "image_path": "img/storage_equipment/Coffee Bean Storage Bins.jpg"
    },
    {
        "Name": "Thermometers",
        "description": "Instant-read, Stainless Steel thermometers.",
        "price": 10.00,
        "stock_quantity": 50,
        "last_updated": datetime.now(),
        "image_path": "img/measuring_and_specialty_tools/Thermometers.jpg"
    },
    {
        "Name": "Whipped Cream Dispenser",
        "description": "1-pint, Aluminum whipped cream dispenser.",
        "price": 40.00,
        "stock_quantity": 20,
        "last_updated": datetime.now(),
        "image_path": "img/cold_beverage_and_miscellaneous/Whipped Cream Dispenser.png"
    },
        {
        "Name": "Blender",
        "description": "Professional Series, 64 oz blender.",
        "price": 399.99,
        "stock_quantity": 3,
        "last_updated": datetime.now(),
        "image_path": "img/cold_beverage_and_miscellaneous/Blender.jpg"
    },
    {
        "Name": "Creamer Containers",
        "description": "Ceramic, 12 oz containers.",
        "price": 15.00,
        "stock_quantity": 25,
        "last_updated": datetime.now(),
        "image_path": "img/serving_and_accessories/Creamer Containers.jpg"
    },
    {
        "Name": "Sugar Dispensers",
        "description": "18 oz, Glass dispensers.",
        "price": 10.00,
        "stock_quantity": 30,
        "last_updated": datetime.now(),
        "image_path": "img/serving_and_accessories/Sugar Dispensers.jpg"
    },
    {
        "Name": "Coffee Stirrers",
        "description": "Wooden, Pack of 100 stirrers.",
        "price": 5.00,
        "stock_quantity": 100,
        "last_updated": datetime.now(),
        "image_path": "img/serving_and_accessories/Coffee Stirrers.jpg"
    },
    {
        "Name": "Saucers",
        "description": "Matching to coffee cups saucers.",
        "price": 8.00,
        "stock_quantity": 60,
        "last_updated": datetime.now(),
        "image_path": "img/serving_and_accessories/Saucers.jpg"
    },
    {
        "Name": "Coffee Canisters",
        "description": "Airtight, Stainless Steel canisters.",
        "price": 25.00,
        "stock_quantity": 20,
        "last_updated": datetime.now(),
        "image_path": "img/storage_equipment/Coffee Canisters.jpg"
    },
    {
        "Name": "Water Softener",
        "description": "Capacity 20L water softener.",
        "price": 75.00,
        "stock_quantity": 10,
        "last_updated": datetime.now(),
        "image_path": "img/water_management/Water Softener.png"
    },
    {
        "Name": "Knock Box",
        "description": "Anti-slip, Stainless Steel knock box.",
        "price": 35.00,
        "stock_quantity": 10,
        "last_updated": datetime.now(),
        "image_path": "img/cleaning_and_maintenance/Knock Box.png"
    },
    {
        "Name": "Coffee Drip Tray",
        "description": "Removable, easy-to-clean drip tray.",
        "price": 20.00,
        "stock_quantity": 15,
        "last_updated": datetime.now(),
        "image_path": "img/cleaning_and_maintenance/Coffee Drip Tray.png"
    },
]
def populate_equipment():
    try:
        # Delete all existing records in the table before populating
        CoffeeEquipment.query.delete()
        db.session.commit()
        
        # Populate the table with equipment_data
        for item in equipment_data:
            equipment = CoffeeEquipment(
                Name=item['Name'],  # Make sure to use 'Name' to match dictionary key
                description=item['description'],
                price=item['price'],
                stock_quantity=item['stock_quantity'],
                last_updated=item['last_updated'],
                image_path=item['image_path']
            )
            db.session.add(equipment)
            print(f"Added: {item['Name']}")  # Use 'Name' here instead of 'name' for consistency
        db.session.commit()
        print("Database populated with equipment data.")
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()



with app.app_context():
    db.create_all()  # Ensures all tables are created
    populate_equipment()  # Calls the function to add items
    
# Define Recommendations model
class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recommended_items = db.Column(db.Text, nullable=False)
    recommendation_time = db.Column(db.DateTime, default=datetime.utcnow)



# Define the path to the .pkl file
file_path = r"C:\Users\User\OneDrive - Strathmore University\Desktop\COFFEE-20241010T112042Z-001\COFFEE\new_association_rules.pkl"


# Load the association rules data from the .pkl file
association_rules_df = pd.read_pickle(file_path)

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/User/OneDrive - Strathmore University/Desktop/COFFEE-20241010T112042Z-001/COFFEE/instance/app.db')

cursor = conn.cursor()

# Insert data into the association_rules table
for _, row in association_rules_df.iterrows():
    cursor.execute("""
    INSERT INTO association_rules (
        antecedents, consequents, antecedent_support, consequent_support, 
        support, confidence, lift, leverage, conviction, zhangs_metric
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(row['antecedents']),            # Convert to string if necessary
        str(row['consequents']),
        row['antecedent support'],
        row['consequent support'],
        row['support'],
        row['confidence'],
        row['lift'],
        row['leverage'],
        row['conviction'],
        row.get('zhangs_metric', None)      # Use None if zhangs_metric is missing
    ))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Association rules data has been successfully inserted into the SQLite database.")
# Load your dataset with the new 'Equipment Name' column
data = pd.read_csv('updated_coffee_shop_equipment_transactions.csv')
   
# Load the saved model
with open('new_association_rules.pkl', 'rb') as f:
    rules = pickle.load(f)
    print(rules.head())  # Check if the rules are loaded correctly

equipment_image_mapping = {
    # Brewing Equipment
    "Espresso Machine": "/static/img/brewing_equipment/Espresso Machine.jpg",
    "Drip Coffee Maker": "/static/img/brewing_equipment/Drip Coffee Maker.jpg",
    "French Press": "/static/img/brewing_equipment/French Press.jpg",
    "Pour-over Brewer": "/static/img/brewing_equipment/Pour-over Brewer.jpg",
    "Cold Brew Coffee Maker": "/static/img/brewing_equipment/Cold Brew Coffee Maker.jpg",
    "Moka Pot": "/static/img/brewing_equipment/Moka Pot.jpg",
    "Siphon Coffee Maker": "/static/img/brewing_equipment/Siphon Coffee Maker.jpg",
    "Single Serve Coffee Maker": "/static/img/brewing_equipment/Single Serve Coffee Maker.png",
    "Aeropress": "/static/img/brewing_equipment/Aeropress.jpg",

    # Grinding Equipment
    "Coffee Grinder": "/static/img/grinding_equipment/Coffee Grinder.png",
    "Burr Grinder": "/static/img/grinding_equipment/Burr Grinder.png",
    "Espresso Grinder": "/static/img/grinding_equipment/Espresso Grinder.png",

    # Milk and Steaming Tools
    "Milk Frother": "/static/img/milk_and_steaming_tools/Milk Frother.png",
    "Steam Wand": "/static/img/milk_and_steaming_tools/Steam Wand.jpg",
    "Automatic Milk Steamer": "/static/img/milk_and_steaming_tools/Automatic Milk Steamer.jpg",

    # Water Management
    "Water Filter System": "/static/img/water_management/Water Filter System.jpg",
    "Water Softener": "/static/img/water_management/Water Softener.png",

    # Tamping and Measuring Tools
    "Tamper": "/static/img/tamping_and_measuring_tools/Tamper.jpg",
    "Coffee Scale": "/static/img/tamping_and_measuring_tools/Coffee Scale.jpg",
    "Portafilter": "/static/img/tamping_and_measuring_tools/Portafilter.jpg",

    # Shop Operations
    "POS System": "/static/img/shop_operations/POS System.png",
    "Cash Register": "/static/img/shop_operations/Cash Register.jpg",
    "Receipt Printer": "/static/img/shop_operations/Receipt Printer.jpg",

    # Serving and Accessories
    "Coffee Cups": "/static/img/serving_and_accessories/Coffee Cups.png",
    "To-go Cups": "/static/img/serving_and_accessories/To-go Cups.jpg",
    "Saucers": "/static/img/serving_and_accessories/Saucers.jpg",
    "Coffee Stirrers": "/static/img/serving_and_accessories/Coffee Stirrers.png",
    "Sugar Dispensers": "/static/img/serving_and_accessories/Sugar Dispensers.jpg",
    "Creamer Containers": "/static/img/serving_and_accessories/Creamer Containers.jpg",
    "Thermal Coffee Carafes": "/static/img/serving_and_accessories/Thermal Coffee Carafes.jpg",
    "Shot Glasses": "/static/img/serving_and_accessories/Shot Glasses.jpg",

    # Cleaning and Maintenance
    "Grinder Cleaning Brush": "/static/img/cleaning_and_maintenance/Grinder Cleaning Brush.png",
    "Espresso Machine Cleaning Solution": "/static/img/cleaning_and_maintenance/Espresso Machine Cleaning Solution.jpg",
    "Milk Frother Cleaning Solution": "/static/img/cleaning_and_maintenance/Milk Frother Cleaning Solution.jpg",

    # Cold Beverage and Miscellaneous Equipment
    "Nitro Cold Brew Dispenser": "/static/img/cold_beverage_and_miscellaneous/Nitro Cold Brew Dispenser.png",
    "Iced Coffee Brewer": "/static/img/cold_beverage_and_miscellaneous/Iced Coffee Brewer.jpg",
    "Blender": "/static/img/cold_beverage_and_miscellaneous/Blender.jpg",
    "Whipped Cream Dispenser": "/static/img/cold_beverage_and_miscellaneous/Whipped Cream Dispenser.png",

    # Storage Equipment
    "Coffee Bean Storage Bins": "/static/img/storage_equipment/Coffee Bean Storage Bins.jpg",
    "Coffee Canisters": "/static/img/storage_equipment/Coffee Canisters.jpg",
    "Refrigerators": "/static/img/storage_equipment/Refrigerators.jpg",
    "Freezers": "/static/img/storage_equipment/Freezers.jpg",
    "Ice Maker": "/static/img/storage_equipment/Ice Maker.png",

    # Measuring and Specialty Tools
    "Thermometers": "/static/img/measuring_and_specialty_tools/Thermometers.jpg"
}



# Update 'Image Path' in the dataset
data['Image Path'] = data['Equipment Name'].map(equipment_image_mapping).fillna('/static/img/default.png')


# Function to sum the values of each equipment type column
def get_popular_equipment():
    equipment_columns = [
        'Espresso Machine', 'Drip Coffee Maker', 'French Press', 'Moka Pot',
        'Cold Brew Coffee Maker', 'Milk Frother', 'Coffee Grinder', 'Steam Wand',
        'Siphon Coffee Maker', 'Aeropress', 'Single Serve Coffee Maker', 'Nitro Cold Brew Dispenser',
        'Iced Coffee Brewer', 'Automatic Milk Steamer', 'Tamper', 'Coffee Scale', 'Portafilter',
        'Knock Box', 'Shot Glasses', 'Coffee Drip Tray', 'Coffee Cups', 'To-go Cups', 'Saucers',
        'Coffee Stirrers', 'Sugar Dispensers', 'Creamer Containers', 'Thermal Coffee Carafes',
        'Grinder Cleaning Brush', 'Espresso Machine Cleaning Solution', 'Blender',
        'Whipped Cream Dispenser', 'Ice Maker', 'POS System', 'Cash Register', 'Receipt Printer',
        'Refrigerators', 'Freezers', 'Coffee Bean Storage Bins', 'Thermometers'
    ]

    popular_equipment = data[equipment_columns].sum().to_dict()
    return popular_equipment
    
@app.route('/equipment/<category>')
def get_equipment_by_category(category):
    
    # Updated data for each category with equipment and images
    equipment_data = { 
 'brewing': [
        {'Name': 'Aeropress', 'EquipmentID': 'BR001', 'Brand': 'Aeropress', 'Specification': 'Portable, Compact', 'Image Path': 'img/brewing_equipment/Aeropress.jpg', 'Price': 29.95},
        {'Name': 'Cold Brew Coffee Maker', 'EquipmentID': 'BR002', 'Brand': 'Toddy', 'Specification': '1.5 liters, Glass', 'Image Path': 'img/brewing_equipment/Cold Brew Coffee Maker.jpg', 'Price': 39.99},
        {'Name': 'Drip Coffee Maker', 'EquipmentID': 'BR003', 'Brand': 'Breville', 'Specification': '12-Cup, Programmable', 'Image Path': 'img/brewing_equipment/Drip Coffee Maker.jpg', 'Price': 129.99},
        {'Name': 'Espresso Machine', 'EquipmentID': 'BR004', 'Brand': 'Breville', 'Specification': '15-bar pump', 'Image Path': 'img/brewing_equipment/Espresso Machine.jpg', 'Price': 499.99},
        {'Name': 'French Press', 'EquipmentID': 'BR005', 'Brand': 'Bodum', 'Specification': '1-liter, Glass', 'Image Path': 'img/brewing_equipment/French Press.jpg', 'Price': 22.99},
        {'Name': 'Iced Coffee Brewer', 'EquipmentID': 'BR006', 'Brand': 'Hario', 'Specification': 'Cold brew system', 'Image Path': 'img/brewing_equipment/Iced Coffee Brewer.jpg', 'Price': 35.00},
        {'Name': 'Moka Pot', 'EquipmentID': 'BR007', 'Brand': 'Bialetti', 'Specification': 'Stovetop Espresso Maker', 'Image Path': 'img/brewing_equipment/Moka pot.jpg', 'Price': 24.99},
        {'Name': 'Nitro Cold Brew Dispenser', 'EquipmentID': 'BR008', 'Brand': 'GrowlerWerks', 'Specification': '64-ounce, Nitrogen infusion', 'Image Path': 'img/brewing_equipment/Nitro Cold Brew Dispenser.jpg', 'Price': 199.00},
        {'Name': 'Pour-over Brewer', 'EquipmentID': 'BR009', 'Brand': 'Hario', 'Specification': 'Ceramic, Drip-style', 'Image Path': 'img/brewing_equipment/Pour-over Brewer.jpg', 'Price': 25.00},
        {'Name': 'Siphon Coffee Maker', 'EquipmentID': 'BR010', 'Brand': 'Yama', 'Specification': 'Glass, 5-cup', 'Image Path': 'img/brewing_equipment/Siphon Coffee Maker.jpg', 'Price': 79.99},
        {'Name': 'Single Serve Coffee Maker', 'EquipmentID': 'BR011', 'Brand': 'Keurig', 'Specification': 'K-cup system', 'Image Path': 'img/brewing_equipment/Single Serve Coffee Maker.png', 'Price': 99.99}
    ],
    'grinding': [
        {'Name': 'Espresso Grinder', 'EquipmentID': 'GR001', 'Brand': 'Baratza', 'Specification': '40 grind settings', 'Image Path': 'img/grinding_equipment/Espresso Grinder.png', 'Price': 139.99},
        {'Name': 'Coffee Grinder', 'EquipmentID': 'GR002', 'Brand': 'Krups', 'Specification': '200W motor', 'Image Path': 'img/grinding_equipment/Coffee Grinder.png', 'Price': 39.99},
        {'Name': 'Burr Grinder', 'EquipmentID': 'GR003', 'Brand': 'Baratza', 'Specification': 'Steel burrs, 40 settings', 'Image Path': 'img/grinding_equipment/Burr Grinder.jpg', 'Price': 129.99}
    ],
    'milk_and_steaming_tools': [
        {'Name': 'Milk Frother', 'EquipmentID': 'MS001', 'Brand': 'Nespresso', 'Specification': 'Electric, Stainless Steel', 'Image Path': 'img/milk_and_steaming_tools/Milk Frother.png', 'Price': 29.99},
        {'Name': 'Steam Wand', 'EquipmentID': 'MS002', 'Brand': 'Breville', 'Specification': 'Manual, Stainless Steel', 'Image Path': 'img/milk_and_steaming_tools/Steam Wand.png', 'Price': 12.99},
        {'Name': 'Automatic Milk Steamer', 'EquipmentID': 'MS003', 'Brand': 'DeLonghi', 'Specification': 'Automatic, 10oz', 'Image Path': 'img/milk_and_steaming_tools/Automatic Milk Steamer.png', 'Price': 49.99},
        {'Name': 'Milk Pitcher', 'EquipmentID': 'MS004', 'Brand': 'Rattleware', 'Specification': 'Stainless Steel, 12oz', 'Image Path': 'img/milk_and_steaming_tools/Milk Pitcher.png', 'Price': 14.99}
    ],

    'water_management': [
    {'Name': 'Water Filter System', 'EquipmentID': 'WT001', 'Brand': 'Brita', 'Specification': '6 months, Reduces impurities', 'Image Path': 'img/water_management/Water Filter System.png', 'Price': 45.99},
    {'Name': 'Water Softener', 'EquipmentID': 'WT002', 'Brand': 'Bosch', 'Specification': 'Capacity 20L', 'Image Path': 'img/water_management/Water Softener.png', 'Price': 119.99}
],

'tamping_and_measuring_tools': [
    {'Name': 'Shot Glasses', 'EquipmentID': 'TP001', 'Brand': 'Barista', 'Specification': '2 oz, Glass', 'Image Path': 'img/tamping_and_measuring_tools/Shot Glasses.png', 'Price': 7.99},
    {'Name': 'Portafilter', 'EquipmentID': 'TP002', 'Brand': 'Rancilio', 'Specification': '58mm, Brass', 'Image Path': 'img/tamping_and_measuring_tools/Portafilter.png', 'Price': 59.99},
    {'Name': 'Coffee Scale', 'EquipmentID': 'TP003', 'Brand': 'Hario', 'Specification': 'Precise weight measurement', 'Image Path': 'img/tamping_and_measuring_tools/Coffee Scale.png', 'Price': 49.99},
    {'Name': 'Tamper', 'EquipmentID': 'TP004', 'Brand': 'Reg Barber', 'Specification': '58mm, Aluminum', 'Image Path': 'img/tamping_and_measuring_tools/Tamper.png', 'Price': 29.99}
],

'cleaning_and_maintenance': [
    {'Name': 'Milk Frother Cleaning Solution', 'EquipmentID': 'CL001', 'Brand': 'Urnex', 'Specification': 'Cleaning Solution', 'Image Path': 'img/cleaning_and_maintenance/Milk Frother Cleaning Solution.png', 'Price': 12.99},
    {'Name': 'Espresso Machine Cleaning Solution', 'EquipmentID': 'CL002', 'Brand': 'Urnex', 'Specification': 'Descaling Solution', 'Image Path': 'img/cleaning_and_maintenance/Espresso Machine Cleaning Solution.png', 'Price': 14.99},
    {'Name': 'Grinder Cleaning Brush', 'EquipmentID': 'CM003', 'Brand': 'Pallo', 'Specification': 'Nylon bristles, Heat-resistant', 'Image Path': 'img/cleaning_and_maintenance/Grinder Cleaning Brush.jpg', 'Price': 7.99},
    {'Name': 'Coffee Drip Tray', 'EquipmentID': 'CM004', 'Brand': 'Breville', 'Specification': 'Removable, Easy to clean', 'Image Path': 'img/cleaning_and_maintenance/Coffee Drip Tray.png', 'Price': 15.99},
    {'Name': 'Knock Box', 'EquipmentID': 'CM005', 'Brand': 'Dreamfarm', 'Specification': 'Anti-slip, Stainless Steel', 'Image Path': 'img/cleaning_and_maintenance/Knock Box.png', 'Price': 24.99}
],

'serving_and_accessories': [
    {'Name': 'Coffee Cups', 'EquipmentID': 'SR001', 'Brand': 'Acme', 'Specification': '6oz, Porcelain', 'Image Path': 'img/serving_and_accessories/Coffee Cups.jpg', 'Price': 14.99},
    {'Name': 'To-go Cups', 'EquipmentID': 'SR002', 'Brand': 'Eco-Friendly', 'Specification': 'Disposable, 12oz', 'Image Path': 'img/serving_and_accessories/To-go Cups.jpg', 'Price': 12.99},
    {'Name': 'Thermal Coffee Carafes', 'EquipmentID': 'SA001', 'Brand': 'Zojirushi', 'Specification': '1.5 liters, Stainless Steel', 'Image Path': 'img/serving_and_accessories/Thermal Coffee Carafes.jpg', 'Price': 22.99},
    {'Name': 'Creamer Containers', 'EquipmentID': 'SA002', 'Brand': 'OXO', 'Specification': 'Ceramic, 12 oz', 'Image Path': 'img/serving_and_accessories/Creamer Containers.jpg', 'Price': 9.99},
    {'Name': 'Sugar Dispensers', 'EquipmentID': 'SA003', 'Brand': 'Winco', 'Specification': '18 oz, Glass', 'Image Path': 'img/serving_and_accessories/Sugar Dispensers.jpg', 'Price': 8.99},
    {'Name': 'Coffee Stirrers', 'EquipmentID': 'SA004', 'Brand': 'Disposable', 'Specification': 'Wooden, Pack of 100', 'Image Path': 'img/serving_and_accessories/Coffee Stirrers.jpg', 'Price': 4.99},
    {'Name': 'Saucers', 'EquipmentID': 'SA005', 'Brand': 'Acme', 'Specification': 'Matching to coffee cups', 'Image Path': 'img/serving_and_accessories/Saucers.jpg', 'Price': 9.99}
],

'cold_beverage_and_miscellaneous': [
    {'Name': 'Ice Maker', 'EquipmentID': 'CD001', 'Brand': 'Igloo', 'Specification': 'Compact, 26 lbs/day', 'Image Path': 'img/cold_beverage_and_miscellaneous/Ice Maker.png', 'Price': 109.99},
    {'Name': 'Whipped Cream Dispenser', 'EquipmentID': 'CD002', 'Brand': 'iSi', 'Specification': '1-pint, Aluminum', 'Image Path': 'img/cold_beverage_and_miscellaneous/Whipped Cream Dispenser.png', 'Price': 29.99},
    {'Name': 'Blender', 'EquipmentID': 'CB003', 'Brand': 'Vitamix', 'Specification': 'Professional Series, 64 oz', 'Image Path': 'img/cold_beverage_and_miscellaneous/Blender.jpg', 'Price': 399.99}
],

'pos_and_shop_operations': [
    {'Name': 'POS System', 'EquipmentID': 'PS001', 'Brand': 'Square', 'Specification': 'Touchscreen, Wi-Fi', 'Image Path': 'img/pos_and_shop_operations/POS System.jpg', 'Price': 1000.00},
    {'Name': 'Cash Register', 'EquipmentID': 'POS002', 'Brand': 'Casio', 'Specification': 'Advanced features, Multi-drawer', 'Image Path': 'img/pos_and_shop_operations/Cash Register.jpg', 'Price': 299.99},
    {'Name': 'Receipt Printer', 'EquipmentID': 'PS003', 'Brand': 'Epson', 'Specification': 'Thermal, 80mm', 'Image Path': 'img/pos_and_shop_operations/Receipt Printer.jpg', 'Price': 199.99}
],

'storage_equipment': [
    {'Name': 'Coffee Canisters', 'EquipmentID': 'ST001', 'Brand': 'Oxo', 'Specification': 'Airtight, Stainless Steel', 'Image Path': 'img/storage_equipment/Coffee Canisters.jpg', 'Price': 14.99},
    {'Name': 'Freezers', 'EquipmentID': 'ST002', 'Brand': 'Whirlpool', 'Specification': 'Upright, 5.0 cu ft', 'Image Path': 'img/storage_equipment/Freezers.jpg', 'Price': 499.99},
    {'Name': 'Refrigerators', 'EquipmentID': 'ST003', 'Brand': 'Samsung', 'Specification': 'Energy-efficient, 18 cu ft', 'Image Path': 'img/storage_equipment/Refrigerators.jpg', 'Price': 999.99},
    {'Name': 'Coffee Bean Storage Bins', 'EquipmentID': 'ST004', 'Brand': 'Rubbermaid', 'Specification': 'Large capacity, BPA-free', 'Image Path': 'img/storage_equipment/Coffee Bean Storage Bins.jpg', 'Price': 25.99}
],

'measuring_and_specialty_tools': [
    {'Name': 'Thermometers', 'EquipmentID': 'MS001', 'Brand': 'Barista Gear', 'Specification': 'Instant-read, Stainless Steel', 'Image Path': 'img/measuring_and_specialty_tools/Thermometers.jpg', 'Price': 9.99}
]
}

 # Return equipment for the selected category or an empty list if no data found
    return jsonify(equipment_data.get(category, []))
    popular_equipment = data[equipment_columns].sum().to_dict()
    return popular_equipment


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations')
def recommendations():
    items = [
        {
            "name": "Espresso Machine",
            "description": "A high-quality espresso machine perfect for small coffee shops.",
            "image": url_for('static', filename='img/brewing_equipment/Espresso Machine.jpg')
        },
        {
            "name": "Coffee Grinder",
            "description": "A premium burr grinder for consistent grind size.",
            "image": url_for('static', filename='img/grinding_equipment/Coffee Grinder.png')
        },
        {
            "name": "Milk Frother",
            "description": "A powerful frother for creating smooth milk froth.",
            "image": url_for('static', filename='img/milk_and_steaming_tools/Milk Frother.png')
        }
    ]
    return render_template('recommendations.html', items=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/recommendations/<item_name>')
def recommendations_view(item_name):
    recommendations = get_recommendations(item_name)
    
    if not recommendations:
        message = "No recommendations found."
        return render_template('recommendations.html', item_name=item_name, message=message)
    
    return render_template('recommendations.html', item_name=item_name, recommendations=recommendations)

# Equipment Management


# User Management Routes
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        new_user = User(username=username, email=email, password_hash=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('New user added successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_user.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    users = User.query.all()
    equipment = CoffeeEquipment.query.all()
    
    # Fetch association rules with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Adjust the number of records per page as needed
    association_rules = AssociationRules.query.paginate(page=page, per_page=per_page)

    return render_template(
        'admin_dashboard.html',
        users=users,
        equipment=equipment,
        association_rules=association_rules
    )




@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        db.session.commit()
        flash('User updated successfully')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully')
    return redirect(url_for('admin_dashboard'))


@app.route('/edit_equipment/<int:equipment_id>', methods=['GET', 'POST'])
def edit_equipment(equipment_id):
    equipment = CoffeeEquipment.query.get_or_404(equipment_id)
    if request.method == 'POST':
        equipment.Name = request.form['Name']
        equipment.category = request.form['category']
        equipment.price = float(request.form['price'])
        equipment.stock_quantity = int(request.form['stock'])
        equipment.description = request.form['description']
        db.session.commit()
        flash('Equipment updated successfully')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_equipment.html', equipment=equipment)

@app.route('/delete_equipment/<int:equipment_id>', methods=['POST'])
def delete_equipment(equipment_id):
    equipment = CoffeeEquipment.query.get_or_404(equipment_id)
    db.session.delete(equipment)
    db.session.commit()
    flash('Equipment deleted successfully')
    return redirect(url_for('admin_dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'customer')  # Default role to 'customer'

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))

        # Create the user with hashed password
        try:
            new_user = User(username=username, email=email, role=role)
            new_user.set_password(password)  # This hashes the password

            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('signin'))  # Redirect to sign-in page after signup
        except Exception as e:
            db.session.rollback()  # Rollback if there's an error
            app.logger.error(f"Error creating user: {e}")
            flash('An error occurred while creating your account. Please try again.', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html')

      


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # Check if user exists and password is correct
        if user and user.check_password(password):
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))  # Redirects to the user dashboard
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('signin'))

    return render_template('signin.html')



# Analytics
@app.route('/analytics')
def analytics():
    # Placeholder for analytics data
    return render_template('analytics.html')

# Settings
@app.route('/settings')
def settings():
    # Placeholder for settings data
    return render_template('settings.html')
def get_recommendations(item_name):
    # Ensure association_rules_df is accessible globally
    global association_rules_df
    
    # Filter association rules where 'antecedents' include the item_name
    recommended_rules = association_rules_df[association_rules_df['antecedents'].apply(lambda x: item_name in x)]
    
    # Use a set to track unique item names to avoid duplicates
    unique_recommendations = set()
    recommendations = []
    
    for index, row in recommended_rules.iterrows():
        consequents = list(row['consequents'])
        for item in consequents:
            # Only add if item name is not already in the set
            if item not in unique_recommendations:
                # Assuming the item has details stored in the CoffeeEquipment database
                equipment = CoffeeEquipment.query.filter_by(Name=item).first()
                if equipment and equipment.Name not in unique_recommendations:
                    recommendations.append({
                        "name": equipment.Name,
                        "description": equipment.description,
                        "price": equipment.price,
                        "image_path": equipment.image_path
                    })
                    # Add the item name to the set to prevent future duplicates
                    unique_recommendations.add(equipment.Name)
    
    # Return a list of unique recommended items
    return recommendations





@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query', '').strip().lower()
    print("Search query:", search_query)  # Debugging: print search query

    if not search_query:
        return render_template('search_results.html', equipment=[], message="No search term provided.")

    # Check if 'Name' exists in data DataFrame columns
    if 'Name' not in data.columns:
        return render_template('search_results.html', equipment=[], message="No 'Name' column found in data.")

    # Clean 'Name' column for consistent searching
    data['cleaned_name'] = data['Name'].str.strip().str.lower()
    filtered_equipment = data[data['cleaned_name'].str.contains(search_query, na=False)]

    # Check if any results were found
    if filtered_equipment.empty:
        return render_template('search_results.html', equipment=[], message="No equipment found.")

    # Convert filtered data to a list of dictionaries for the template
    equipment_data = filtered_equipment.to_dict(orient='records')

    return render_template('search_results.html', equipment=equipment_data)

# Route for adding a recommendation
@app.route('/add_recommendation', methods=['GET', 'POST'])
def add_recommendation():
    if request.method == 'POST':
        antecedent = request.form['antecedent']
        consequent = request.form['consequent']
        
        # Assuming a model called Recommendation to store antecedent-consequent pairs
        new_recommendation = Recommendation(antecedent=antecedent, consequent=consequent)
        db.session.add(new_recommendation)
        db.session.commit()
        flash('New recommendation added successfully!')
        
        return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard

    return render_template('add_recommendation.html')

@app.route('/edit_recommendation/<int:id>', methods=['GET', 'POST'])
def edit_recommendation(id):
    # Use AssociationRules instead of Recommendation
    recommendation = AssociationRules.query.get_or_404(id)
    if request.method == 'POST':
        recommendation.antecedents = request.form['antecedent']
        recommendation.consequents = request.form['consequent']
        db.session.commit()
        flash('Recommendation updated successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_recommendation.html', recommendation=recommendation)


@app.route('/delete_recommendation/<int:id>', methods=['POST'])
def delete_recommendation(id):
    recommendation = Recommendation.query.get_or_404(id)
    db.session.delete(recommendation)
    db.session.commit()
    flash('Recommendation deleted successfully!')
    return redirect(url_for('admin_dashboard'))




def get_recommendations(item_name):
    # Filter association rules where 'antecedents' include the item_name
    recommended_rules = association_rules_df[association_rules_df['antecedents'].apply(lambda x: item_name in x)]
    
    # Extract the 'consequents' from the filtered rules as recommended items
    recommendations = []
    for _, row in recommended_rules.iterrows():
        consequents = list(row['consequents'])
        for item in consequents:
            # Assuming the item has details stored in the CoffeeEquipment database
            equipment = CoffeeEquipment.query.filter_by(Name=item).first()
            if equipment:
                recommendations.append({
                    "name": equipment.Name,
                    "description": equipment.description,
                    "price": equipment.price,
                    "image_path": equipment.image_path
                })
    
    # Return a list of dictionaries containing recommended items
    return recommendations

@app.route('/suggestions')
def suggestions():
    # Get the item_name from the query parameter
    item_name = request.args.get('item_name')
    
    # Fetch recommendations based on the item_name
    recommendations = []
    if item_name:
        recommendations = get_recommendations(item_name)

    return render_template('suggestions.html', item_name=item_name, recommendations=recommendations)

@app.route('/dashboard')
def dashboard():
    # Get the item_name from the query parameter
    item_name = request.args.get('item_name')
    
    # Initialize variables
    recommendations = []
    recommended_details = []
    item = None

    # Fetch recommendations only if item_name is provided
    if item_name:
        # Fetch recommended items based on association rules
        recommended_items = get_recommendations(item_name)
        
        # Extract names from recommended items
        recommended_names = [item['name'] for item in recommended_items]
        
        # Fetch item details for the current item
        item = CoffeeEquipment.query.filter_by(Name=item_name).first()
        
        # Fetch details for recommended items if there are any
        recommended_details = CoffeeEquipment.query.filter(CoffeeEquipment.Name.in_(recommended_names)).all() if recommended_names else []
    
    # Fetch all equipment items to display on the dashboard
    all_equipment = CoffeeEquipment.query.all()
    
    # Render the template with the required context
    return render_template(
        'dashboard.html',
        equipment=all_equipment,
        recommendations=recommended_details,
        item_name=item_name,
        item=item
    )

@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        Name = request.form['Name']
        category = request.form['category']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        description = request.form['description']
        
        # Create a new equipment entry
        new_equipment = CoffeeEquipment(
            Name=Name,
            category=category,
            price=price,
            stock_quantity=stock,
            description=description
        )
        
        # Add and commit to the database
        db.session.add(new_equipment)
        db.session.commit()
        
        flash('New equipment added successfully!')
        return redirect(url_for('admin_dashboard'))
    
    # Render the form if it's a GET request
    return render_template('add_equipment.html')


@app.route('/logout')
def logout():
    flash('Logged out successfully', 'success')
    return redirect(url_for('signin'))

# API endpoint to serve popular equipment data for the chart
@app.route('/api/popular_equipment')
def api_popular_equipment():
    popular_equipment = get_popular_equipment()
    return jsonify(popular_equipment)

if __name__ == '__main__':
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    app.run(debug=True)
