-- DDL file for FitnessClubManagement
-- Can't name admin (keyword)
CREATE TABLE Administrator (
	adminID serial PRIMARY KEY
);

CREATE TABLE Trainer (
	trainerID serial PRIMARY KEY
);

-- Name is a keyword
CREATE TABLE PersonName (
	nameID serial PRIMARY KEY,
	firstName varchar(20) NOT NULL,
	lastName varchar(20) NOT NULL
);

CREATE TABLE Staff (
	staffID serial PRIMARY KEY,
	nameID int REFERENCES PersonName (nameID),
	email varchar(60) NOT NULL,
	phoneNumber varchar(11)
);

CREATE TABLE IsAdmin (
	adminID int REFERENCES Administrator (adminID),
	staffID int REFERENCES Staff (staffID),
	PRIMARY KEY (adminID, staffID)
);

CREATE TABLE IsTrainer (
	trainerID int REFERENCES Trainer (trainerID),
	staffID int REFERENCES Staff (staffID),
	PRIMARY KEY (trainerID, staffID)
);

CREATE TABLE Room (
	roomID serial PRIMARY KEY
);

CREATE TABLE Equipment (
	equipmentID serial PRIMARY KEY,
	roomID int REFERENCES Room (roomID),
	status varchar(15),
	equipmentName varchar(30) -- Name is a keyword
);

-- Class is a keyword
CREATE TABLE GymClass (
	classID serial PRIMARY KEY,
	roomID int REFERENCES Room (roomID),
	startDate timestamp NOT NULL,
	endDate timestamp NOT NULL,
	capacity int
);


CREATE TABLE Runs (
	trainerID int REFERENCES Trainer (trainerID),
	classID int REFERENCES GymClass (classID),
	PRIMARY KEY (trainerID, classID)
);


-- Should statistic be "value", and "type" where type is a string element of {HeartRate, BloodPressure, Weight, Height}?
CREATE TABLE Statistic (
	statID serial PRIMARY KEY,
	HeartRate int,
	BloodPressure int,
	Weight int,
	Height int,
	statDate date NOT NULL
);

-- What if we reused statistic to be able to check any metric? I.e. target metric? Statistic could contain metric actually
CREATE TABLE FitnessGoal (
	goalID serial PRIMARY KEY,
	isAchieved bool NOT NULL,
	targetDate date NOT NULL,
	targetWeight int NOT NULL
);

CREATE TABLE EmergencyContact (
	emergencyContactID serial PRIMARY KEY,
	nameID int REFERENCES PersonName (nameID),
	dateOfBirth date,
	-- Contact info reuse with staff (maybe that's okay though)
	email varchar(60) NOT NULL,
	phoneNumber varchar(11)
);

CREATE TABLE PersonalInfo (
	personalInfoID serial PRIMARY KEY,
	nameID int REFERENCES PersonName (nameID),
	emergencyContactID int REFERENCES EmergencyContact (emergencyContactID),
	-- Why store DoB?... -> What if name became contact info (used by three tables now): FName, LName, email, number.
	dateOfBirth date,
	-- Contact info reuse with staff+EContact (maybe that's okay though)
	email varchar(60) NOT NULL,
	phoneNumber varchar(11)
);

CREATE TABLE BillingInfo (
	billingInfoID serial PRIMARY KEY,
	billingAddress varchar(60) NOT NULL,
	memEndDate date NOT NULL,
	creditCardNumber int NOT NULL,
	creditCardExpiryDate date NOT NULL,
	creditCardSecurityCode int
);

-- Member is a keyword. Not putting phone number + e-mail since it's already in personal info.
CREATE TABLE MemberInfo(
	memberInfo serial PRIMARY KEY,
	personalInfoID int REFERENCES PersonalInfo (personalInfoID),
	billingInfoID int REFERENCES BillingInfo (billingInfoID),
	statID int REFERENCES Statistic (statID),
	goalID int REFERENCES FitnessGoal (goalID)
);