-- create the databases
CREATE DATABASE IF NOT EXISTS ntss;

USE ntss;

-- create schemas needed
--- Customers table
CREATE TABLE IF NOT EXISTS `customers` (
    `cust_id` int(11) NOT NULL AUTO_INCREMENT,
    `cust_guid` VARCHAR(75) NOT NULL,
    `name` varchar(255) NOT NULL,
    `address` varchar(255) NOT NULL,
    `address2` varchar(255) DEFAULT NULL,
    `city` varchar(75) NOT NULL,
    `state` varchar(75) NOT NULL,
    `zip` varchar(25) NOT NULL,
    `email` varchar(255) DEFAULT NULL,
    `phone` varchar(25) DEFAULT NULL,
    `website` varchar(255) DEFAULT NULL,
    `is_active` int(1) DEFAULT NULL,
    `create_date` timestamp DEFAULT CURRENT_TIMESTAMP,
    `updated_date` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`cust_id`),
    UNIQUE KEY `cust_guid` (`cust_guid`),
    KEY `is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `users` (
    `user_id` int(11) NOT NULL AUTO_INCREMENT,
    `user_guid` VARCHAR(75) NOT NULL,
    `cust_guid` VARCHAR(75) DEFAULT NULL,
    `password` VARCHAR(255) NOT NULL,
    `prefix_name` varchar(25) DEFAULT NULL,
    `first_name` varchar(255) NOT NULL,
    `middle_name` varchar(255) DEFAULT NULL,
    `last_name` varchar(255) NOT NULL,
    `suffix_name` varchar(25) DEFAULT NULL,
    `address` varchar(255) NOT NULL,
    `address2` varchar(255) DEFAULT NULL,
    `city` varchar(75) NOT NULL,
    `state` varchar(75) NOT NULL,
    `zip` varchar(25) NOT NULL,
    `email` varchar(255) NOT NULL,
    `phone` varchar(25) DEFAULT NULL,
    `website` varchar(255) DEFAULT NULL,
    `is_active` int(1) DEFAULT 0,
    `verification_code` varchar(255) DEFAULT NULL,
    `user_roles` VARCHAR(255) DEFAULT 'OBSERVER',
    `create_date` timestamp DEFAULT CURRENT_TIMESTAMP,
    `updated_date` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`user_id`),
    UNIQUE KEY `user_guid` (`user_guid`),
    UNIQUE KEY `user_email` (`email`),
    KEY `is_active` (`is_active`),
    KEY `user_roles` (`user_roles`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- insert the default customer
INSERT INTO `customers` (
    `cust_guid`, `name`,
    `address`, `city`, `state`, `zip`,
    `phone`, `website`, `is_active`
) VALUES (
    hex(REPLACE(uuid(), '-','')), 'NTSS', 
    '1200 Murchison Rd', 'Fayetteville', 'NC', '28301',
    '910-672-1111', 'https://www.uncfsu.edu/', 1
);

SET @cust_guid=(select cust_guid from customers order by cust_id asc limit 1);

INSERT INTO `users` (
    `user_guid`, `cust_guid`, `password`,
    `prefix_name`,`first_name`,`middle_name`,`last_name`,`suffix_name`,
    `address`, `address2`, `city`, `state`, `zip`,
    `email`, `phone`, `website`, `is_active`, `user_roles`
) VALUES (
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Jose'", '', 'Vargas', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'NC', '28301',
    'jvargas5@broncos.uncfsu.edu', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'NTSS_ADMIN'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Ryan", '', 'De Jesus', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'NC', '28301',
    'rdejesus3@broncos.uncfsu.edu', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'NTSS_ADMIN'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Tyuss", '', 'Handley', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'NC', '28301',
    'thandley1@broncos.uncfsu.edu', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'NTSS_ADMIN'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Caileb", '', 'Carter', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'NC', '28301',
    'ccarter10@broncos.uncfsu.edu', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'NTSS_ADMIN'
);
