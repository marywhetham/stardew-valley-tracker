-- Locations
INSERT INTO locations(location_name) VALUES ('string');

-- Items
INSERT INTO items(item_name, location_id, season, selling_price, level_available) VALUES ('item1', 2, ARRAY[1], 1.5, 1);

-- Obelisk
INSERT INTO obelisks(obelisk_name, cost) VALUES ('earth', 500000);
INSERT INTO obelisk_building_materials(obelisk_id, item_id) VALUES (1, 2);