import pyspark.sql.functions as f

kpis = [
            {'name': 'crimes_per_type',
             'query': """SELECT crimeType, count(*) AS count FROM crimes GROUP BY crimeType"""},
              {'name': 'crimes_by_location',
             'query': """SELECT districtName, count(*) AS count 
             FROM crimes GROUP BY districtName ORDER BY count(*) ASC"""},
              {'name': 'crimes_per_month_per_area',
             'query': """SELECT month, count(crimeId) as crimes, districtName 
             FROM crimes GROUP BY month, districtName  ORDER BY month"""},
              {'name': 'cumul_crimes_per_type_over_time',
             'query': """SELECT month, crimeType, sum(crimes) 
             OVER (PARTITION BY crimeType ORDER BY month ASC) AS crimes 
             FROM (SELECT month, count(crimeId) as crimes, crimeType 
                FROM crimes GROUP BY month, crimeType) 
             ORDER BY month"""},
              {'name': 'guilty_per_type',
             'query': """SELECT CASE 
                WHEN lastOutcome IN ("Offender given penalty notice", "Suspect charged", "Offender given a caution") 
                THEN TRUE ELSE FALSE END AS guiltyFound, crimeType, count(*)
             FROM crimes GROUP BY crimeType, guiltyFound"""}
        ]

extract_file_name_udf = f.udf(lambda path: " ".join(path.split("/")[-1].split("-")[2:-1]))
