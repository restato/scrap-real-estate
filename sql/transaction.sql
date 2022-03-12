CREATE TABLE `transaction` (
    `area_code` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `transaction_amount` INT(20) COLLATE utf8_bin NOT NULL,
    `year_of_construction` INT(10) COLLATE utf8_bin NOT NULL,
    `transaction_year` INT(10) COLLATE utf8_bin NOT NULL,
    `legal_dong` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `apt_name` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `transaction_month` INT(10) COLLATE utf8_bin NOT NULL,
    `transaction_day` INT(10) COLLATE utf8_bin NOT NULL,
    `dedicated_area` DECIMAL(10,5) COLLATE utf8_bin NOT NULL,
    `jibun` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `floor` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `date_of_cause_for_dismantled` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `is_dismantled` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `si` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `gu` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `sigungu` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `area` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `dedicated_area_level` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `amount_per_area` VARCHAR(255) COLLATE utf8_bin NOT NULL,
    `transaction_date` DATE COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
;