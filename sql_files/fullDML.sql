-- Inserting ContactInfo data
INSERT INTO ContactInfo (firstName, lastName, email, phoneNumber)
VALUES
    ('John', 'Doe', 'johndoe@example.com', '1234567890'),
    ('Jane', 'Smith', 'janesmith@example.com', '9876543210'),
    ('Michael', 'Johnson', 'michaeljohnson@example.com', '5551112222');

-- Inserting Administrator data
INSERT INTO Administrator (adminID)
VALUES (1);

-- Inserting Trainer data
INSERT INTO Trainer (trainerID)
VALUES (1),
       (2);

-- Inserting Staff data
INSERT INTO Staff (contactID)
VALUES (1),
       (2),
       (3);

-- Inserting IsAdmin data
INSERT INTO IsAdmin (adminID, staffID)
VALUES (1, 1);

-- Inserting IsTrainer data
INSERT INTO IsTrainer (trainerID, staffID)
VALUES (1, 2),
       (2, 3);

-- Inserting Room data (3x roooms)
INSERT INTO Room DEFAULT VALUES;
INSERT INTO Room DEFAULT VALUES;
INSERT INTO Room DEFAULT VALUES;

-- Inserting Equipment data
INSERT INTO Equipment (roomID, status, equipmentName)
VALUES
    (1, 'Working', 'Treadmill'),
    (2, 'Working', 'Dumbbells'),
    (3, 'Working', 'Elliptical'),
    (1, 'Maintenance', 'Dumbbells'),
    (1, 'Out of Order', 'Elliptical');

-- Inserting GymClass data
INSERT INTO GymClass (roomID, startDate, endDate, capacity)
VALUES
    (1, '2024-04-10 10:00:00', '2024-04-10 11:00:00', 10),
    (1, '2024-04-12 12:00:00', '2024-04-12 13:00:00', 15);

-- Inserting PersonalInfo data
INSERT INTO PersonalInfo (dateOfBirth, contactID, emergencyContactID)
VALUES
    ('1990-01-15', 1, 3),
    ('1985-06-20', 2, 1);

-- Inserting BillingInfo data
INSERT INTO BillingInfo (billingAddress, memEndDate, creditCardNumber, creditCardExpiryDate, creditCardSecurityCode)
VALUES
    ('123 Main St, Cityville, USA', '2024-12-31', 12345678, '2026-01-01', 123),
    ('456 Oak Ave, Townsville, USA', '2024-11-30', 87654321, '2025-12-01', 456);

-- Inserting MemberInfo data
INSERT INTO MemberInfo (personalInfoID, billingInfoID)
VALUES
    (1, 1),
    (2, 2);

-- Inserting Statistic data
INSERT INTO Statistic (memberid, "type", "value")
VALUES
    (1, 'weight', '100kg'),
    (1, 'bench', '425lbs'),
    (2, 'weight', '100kg'),
    (2, 'bench', '100lbs');

-- Inserting FitnessGoal data
INSERT INTO FitnessGoal (memberID, type, description, isAchieved, targetDate)
VALUES
    (1, 'typeA', 'typADesc', true, '2024-05-01'),
    (2, 'typeB',  'typeBDesc', false, '2024-04-30');


-- Inserting Runs data
INSERT INTO Runs (trainerID, classID)
VALUES (1, 1),
       (2, 2);

-- Inserting Runs data
INSERT INTO Participates (memberID, classID)
VALUES (1, 1),
       (2, 2);
