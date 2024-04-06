-- Test queries manually found to determine how to program functions implementing them for DB features.
-- "Test cases" Based on test DML at the time of writing them


-- Goal of this query: Get all "available" rooms with a given startTimeTest, and endTimeTest.
--  Method: If there exists a class where either test times is between the class startTime and endTime, its room is filtered out.
--  Query 1: Excludes room 1 with a start time in bound

--  Query 2: Excludes room 1 with an end time in bound

--  Query 3: Does not exclude room 1 (start, end, out of bound)