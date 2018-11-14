ALTER TABLE `full` MODIFY `date` DATE;
ALTER TABLE `full` MODIFY `time` TIME;
ALTER TABLE `full` ADD `datetime` DATETIME;
UPDATE `full` SET `datetime` = CONCAT(`date`, ' ', `time`);