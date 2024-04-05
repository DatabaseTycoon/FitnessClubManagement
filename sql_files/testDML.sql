-- Project DDL file

-- ******** Insert, Room **********
-- (Insert 5 rooms)
INSERT INTO room (roomid) VALUES
    (0), (1), (2), (3), (4);

-- ******* Insert, equipment *********
-- Add an available bike to room 1
INSERT INTO Equipment (equipmentID, roomID, equipmentName, status) VALUES
(0, 1, 'bike', 'available');

-- ******* Insert, GymClass **********
-- Add a gym class on room 1, with capacity 5.
INSERT INTO GymClass (classID, roomID, startDate, endDate, capacity) VALUES
(0, 1, '2024-09-13 13:00:00', '2024-09-13 15:00:00', 5);
