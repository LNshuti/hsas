SELECT
  SUM(total_days_of_care) AS total_days_of_care_sum,
  AVG(total_days_of_care) AS total_days_of_care_avg,
  MIN(total_days_of_care) AS total_days_of_care_min,
  MAX(total_days_of_care) AS total_days_of_care_max,
  
  SUM(total_charges) AS total_charges_sum,
  AVG(total_charges) AS total_charges_avg,
  MIN(total_charges) AS total_charges_min,
  MAX(total_charges) AS total_charges_max,
  
  SUM(total_cases) AS total_cases_sum,
  AVG(total_cases) AS total_cases_avg,
  MIN(total_cases) AS total_cases_min,
  MAX(total_cases) AS total_cases_max
FROM (
  SELECT
    CAST(total_days_of_care AS INTEGER) AS total_days_of_care,
    CAST(total_charges AS INTEGER) AS total_charges,
    CAST(total_cases AS INTEGER) AS total_cases
  FROM
    hsa_data
  WHERE
    total_days_of_care > 0
) AS filtered_data;
