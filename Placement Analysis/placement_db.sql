CREATE DATABASE placement_db;
USE placement_db;
CREATE TABLE students(
id INT PRIMARY KEY,
cgpa FLOAT,
internships INT,
certifications INT,
aptitude_score INT,
communication_score INT,
placed VARCHAR(10)
);
SELECT * FROM placementdata;
SELECT COUNT(*) FROM placementdata;
SELECT AVG(cgpa) FROM placementdata;
SELECT PlacementStatus,COUNT(*)
FROM placementdata
GROUP BY  PlacementStatus;
SELECT
ROUND(
SUM(CASE WHEN PlacementStatus='Placed'
THEN 1 ELSE 0 END)
/
COUNT(*)*100,2
)
AS Placement_Percentage
FROM placementdata;