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


CREATE TABLE IF NOT EXISTS `events` (
    `event_guid` VARCHAR(75) NOT NULL,
    `venue_guid` VARCHAR(75) NOT NULL,
    `user_guid` VARCHAR(75) NOT NULL,
    `name` VARCHAR(75) NOT NULL,
    `theme` VARCHAR(255) NOT NULL,
    `slogan` VARCHAR(50) NOT NULL,
    `booths` int(5) NOT NULL,
    `conference_rooms` int(3) NOT NULL,
    `ticket_price` decimal(6,2) DEFAULT '0.00',
    `start_date` timestamp NOT NULL,
    `end_date` timestamp NOT NULL,
    `website` varchar(255) DEFAULT NULL,
    `create_date` timestamp DEFAULT CURRENT_TIMESTAMP,
    `updated_date` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY `event_guid` (`event_guid`),
    KEY `venue_guid` (`venue_guid`),
    KEY `user_guid` (`user_guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `event_users` (
    `sys_id` INT(10) AUTO_INCREMENT,
    `event_guid` VARCHAR(75) NOT NULL,
    `user_guid` VARCHAR(75) NOT NULL,
    `create_date` timestamp DEFAULT CURRENT_TIMESTAMP,
    `updated_date` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY `sys_id` (`sys_id`),
  	KEY `event_guid` (`event_guid`),
    KEY `event_user` (`event_guid`, `user_guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `venues` (
    `venue_guid` VARCHAR(75) NOT NULL,
    `name` VARCHAR(75) NOT NULL,
    `address` varchar(255) NOT NULL,
    `address2` varchar(255) DEFAULT NULL,
    `city` varchar(75) NOT NULL,
    `state` varchar(75) NOT NULL,
    `zip` varchar(25) NOT NULL,
    `booths` INT(10) NOT NULL,
    `conference_rooms` INT(10) NOT NULL,
    `website` varchar(255) DEFAULT NULL,
    `phone` varchar(25) DEFAULT NULL,
    `cost` decimal(6,2) DEFAULT '0.00',
    `is_active` int(1) DEFAULT 0,
    `create_date` timestamp DEFAULT CURRENT_TIMESTAMP,
    `updated_date` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY `venue_guid` (`venue_guid`),
    KEY `is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `transactions` (
    `transaction_guid` VARCHAR(75) NOT NULL,
    `event_guid` VARCHAR(75) NOT NULL,
    `user_guid` VARCHAR(75) NOT NULL,
    `item_description` TEXT NOT NULL,
    `payment` decimal(6,2) NOT NULL,
    `create_date` timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY `transaction_guid` (`transaction_guid`),
  	KEY `event_guid` (`event_guid`),
    KEY `event_user` (`event_guid`, `user_guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- insert the default customer
INSERT INTO `customers` (
    `cust_guid`, `name`,
    `address`, `city`, `state`, `zip`,
    `phone`, `website`, `is_active`
) VALUES (
    hex(REPLACE(uuid(), '-','')), 'NTSS', 
    '1200 Murchison Rd', 'Fayetteville', 'North Carolina', '28301',
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
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'jvargas5@broncos.uncfsu.edu', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'NTSS_ADMIN'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Ryan", '', 'De Jesus', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'rdejesus3@broncos.uncfsu.edu', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'NTSS_ADMIN'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Tyuss", '', 'Handley', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'thandley1@broncos.uncfsu.edu', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'NTSS_ADMIN'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Caileb", '', 'Carter', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'ccarter10@broncos.uncfsu.edu', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'NTSS_ADMIN'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Joe", '', 'Smack', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'joe.smack@aol.com', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'EVENT_CUSTOMER'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Observer", '', 'Smack', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'observer@mailinator.com', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'OBSERVER'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Selected", '', 'Speaker', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'selected.speaker@mailinator.com', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'SELECTED_SPEAKER'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Domain", '', 'Expert', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'domain.expert@mailinator.com', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'DOMAIN_EXPERT'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Exhibitor", '', 'Smack', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'exhibitor@mailinator.com', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'EXHIBITOR'
),
(
    hex(REPLACE(uuid(),'-','')), @cust_guid, '$argon2id$v=19$m=65536,t=3,p=4$Uajfa42Shy/FoK8DroIbPQ$l/Twf9FIXIjAkvaqXwyHujqf4ZUt+WhT9Y0h2t91vw4',
    'Mr.', "Event", '', 'Stagg', '',
    '1200 Murchison Rd', '', 'Fayetteville', 'North Carolina', '28301',
    'event.staff@mailinator.com', '910-672-1111', 'https://www.uncfsu.edu/', 1, 'EVENT_STAFF'
);


INSERT INTO `venues` (
    `venue_guid`, `name`, `address`, `city`, `state`, `zip`, `booths`, `conference_rooms`,
    `website`, `is_active`, `phone`, `cost`
) VALUES (
    '7cb27f06534249c7a57f78cbc159017b', 'MGM Grand Conference Center','3799 Las Vegas Blvd S',
    'Las Vegas','Nevada','89109',270,12,'https://mgmgrand.mgmresorts.com', 1, '800-929-1112'
);

SET @user_guid=(select user_guid from users where USER_ROLES = 'NTSS_ADMIN' order by user_id asc limit 1);

INSERT INTO `events` (
    `event_guid`, `user_guid`, `venue_guid`, `name`, `slogan`, `theme`, `website`,
    `booths`, `conference_rooms`, `ticket_price`, `start_date`, `end_date`
) VALUES (
    '1915731d79ca47a89fadc07064514889', @user_guid, '7cb27f06534249c7a57f78cbc159017b', 'La Fiesta', 'slog', 'theme', 'https://google.com',
    250, 22, 25.00, '2023-11-16', '2023-11-25'
);