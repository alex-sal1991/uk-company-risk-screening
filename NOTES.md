Cohort: companies incorporated 1 January – 14 January 2025
SIC codes: 82990, 96090, 64209
Status: all statuses

companies  (1 row per company)    key: company_number
- company_number
- company_name
- company_status
- company_status_detail
- ro_address_line_1
- ro_postal_code
- ro_city
- company_incorporation_date (company creation date)
- company_type
- psc_register_found
- psc_active_count
- accounts_overdue
- confirmation_statement_overdue
- has_charges
- has_insolvency_history
- date_of_cessation
- jurisdiction
- sic_codes

officers   (1 row per company–officer appointment)    key: company_number + officer_id + officer_role
- officer_id
- officer_name
- officer_dob_month
- officer_dob_year
- officer_nationality
- officer_role
- officer_postal_code
- officer_locality
- appointed_on
- resigned_on
- company_number = ["links"]["self"] split on "/" an extract the company number on the second item in the list 


psc        (1 row per company–PSC)    key: company_number + psc_id
- psc_name
- kind
- notified_on
- ceased
- company_number = ["links"]["self"] split on "/" an extract the company number on the second item in the list
