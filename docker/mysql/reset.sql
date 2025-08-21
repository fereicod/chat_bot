-- Disable foreign key checks to drop tables
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS conversations;

SET FOREIGN_KEY_CHECKS = 1;
