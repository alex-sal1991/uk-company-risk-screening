IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'silver') EXEC('CREATE SCHEMA silver');

DROP TABLE IF EXISTS silver.psc;
DROP TABLE IF EXISTS silver.officers;
DROP TABLE IF EXISTS silver.companies;

CREATE TABLE silver.companies (
    company_number NVARCHAR(8) PRIMARY KEY,
    company_name NVARCHAR(255) NOT NULL,
    company_status NVARCHAR(255),
    company_status_detail NVARCHAR(255),
    ro_address_line_1 NVARCHAR(255),
    ro_postal_code NVARCHAR(50),
    ro_city NVARCHAR(255),
    incorporation_date DATE,
    company_type NVARCHAR(255),
    psc_register_found BIT,
    psc_active_count INT,
    accounts_overdue BIT,
    confirmation_statement_overdue BIT,
    has_charges BIT,
    has_insolvency_history BIT,
    date_of_cessation DATE,
    jurisdiction NVARCHAR(255),
    sic_codes NVARCHAR(100)
);

CREATE TABLE silver.officers (
    officer_id NVARCHAR(50),
    appointment_id NVARCHAR(50) PRIMARY KEY,
    company_number NVARCHAR(8) NOT NULL,
    officer_name NVARCHAR(255) NOT NULL,
    officer_dob_month INT,
    officer_dob_year INT,
    officer_nationality NVARCHAR(255),
    officer_role NVARCHAR(255),
    officer_postal_code NVARCHAR(50),
    officer_locality NVARCHAR(255),
    appointed_on DATE,
    resigned_on DATE,
    CONSTRAINT fk_officers_company FOREIGN KEY (company_number)
        REFERENCES silver.companies(company_number)
);

CREATE TABLE silver.psc (
    psc_id NVARCHAR(50),
    company_number NVARCHAR(8) NOT NULL,
    psc_postal_code NVARCHAR(50),
    psc_name NVARCHAR(255) NOT NULL,
    kind NVARCHAR(255),
    natures_of_control NVARCHAR(500),
    ceased BIT,
    notified_on DATE,
    ceased_on DATE,
    CONSTRAINT fk_psc_company FOREIGN KEY (company_number)
        REFERENCES silver.companies(company_number),
    
    PRIMARY KEY(company_number, psc_id)
);