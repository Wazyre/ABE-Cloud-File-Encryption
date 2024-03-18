DROP DATABASE IF EXISTS `aws_abe_encrytion`;
CREATE DATABASE `aws_abe_encrytion`;
USE `aws_abe_encrytion`;

SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;

CREATE TABLE `aws_user` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `year` varchar(2) NOT NULL,
  `department` varchar(50) NOT NULL,
  `position` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `aws_user` VALUES (1,'Alice','cn029!38r4yc09@@h','aliced@uoregon.edu','10','Physics','Professor');
INSERT INTO `aws_user` VALUES (2,'Bob','nv203#98vr#V79y29v8','bobs2@gmail.com','1','Computer Science','Teaching Assistant');
INSERT INTO `aws_user` VALUES (3,'Candice','#*V&v38V*&v0#&^VB','candicel@hotline.com','4','Business','Graduate Student');
INSERT INTO `aws_user` VALUES (4,'Donald','CN##@#C23cn#C*37c3','donaldt@osu.edu','3','Human Phys','Undergraduate Student');
INSERT INTO `aws_user` VALUES (5,'Eve','H&^AHS&A^868as8dS','evef@uoregon.edu','5','Journalism','Professor');
