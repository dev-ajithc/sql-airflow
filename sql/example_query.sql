-- Example SQL query that will be scheduled
SELECT 
    current_timestamp as execution_time,
    count(*) as total_count
FROM 
    your_table
WHERE 
    created_at >= current_date - interval '1 day';
