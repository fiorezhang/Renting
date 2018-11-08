USE RENTING;
#DROP TABLE `rent`;
CREATE TABLE IF NOT EXISTS `rent`(
	`company`    varchar(40),
    `class`      varchar(40),
    `date`       varchar(40),
    `time`       varchar(40),
    `province`   varchar(40),
    `city`       varchar(40),
    `district`   varchar(40),
    `community`  varchar(40),
    `money`      varchar(40),
    `room`       varchar(40),
    `area`       varchar(40),
    `direction`  varchar(40),
    `floor`      varchar(40),
    `decoration` varchar(40),
    `old`        varchar(40)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
SELECT * FROM `rent` LIMIT 100;
SELECT `company`, COUNT(*) AS `count_company` FROM `rent` GROUP BY `company` ORDER BY `count_company` DESC;
SELECT `province`, COUNT(*) AS `count_province` FROM `rent` GROUP BY `province` ORDER BY `count_province` DESC;
SELECT `city`, COUNT(*) AS `count_city` FROM `rent` GROUP BY `city` ORDER BY `count_city` DESC;
SELECT `district`, COUNT(*) AS `count_district` FROM `rent` WHERE `district` != 'NULL' GROUP BY `district` ORDER BY `count_district` DESC LIMIT 100;
SELECT `money`, COUNT(*) AS `count_money` FROM `rent` WHERE `money` != 'NULL' AND `money` != 'NOVA' GROUP BY `money` ORDER BY `money` DESC LIMIT 100;