SELECT 
    HOUR(Timestamp) AS Hour_Of_Day, 
    COUNT(*) AS Fraud_Count
FROM transactions
WHERE Is_Fraud = 1
GROUP BY HOUR(Timestamp)
ORDER BY Fraud_Count DESC
LIMIT 0, 1000;
