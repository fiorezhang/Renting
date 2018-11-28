USE RENTING;
CREATE TABLE IF NOT EXISTS `gps`(
    `province`   varchar(40),
    `city`       varchar(40),
    `district`   varchar(40),
    `community`  varchar(40)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
DROP TABLE `gps`;
INSERT INTO `gps` SELECT `province`, `city`, `district`, `community` FROM `distinct` WHERE `id` IN (SELECT MAX(`id`) FROM `distinct` WHERE `community` != 'NULL' AND `area` != 'NULL' AND `money` != 'NULL' GROUP BY `city`, `community`);
ALTER TABLE `gps` ADD `address` VARCHAR(40);
ALTER TABLE `gps` ADD `lat` FLOAT;
ALTER TABLE `gps` ADD `lng` FLOAT;
SELECT * FROM `gps` WHERE `address` IS NOT NULL LIMIT 2000;