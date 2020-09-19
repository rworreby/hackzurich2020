DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS truck;
DROP TABLE IF EXISTS fahrt;
DROP TABLE IF EXISTS pickup;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    token TEXT NOT NULL
);

CREATE TABLE truck (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    current_load INTEGER NOT NULL,
    max_load INTEGER NOT NULL,
    home_location_log REAL NOT NULL,
    home_location_lat REAL NOT NULL,
    current_location_log REAL NOT NULL,
    current_location_lat REAL NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE fahrt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    truck_id INTEGER NOT NULL,
    load INTEGER NOT NULL,
    start_location_log REAL NOT NULL,
    start_location_lat REAL NOT NULL,
    end_location_log REAL NOT NULL,
    end_location_lat REAL NOT NULL,
    FOREIGN KEY (truck_id) REFERENCES truck(id)
);

CREATE TABLE pickup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    load INTEGER NOT NULL,
    notes TEXT,
    type TEXT,
    start_location_log REAL NOT NULL,
    start_location_lat REAL NOT NULL,
    end_location_log REAL,
    end_location_lat REAL,
    FOREIGN KEY (truck_id) REFERENCES truck(id)
);