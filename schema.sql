BEGIN;
CREATE TABLE `ctfweb_game` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(200) NOT NULL,
    `start_time` datetime NOT NULL,
    `end_time` datetime NOT NULL,
    `active` integer NOT NULL
)
;
CREATE TABLE `ctfweb_category` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `game_id` integer NOT NULL,
    `name` varchar(200) NOT NULL
)
;
ALTER TABLE `ctfweb_category` ADD CONSTRAINT `game_id_refs_id_32ce16d` FOREIGN KEY (`game_id`) REFERENCES `ctfweb_game` (`id`);
CREATE TABLE `ctfweb_challenge` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `game_id` integer NOT NULL,
    `category_id` integer NOT NULL,
    `name` varchar(200) NOT NULL,
    `description` varchar(2000) NOT NULL,
    `points` integer NOT NULL,
    `active` integer NOT NULL,
    `key` varchar(200) NOT NULL
)
;
ALTER TABLE `ctfweb_challenge` ADD CONSTRAINT `game_id_refs_id_5f7f8137` FOREIGN KEY (`game_id`) REFERENCES `ctfweb_game` (`id`);
ALTER TABLE `ctfweb_challenge` ADD CONSTRAINT `category_id_refs_id_b67a2957` FOREIGN KEY (`category_id`) REFERENCES `ctfweb_category` (`id`);
CREATE TABLE `ctfweb_hint` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `game_id` integer NOT NULL,
    `challenge_id` integer NOT NULL,
    `text` varchar(2000) NOT NULL,
    `active` integer NOT NULL
)
;
ALTER TABLE `ctfweb_hint` ADD CONSTRAINT `game_id_refs_id_916d18c` FOREIGN KEY (`game_id`) REFERENCES `ctfweb_game` (`id`);
ALTER TABLE `ctfweb_hint` ADD CONSTRAINT `challenge_id_refs_id_3e292e12` FOREIGN KEY (`challenge_id`) REFERENCES `ctfweb_challenge` (`id`);
CREATE TABLE `ctfweb_competitor` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `game_id` integer NOT NULL,
    `user_id` integer NOT NULL UNIQUE,
    `display_name` varchar(200) NOT NULL,
    `affiliation` varchar(200),
    `url` varchar(200),
    `bad_keys` integer NOT NULL,
    `points` integer NOT NULL,
    `active` integer NOT NULL
)
;
ALTER TABLE `ctfweb_competitor` ADD CONSTRAINT `game_id_refs_id_15c0d77d` FOREIGN KEY (`game_id`) REFERENCES `ctfweb_game` (`id`);
ALTER TABLE `ctfweb_competitor` ADD CONSTRAINT `user_id_refs_id_68a0de3d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `ctfweb_solved` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `game_id` integer NOT NULL,
    `competitor_id` integer NOT NULL,
    `challenge_id` integer NOT NULL,
    `points` integer NOT NULL,
    `time` datetime NOT NULL
)
;
ALTER TABLE `ctfweb_solved` ADD CONSTRAINT `game_id_refs_id_3f38fd9a` FOREIGN KEY (`game_id`) REFERENCES `ctfweb_game` (`id`);
ALTER TABLE `ctfweb_solved` ADD CONSTRAINT `competitor_id_refs_id_bf34a508` FOREIGN KEY (`competitor_id`) REFERENCES `ctfweb_competitor` (`id`);
ALTER TABLE `ctfweb_solved` ADD CONSTRAINT `challenge_id_refs_id_dd307314` FOREIGN KEY (`challenge_id`) REFERENCES `ctfweb_challenge` (`id`);
CREATE INDEX `ctfweb_category_7b333d1e` ON `ctfweb_category` (`game_id`);
CREATE INDEX `ctfweb_challenge_7b333d1e` ON `ctfweb_challenge` (`game_id`);
CREATE INDEX `ctfweb_challenge_42dc49bc` ON `ctfweb_challenge` (`category_id`);
CREATE INDEX `ctfweb_hint_7b333d1e` ON `ctfweb_hint` (`game_id`);
CREATE INDEX `ctfweb_hint_dd8bebce` ON `ctfweb_hint` (`challenge_id`);
CREATE INDEX `ctfweb_competitor_7b333d1e` ON `ctfweb_competitor` (`game_id`);
CREATE INDEX `ctfweb_solved_7b333d1e` ON `ctfweb_solved` (`game_id`);
CREATE INDEX `ctfweb_solved_6f4d7c0c` ON `ctfweb_solved` (`competitor_id`);
CREATE INDEX `ctfweb_solved_dd8bebce` ON `ctfweb_solved` (`challenge_id`);
COMMIT;
