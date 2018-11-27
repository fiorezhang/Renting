USE `RENTING`;
CREATE TABLE IF NOT EXISTS `sample`(
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
ALTER TABLE `sample` ADD id INT;
INSERT INTO `sample` SELECT * FROM `distinct`
WHERE `class` = '出租房'
AND `province` != 'NULL'
AND `city` != 'NULL'
AND `community` != 'NULL'
AND `money` != 'NULL'
AND `area` != 'NULL'
; #2100000

#SET @@GLOBAL.sql_mode="NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION";

#SELECT * FROM `sample` WHERE `area` LIKE '%平%' OR `area` LIKE '%m%' ORDER BY RAND() LIMIT 100;
#UPDATE `sample` SET `area` = REPLACE(`area`, '平米', '');
#UPDATE `sample` SET `area` = REPLACE(`area`, '暂无信息', '0');
#SELECT * FROM `sample` WHERE `area` = '';
#DELETE FROM `sample` WHERE `area` = '';
ALTER TABLE `sample` MODIFY COLUMN `area` INT;
#SELECT * FROM `sample` LIMIT 1 OFFSET 10921;
DELETE FROM `sample` WHERE `area` > 1000;
SELECT * FROM `sample` ORDER BY `area` DESC LIMIT 100;

ALTER TABLE `sample` MODIFY COLUMN `money` INT;
#DELETE FROM `sample` WHERE CONVERT(`money`, DECIMAL) > 100000;
#SELECT * FROM `sample` LIMIT 1 OFFSET 347334;
DELETE FROM `sample` WHERE `money` > 100000;
SELECT * FROM `sample` ORDER BY `money` DESC LIMIT 100;
DELETE FROM `sample` WHERE `money`/`area` > 1000;

SELECT COUNT(*) FROM `sample`; #2160000
SELECT * FROM `sample` ORDER BY RAND() LIMIT 10;

SELECT COUNT(*) FROM `sample` WHERE `decoration` != 'NULL'; #1470000
SELECT COUNT(*) FROM `sample` WHERE `id` IN (SELECT MAX(`id`) FROM `sample` GROUP BY `community`); #320000