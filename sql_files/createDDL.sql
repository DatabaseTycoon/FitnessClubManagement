-- DDL file for FitnessClubManagement
-- Can't name admin (keyword)
CREATE TABLE ContactInfo (
	ContactID serial PRIMARY KEY,
	firstName text NOT NULL,
	lastName text NOT NULL,
	email varchar(60) NOT NULL,
	phoneNumber varchar(11)
);

CREATE TABLE Administrator (
	adminID serial PRIMARY KEY
);

CREATE TABLE Trainer (
	trainerID serial PRIMARY KEY
);

CREATE TABLE Staff (
	staffID serial PRIMARY KEY,
	contactID int REFERENCES ContactInfo (contactID)
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

CREATE TABLE PersonalInfo (
	personalInfoID serial PRIMARY KEY,
    dateOfBirth date,
	contactID int REFERENCES ContactInfo (contactID),
	emergencyContactID int REFERENCES ContactInfo (contactID)
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
	billingInfoID int REFERENCES BillingInfo (billingInfoID)
);

CREATE TABLE Runs (
	trainerID int,
	classID int,
	PRIMARY KEY (trainerID, classID),
    FOREIGN KEY (classID) REFERENCES GymClass ON DELETE CASCADE,
    FOREIGN KEY (trainerID) REFERENCES Trainer ON DELETE CASCADE
);

CREATE TABLE Participates (
	memberID int,
	classID int,
	PRIMARY KEY (memberID, classID),
    FOREIGN KEY (classID) REFERENCES GymClass ON DELETE CASCADE,
    FOREIGN KEY (memberID) REFERENCES MemberInfo ON DELETE CASCADE
);

-- Should statistic be "value", and "type" where type is a string element of {HeartRate, BloodPressure, Weight, Height}?
CREATE TABLE Statistic (
	memberID int REFERENCES MemberInfo (memberInfo),
	type TEXT,
	value TEXT,
	PRIMARY KEY (memberID, type)
);

-- What if we reused statistic to be able to check any metric? I.e. target metric? Statistic could contain metric actually
CREATE TABLE FitnessGoal (
	memberID int REFERENCES MemberInfo (memberInfo),
	type TEXT,
	description TEXT,
	isAchieved bool NOT NULL,
	targetDate date NOT NULL,
	PRIMARY KEY (memberID, type)
);
