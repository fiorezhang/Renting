USE RENTING;
ALTER TABLE `full` ADD id INT;
ALTER TABLE `full` CHANGE id id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;
SELECT COUNT(*) FROM `full` WHERE `id` IN (SELECT MAX(`id`) FROM `full` WHERE `community` != 'NULL' AND `area` != 'NULL' AND `floor` != 'NULL' GROUP BY `community`, `area`, `floor`);

CREATE TABLE IF NOT EXISTS `distinct`(
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
ALTER TABLE `distinct` ADD id INT;
INSERT INTO `distinct` SELECT * FROM `full` WHERE `id` IN (SELECT MAX(`id`) FROM `full` WHERE `community` != 'NULL' AND `area` != 'NULL' AND `floor` != 'NULL' GROUP BY `community`, `area`, `floor`);
