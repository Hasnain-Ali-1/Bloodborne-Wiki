import mysql.connector
import pandas as pd
import numpy as np
import atexit
import base64
import os

from flask import Flask, jsonify
from flask import send_from_directory
from flask_cors import CORS

# Connect to MySQL database server
connection = mysql.connector.connect(
    host="localhost",
    port=3307,  # Change to the port mySQL is running on in your system
    user="root", # Change username to what you set it to
    password="password" # Change password to what you set it to
)

# Create a new database named bloodborne_wiki if it doesn't exist
def create_database():
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS bloodborne_wiki")
        print("Database 'bloodborne_wiki' created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

# Make sure the database bloodborne_wiki is selected
def select_database():
    cursor = connection.cursor()
    try:
        cursor.execute("USE bloodborne_wiki")
        print("Database 'bloodborne_wiki' selected successfully")
    except mysql.connector.Error as err:
        print(f"Error selecting database: {err}")
    finally:
        cursor.close()

# Create new tables within the bloodborne_wiki database
def create_tables():
    select_database()
    create_armorType_table()
    create_armor_table()
    create_caryllRunesType_table()
    create_caryllRunes_table()
    create_hunterTools_table()
    create_weaponType_table()
    create_weapon_table()

# Create a table named armorType within the bloodborne_wiki database, if it doesn't exist
def create_armorType_table():
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS armorType (
                armorTypeID INT PRIMARY KEY NOT NULL,
                armorTypeName VARCHAR(20) NOT NULL
            )
        """)
        print("Table 'armorType' created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating 'armorType' table: {err}")
    finally:
        cursor.close()

# Create a table named armor within the bloodborne_wiki database, if it doesn't exist
def create_armor_table():
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS armor (
                armorID INT PRIMARY KEY NOT NULL,
		armorName VARCHAR(255),
                armorTypeID INT,
		physicalDefense INT,
		bluntDefense INT,
		thrustDefense INT,
		bloodtingeDefense INT,
		arcaneDefense INT,
		fireDefense INT,
		boltDefense INT,
		slowPoisonResistance INT,
		fastPoisonResistance INT,
		frenzyResistance INT,
		beasthoodResistance INT,
		filepath VARCHAR(255),
		FOREIGN KEY (armorTypeID) REFERENCES armorType(armorTypeID)
            )
        """)
        print("Table 'armor' created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating 'armor' table: {err}")
    finally:
        cursor.close()

# Create a table named caryllRunesType within the bloodborne_wiki database, if it doesn't exist
def create_caryllRunesType_table():
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS caryllRunesType (
                runeTypeID INT PRIMARY KEY NOT NULL,
                runeTypeName VARCHAR(20) NOT NULL
            )
        """)
        print("Table 'caryllRunesType' created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating 'caryllRunesType' table: {err}")
    finally:
        cursor.close()

# Create a table named caryllRunes within the bloodborne_wiki database, if it doesn't exist
def create_caryllRunes_table():
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS caryllRunes (
                runeID INT PRIMARY KEY NOT NULL,
                runeTypeID INT NOT NULL,
                runeName VARCHAR(255),
		runeEffect TEXT,
		filepath VARCHAR(255),
		FOREIGN KEY (runeTypeID) REFERENCES caryllRunesType(runeTypeID)
            )
        """)
        print("Table 'caryllRunes' created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating 'caryllRunes' table: {err}")
    finally:
        cursor.close()

# Create a table named hunterTools within the bloodborne_wiki database, if it doesn't exist
def create_hunterTools_table():
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hunterTools (
                toolID INT PRIMARY KEY NOT NULL,
                toolName VARCHAR(255),
		toolDescription TEXT,
		bulletUse INT,
		arcaneRequirements INT,
		arcaneScaling VARCHAR(3),
		filepath VARCHAR(255)
            )
        """)
        print("Table 'hunterTools' created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating 'hunterTools' table: {err}")
    finally:
        cursor.close()

# Create a table named weaponType within the bloodborne_wiki database, if it doesn't exist
def create_weaponType_table():
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weaponType (
                weaponTypeID INT PRIMARY KEY NOT NULL,
                weaponTypeName VARCHAR(20) NOT NULL
            )
        """)
        print("Table 'weaponType' created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating 'weaponType' table: {err}")
    finally:
        cursor.close()

# Create a table named weaponType within the bloodborne_wiki database, if it doesn't exist
def create_weapon_table():
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weapon (
                weaponID INT PRIMARY KEY NOT NULL,
                weaponName VARCHAR(255),
		weaponTypeID INT,
		physicalAttack INT,
		bloodAttack INT,
		arcaneAttack INT,
		fireAttack INT,
		boltAttack INT,
		slowPoisonAttack INT,
		rapidPoisonAttack INT,
		kinDamage INT,
		beastDamage INT,
		strengthRequirement VARCHAR(10),
		skillRequirement VARCHAR(10),
		bloodtingeRequirement VARCHAR(10),
		arcaneRequirement VARCHAR(10),
		durability INT,
		filepath VARCHAR(255),
		FOREIGN KEY (weaponTypeID) REFERENCES weaponType(weaponTypeID)
            )
        """)
        print("Table 'weapon' created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating 'weapon' table: {err}")
    finally:
        cursor.close()

# Function to populate tables using data from CSV files, only if tables are empty
def populate_tables_from_csv():
    # Relative paths to CSV files
    csv_folder = "Spreadsheets"
    csv_files = [
        "armorType.csv",
        "armor.csv",
	"caryllRunesType.csv",
        "caryllRunes.csv",
        "hunterTools.csv",
        "weaponType.csv",
        "weapon.csv"
    ]

    cursor = connection.cursor()

    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]
        csv_path = os.path.join(csv_folder, csv_file)

        # Check if table is empty
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        result = cursor.fetchone()

        if result[0] == 0:
            df = pd.read_csv(csv_path)
            # Replace NaN values with NULL
            df.replace({np.nan: None}, inplace=True)
            for index, row in df.iterrows():
                # Prepare SQL query to insert row into the table
                columns = ', '.join(row.keys())
                values = ', '.join(['%s'] * len(row))
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                cursor.execute(query, tuple(row))
            connection.commit()
            print(f"Table '{table_name}' populated successfully from CSV.")
        else:
            print(f"Table '{table_name}' already contains data. Skipping population.")

    cursor.close()

# Ensure the database and table are created and populated with info before running the application
create_database()
create_tables()
populate_tables_from_csv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# A function to convert file paths to base64
def convert_to_base64(filepath):
    with open(filepath, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        return base64_data

# A route to grab information from the caryllrunes table and send it to the frontend
@app.route('/api/caryllRunes')
def get_caryll_runes():
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT cr.runeID, cr.runeName, cr.runeEffect, cr.filepath, crt.runeTypeName
            FROM caryllRunes cr
            JOIN caryllRunesType crt ON cr.runeTypeID = crt.runeTypeID
            ORDER BY cr.runeID
        """)

        caryll_runes = cursor.fetchall()
        
        # Convert file paths to Base64-encoded strings
        for rune in caryll_runes:
            filepath = rune['filepath']
            rune['filepath'] = convert_to_base64(filepath)
        
        return jsonify(caryll_runes)
    except mysql.connector.Error as err:
        print(f"Error fetching data from caryllrunes table: {err}")
        return jsonify({'error': 'Failed to fetch data from caryllrunes table'}), 500
    finally:
        cursor.close()

# A route to grab information from the huntertools table and send it to the frontend
@app.route('/api/hunterTools')
def get_hunter_tools():
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
	    SELECT toolID, toolName, toolDescription, bulletUse, arcaneRequirements, arcaneScaling, filepath 
	    FROM huntertools
	""")

        hunter_tools = cursor.fetchall()
        
        # Convert file paths to Base64-encoded strings
        for tool in hunter_tools:
            filepath = tool['filepath']
            tool['filepath'] = convert_to_base64(filepath)
        
        return jsonify(hunter_tools)
    except mysql.connector.Error as err:
        print(f"Error fetching data from huntertools table: {err}")
        return jsonify({'error': 'Failed to fetch data from huntertools table'}), 500
    finally:
        cursor.close()

# A route to grab all armor regardless of type and send it to the frontend
@app.route('/api/allArmorItems')
def get_all_armor_items():
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT a.armorID, a.armorName, a.armorTypeID, a.physicalDefense, a.bluntDefense, a.thrustDefense,
                   a.bloodtingeDefense, a.arcaneDefense, a.fireDefense, a.boltDefense, a.slowPoisonResistance,
                   a.fastPoisonResistance, a.frenzyResistance, a.beasthoodResistance, a.filepath, at.armorTypeName
            FROM armor a
            JOIN armorType at ON a.armorTypeID = at.armorTypeID
            ORDER BY a.armorName ASC
        """)

        armor_items = cursor.fetchall()

        # Convert file paths to Base64-encoded strings
        for armor_item in armor_items:
            filepath = armor_item['filepath']
            armor_item['filepath'] = convert_to_base64(filepath)

        return jsonify(armor_items)
    except mysql.connector.Error as err:
        print(f"Error fetching all armor items: {err}")
        return jsonify({'error': 'Failed to fetch all armor items'}), 500
    finally:
        cursor.close()

# A route to grab information from the armor table based on armor type and send it to the front end
@app.route('/api/armorByType/<int:armor_type_id>')
def get_armor_by_type(armor_type_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT a.armorID, a.armorName, a.armorTypeID, a.physicalDefense, a.bluntDefense, a.thrustDefense,
                   a.bloodtingeDefense, a.arcaneDefense, a.fireDefense, a.boltDefense, a.slowPoisonResistance,
                   a.fastPoisonResistance, a.frenzyResistance, a.beasthoodResistance, a.filepath, at.armorTypeName
            FROM armor a
            JOIN armorType at ON a.armorTypeID = at.armorTypeID
            WHERE a.armorTypeID = %s
        """, (armor_type_id,))

        armor_items = cursor.fetchall()

        # Convert file paths to Base64-encoded strings
        for armor_item in armor_items:
            filepath = armor_item['filepath']
            armor_item['filepath'] = convert_to_base64(filepath)

        return jsonify(armor_items)
    except mysql.connector.Error as err:
        print(f"Error fetching armor items by type: {err}")
        return jsonify({'error': 'Failed to fetch armor items by type'}), 500
    finally:
        cursor.close()

# A route to grab all weapons regardless of type and send it to the frontend
@app.route('/api/allWeaponItems')
def get_all_weapon_items():
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT w.weaponID, w.weaponName, w.weaponTypeID, w.physicalAttack, w.bloodAttack,
                   w.arcaneAttack, w.fireAttack, w.boltAttack, w.slowPoisonAttack, w.rapidPoisonAttack,
                   w.kinDamage, w.beastDamage, w.strengthRequirement, w.skillRequirement,
                   w.bloodtingeRequirement, w.arcaneRequirement, w.durability, w.filepath, 
                   wt.weaponTypeName 
            FROM weapon w 
            JOIN weaponType wt ON w.weaponTypeID = wt.weaponTypeID
            ORDER BY w.weaponName ASC
        """)

        weapon_items = cursor.fetchall()

        # Convert file paths to Base64-encoded strings
        for weapon_item in weapon_items:
            filepath = weapon_item['filepath']
            weapon_item['filepath'] = convert_to_base64(filepath)

        return jsonify(weapon_items)
    except mysql.connector.Error as err:
        print(f"Error fetching all weapon items: {err}")
        return jsonify({'error': 'Failed to fetch all weapon items'}), 500
    finally:
        cursor.close()

# A route to grab information from the weapoan table based on weapon type and send it to the front end
@app.route('/api/weaponsByType/<int:weapon_type_id>')
def get_weapons_by_type(weapon_type_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
	    SELECT w.weaponID, w.weaponName, w.weaponTypeID, w.physicalAttack, w.bloodAttack,
                   w.arcaneAttack, w.fireAttack, w.boltAttack, w.slowPoisonAttack, w.rapidPoisonAttack,
                   w.kinDamage, w.beastDamage, w.strengthRequirement, w.skillRequirement,
                   w.bloodtingeRequirement, w.arcaneRequirement, w.durability, w.filepath,
                   wt.weaponTypeName
            FROM weapon w
            JOIN weaponType wt ON w.weaponTypeID = wt.weaponTypeID
            WHERE w.weaponTypeID = %s
	    """, (weapon_type_id,))

        weapons = cursor.fetchall()

        # Convert file paths to Base64-encoded strings
        for weapon in weapons:
            filepath = weapon['filepath']
            weapon['filepath'] = convert_to_base64(filepath)

        return jsonify(weapons)
    except mysql.connector.Error as err:
        print(f"Error fetching weapons by type: {err}")
        return jsonify({'error': 'Failed to fetch weapons by type'}), 500
    finally:
        cursor.close()

# Close the MySQL connection when the application exits
def close_connection():
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed.")

# Register the function to be called when the application exits
atexit.register(close_connection)

if __name__ == '__main__':
    app.run(debug=True)

