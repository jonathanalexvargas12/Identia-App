-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         11.7.2-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para identia_db
CREATE DATABASE IF NOT EXISTS `identia_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci */;
USE `identia_db`;

-- Volcando estructura para tabla identia_db.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.auth_group: ~0 rows (aproximadamente)

-- Volcando estructura para tabla identia_db.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.auth_group_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla identia_db.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.auth_permission: ~24 rows (aproximadamente)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 3, 'add_permission'),
	(6, 'Can change permission', 3, 'change_permission'),
	(7, 'Can delete permission', 3, 'delete_permission'),
	(8, 'Can view permission', 3, 'view_permission'),
	(9, 'Can add group', 2, 'add_group'),
	(10, 'Can change group', 2, 'change_group'),
	(11, 'Can delete group', 2, 'delete_group'),
	(12, 'Can view group', 2, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session');

-- Volcando estructura para tabla identia_db.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.auth_user: ~5 rows (aproximadamente)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, '', '2026-02-06 01:21:41.315291', 0, '00000000', 'admin', 'admmin', 'admin@correo.com', 1, 1, '2026-02-05 04:06:25.725158'),
	(2, '', '2026-02-07 00:49:18.969268', 0, '10', 'admin', 'admin', 'admin@email.com', 1, 1, '2026-02-06 16:48:58.256056'),
	(3, '', '2026-03-12 02:10:49.000000', 0, '42917356', 'Daniel', 'Betancourt', 'josedaniel@gmail.com', 1, 1, '2026-02-07 01:10:40.000000'),
	(4, '', '2026-02-22 12:16:08.538683', 0, '42917358', 'Admin2', 'Admin2', 'ejemplocorreo@email.com', 1, 1, '2026-02-07 02:10:44.162149'),
	(5, '', '2026-03-12 03:31:59.000000', 0, '42917365', 'Admin', 'Admin', 'ejemplo@correo.com', 1, 1, '2026-02-22 14:04:52.000000');

-- Volcando estructura para tabla identia_db.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.auth_user_groups: ~0 rows (aproximadamente)

-- Volcando estructura para tabla identia_db.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.auth_user_user_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla identia_db.bitacora_asistencia
CREATE TABLE IF NOT EXISTS `bitacora_asistencia` (
  `id_pk` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del registro de asistencia.',
  `id_usuario_fk` int(8) unsigned zerofill NOT NULL COMMENT 'Relación con Usuarios.',
  `acceso` varchar(20) DEFAULT NULL COMMENT 'Tipo de acceso (Entrada).',
  `hora_acceso` time DEFAULT NULL COMMENT 'Hora exacta de entrada.',
  `salida` varchar(20) DEFAULT NULL COMMENT 'Tipo de acceso (Salida).',
  `hora_salida` time DEFAULT NULL COMMENT 'Hora exacta de salida.',
  `fecha` date DEFAULT NULL COMMENT 'Fecha del registro.',
  `estado_jornada` varchar(50) DEFAULT NULL COMMENT 'Ej: "Presente", "Tardanza".',
  PRIMARY KEY (`id_pk`),
  KEY `FK_bitacora_asistencia-usuarios` (`id_usuario_fk`),
  CONSTRAINT `FK_bitacora_asistencia-usuarios` FOREIGN KEY (`id_usuario_fk`) REFERENCES `usuarios` (`id_pk`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Registra los movimientos reales de entrada y salida de los usuarios.';

-- Volcando datos para la tabla identia_db.bitacora_asistencia: ~6 rows (aproximadamente)
INSERT INTO `bitacora_asistencia` (`id_pk`, `id_usuario_fk`, `acceso`, `hora_acceso`, `salida`, `hora_salida`, `fecha`, `estado_jornada`) VALUES
	(10, 42917365, 'Entrada', '16:00:26', 'Salida parcial', '16:01:54', '2026-02-26', 'Presente'),
	(12, 42917365, 'Entrada', '16:24:06', 'Salida', '20:00:00', '2026-02-26', 'Jornada incompleta'),
	(13, 42917365, 'Entrada', '14:28:17', 'Salida', '17:32:41', '2026-03-08', 'Presente'),
	(14, 42917365, 'Entrada', '21:46:18', 'Salida parcial', '21:48:14', '2026-03-11', 'Presente'),
	(15, 42917365, 'Entrada', '21:49:42', 'Salida parcial', '23:32:35', '2026-03-11', 'Regreso'),
	(16, 42917365, 'Entrada', '23:34:22', 'Salida', '23:35:37', '2026-03-11', 'Regreso');

-- Volcando estructura para tabla identia_db.bitacora_incidentes
CREATE TABLE IF NOT EXISTS `bitacora_incidentes` (
  `id_pk` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del incidente.',
  `novedad` varchar(100) NOT NULL DEFAULT '0' COMMENT 'Título o resumen del evento.',
  `detalles` text NOT NULL COMMENT 'Descripción amplia del suceso.',
  `hora` time NOT NULL COMMENT 'Hora del reporte.',
  `fecha` date NOT NULL COMMENT 'Fecha del reporte.',
  `ip` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_pk`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Registro de novedades o eventos fuera de lo común.';

-- Volcando datos para la tabla identia_db.bitacora_incidentes: ~0 rows (aproximadamente)

-- Volcando estructura para tabla identia_db.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.django_admin_log: ~0 rows (aproximadamente)

-- Volcando estructura para tabla identia_db.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.django_content_type: ~6 rows (aproximadamente)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'group'),
	(3, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session');

-- Volcando estructura para tabla identia_db.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.django_migrations: ~18 rows (aproximadamente)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2026-02-05 01:50:23.289978'),
	(2, 'auth', '0001_initial', '2026-02-05 01:50:31.044877'),
	(3, 'admin', '0001_initial', '2026-02-05 01:50:32.537550'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2026-02-05 01:50:32.603969'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-02-05 01:50:32.648455'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2026-02-05 01:50:33.611151'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2026-02-05 01:50:34.307863'),
	(8, 'auth', '0003_alter_user_email_max_length', '2026-02-05 01:50:34.705954'),
	(9, 'auth', '0004_alter_user_username_opts', '2026-02-05 01:50:34.748766'),
	(10, 'auth', '0005_alter_user_last_login_null', '2026-02-05 01:50:35.314196'),
	(11, 'auth', '0006_require_contenttypes_0002', '2026-02-05 01:50:35.350550'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2026-02-05 01:50:35.384627'),
	(13, 'auth', '0008_alter_user_username_max_length', '2026-02-05 01:50:35.822008'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2026-02-05 01:50:36.198904'),
	(15, 'auth', '0010_alter_group_name_max_length', '2026-02-05 01:50:36.619265'),
	(16, 'auth', '0011_update_proxy_permissions', '2026-02-05 01:50:36.673510'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2026-02-05 01:50:37.072619'),
	(18, 'sessions', '0001_initial', '2026-02-05 01:50:37.780446');

-- Volcando estructura para tabla identia_db.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.django_session: ~28 rows (aproximadamente)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('07srgw678p0ed2sma4chyygau30rwp62', '.eJxdkEluwzAMRe_CtWFosgN71eEgAkUxsFDbCjRkU_TuRVUXccrd_--TBPkJvN1WRh9t8DCb7qGJfV0RZhBHwQnucXOJM8yAfgv7GeGN1zX4eMB_lGJKHP_6Xn5lT3E7hzgX9C1EJdwjdBCyxVoW3ksgLOztPaClmkvcYC6pcgctYGvm1E4BCU-eQ_rg_QfUXDGFmPvDyv17G_T6WBDi_nbkn4YsmJf2EacmzZerI0HkR_STGrUxmrWXbjLa0KBGMRknpBqlvEqhzGUc5GCUdsLA1zfASn9y:1vnqmS:eXSwZZDNyGuLTnJuDjHxdPhgygkPUXZh2o7SQUiP5VI', '2026-02-05 05:15:48.882411'),
	('2fsqxhh9fn96ihm375ek95kt9a9m7hao', '.eJxtkMlugzAURf_F6wh5wghWTfohloeHcAN25CFdVP33GkoFkerNk-65vm_4QrA8ZlA2SGfRwGlPOibayyEbsGVWaEB4f-gEfVh0hFTp1S7On5F6wDw7G_6FJsQIoRL4WLXw9is0JixnG6RcyxpgsnuGipyVJRUVXZDj_TyvS1KVPIHPzqgMVj6dkqakXBOHHAtc0Gao3yFuu6IWvWhamTv4FewdUrNLqXnfgq5HAxf8bfe_hEwqTdutNO0ZdKM22BgrlO2pYJwzYJbonjNuWipwzzUmVBAyEkx5J1rScso05jXUw-cx69-e3z9RoY-T:1w0VpM:htb2j7fqpcUcCT3Db9-4GuWHnAyt3Hi48CJi6eOrMtc', '2026-03-12 03:31:08.000000'),
	('36eh4yzadqvblmtyhyygurs6rt5fuhem', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vzIv4:BVjAwQBXjbBebKa1NjvZPNRckvoqosAlzE8z5-I4ulA', '2026-03-08 19:32:02.000000'),
	('41yycdqlxpav1pv53o60reohffv6n4jj', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vznZW:pxW04Y2ipvOsyiEDcxjrFMHBfnsPAJnCSBCZiAZx2fM', '2026-03-10 04:15:50.000000'),
	('4kn81rj3d0jn045meyqpdsx10cqupbjb', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vzPeV:QBHpaNRPZJvFFy2TR8fceMS29tVgw3rA5nEag0Vh2bQ', '2026-03-09 02:43:23.000000'),
	('5qccok2f05stsv7pektek5b4ndevptlx', '.eJxVkMtugzAQRf_F6yjyCyismnbXD-jWGttDcAN25Aebqv9eByGFeGPpnjt3Hr8El_uMYINylgyS96wTzdvpKRu0ZQYyELo_coA-LDpiqvQreMgT-COFO86zs-HBvyFeIR2pCTFiqOhnL103y_t1ATefTViOZky5ftUMJrs1VOSsKqlAdEGNt-PkLikoeUKfnYGMVq0OlCkp18Qhx4InshlqOcZtayLJi6bB3NA_wN4hnXcpnT-3oMuzgQv-Y_e_hEyQpu1qmvcCu1Ebaoxtwfa8FVIKFJbpXgppGt7SXmrKeMvYyCiXXduwRnKhqSR__z07jQM:1vpGSo:j6hkvkMpyxcxk6deokQMgPpjv53EThal5U_jZTHSgn8', '2026-02-09 02:53:22.067755'),
	('77b2v4v1c2ctmmrub0fh6crngoi9ox87', '.eJxtkEluhDAQRe_idQt5wgRW6eQglodCOA12y0NnEeXuMYQIWoo3Jf9X_vXLXwiW-wzKBuksGjjtScfal8shG7BlVmhAeD_oBH1YdIRU6dUuztMzU3eYZ2fD_9SEGCFUBB-rFn7vr7AoNzcmLOdeSLmW1cZk9wgVOStLKiq6IMfbObZLUpU8gc_OqAxWPpySpqRcHYccC1zQ1lCfQ9xWRhw9aVqZG_gV7BNSs0uped-MrscAF_zb3v9kMqk0bV-mac-gG7XBxlihbE8F45wBs0T3nHHTUoF7rjGhgpCRYMo70ZKWU6bxmszD55H1b8_vH11TkgQ:1vtwdH:q8Wo80UKFfi-yzpyO9gb2rWcg9o9t7ncIm76u6ZluLU', '2026-02-22 00:43:31.098695'),
	('bd87h4z1fn3wtj6lnuimne9qalvvosci', '.eJxtzjsOAjEMBNC7uF6hpU3FTSwTG2ERx6vE2QZxdyQ-IgVTzpti7iC2FSF2VIZ0XJdfkYVHIUiwfgITVrdzkw4JiE3rTLRJKcr-F7O3Jv6VkxhpOWS3eSM9iF-bHLo7LKCMow9q6ni5vW9qRxpxlRqaKYRxV8I8erhBijbk8QRjsU1A:1voRCv:nPdyD3_l4wPuKRCScmfbvwgeSW3EGNScMo0OnN-1v14', '2026-02-06 20:09:33.489639'),
	('cuxwjbdm7kfxbbeao2ly0tiyfszr5ou0', '.eJxVkMtugzAQRf_F6yjyCyismnbXD-jWGttDcAN25Aebqv9eByGFeGPpnjt3Hr8El_uMYINylgyS96wTzdvpKRu0ZQYyELo_coA-LDpiqvQreMgT-COFO86zs-HBvyFeIR2pCTFiqOhnL103y_t1ATefTViOZky5ftUMJrs1VOSsKqlAdEGNt-PkLikoeUKfnYGMVq0OlCkp18Qhx4InshlqOcZtayLJi6bB3NA_wN4hnXcpnT-3oMuzgQv-Y_e_hEyQpu1qmvcCu1Ebaoxtwfa8FVIKFJbpXgppGt7SXmrKeMvYyCiXXduwRnKhqSR__z07jQM:1vp6vs:8SG2MADtDX5rmts_W43mjg7HxAaONOhMTM_4W-LXlPw', '2026-02-08 16:42:44.155358'),
	('d2pdsbzh4tkp8orp4fi1py452jj0h9p3', '.eJxVkMtugzAQRf9l1ijCD6CwatpdP6Bba2wPwQ3YkR9sqv57BUIKmeU9Zx72L9DymAltUM7CIHnPOtG8Vc_YkC0zwgD1UXCCPiw6UoIBvoLHPKE_U3zQPDsbNv6N8YbpTE2IkQIM8HO0rrvyflvQzRcTlrNMKaPdZDTZrQEqcFaVVDC6oMb7-XKXFJY8kc_OYCarVofKlJTDAkOOhSrYBVUSxf3VIOEl02ju5DdwbEiXI0qXz33Q9bnABf9x-C9DJkzT_mua94K6UZvaGNui7XkrpBQkLNO9FNI0vK17qWvGW8ZGVnPZtQ1rJBe6lvD3Dz07jQM:1vouHm:WKjG7ga5sfNA_gK31mUWG9TF0Wp-AE14z-8Nd9Dp7y0', '2026-02-08 03:12:30.231102'),
	('eby1zcsa53a4tqgap866dho0ttvinjr7', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vvhwG:q_U9mSWyffLed9JDnGa1S1sJl2qjAEuIyWh9g0bgoGg', '2026-02-26 21:26:24.000000'),
	('edgl5ugxv2kmyzwnlujingpinkim4lbb', 'e30:1vtBW4:VvYvDnE7cr7fyRRIRXIT1Bnf0YGaZXKg8rkfVYy-F5Y', '2026-02-19 22:24:56.399207'),
	('fe0j8wx6d02o3c1rrhkmwb8yd7yz1z1w', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vzNO8:DLAfpvls_Qzk9PrWq_puE_KQoC8x7vggpTryWE5JpfE', '2026-03-09 00:18:20.000000'),
	('kc23pf1uj2kbvol5wjz89wagwxpncodf', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vzZtd:IAwU055z93k2AyvmObdwb-gL5PV01AAqkIXKp_AH_JI', '2026-03-09 13:39:41.000000'),
	('kuln0s0r49yo75lqunchhrqvbmlomcky', '.eJxtkMtqwzAQRf9l1sboZQd71aYfIkbSGItYVtAjm9J_L1Vd4kC1vOdwRzOfQOG-EbqovYOZs-4ZWHJ1Q5iBHQ9OcI_BJMowA7rg9zPCO22bd_FfaGNKFP_IGwX0W29jODuUC7rm2OIfETrwTtdcMfmol9vvN33WWMtKe_EWCzn98KhtzSUGmEuq1EETdM2U2nIg4CUzaG-0_4CjO_dHlPuPVvT-HODjfj38l5IV89pOZMQk6bIYy6x1I7pJjFIpSdJxMymp7CBGNinDuBg5XzgT6jIOfFBCGqbg6xuE2YUg:1voUAp:23t5jPvcjO0DLjxc_3sc_FIHO1sxCJHFrGTdbKvbPus', '2026-02-06 23:19:35.702252'),
	('nzu5oo4ehhdxneik90ppufmisiywbvso', '.eJxtkMtuwyAQRf-FdWTxsl171bQfggYYyzQ2RDyyqfrvxa6lOFLZjLjncmeGb4LrfUGwQTlLRskH1ov27fKUDdqyABkJPQ45QR9WHTFVerWr8_zM4I7L4mz4n5oQI4aK8GvTwt_9HVdwS2PCevZiyrVsMSa7R6jIWVVSgeiCmm7nsV1SUPKMPjsDGa16OFCmpFwTxxwLXshuqM8x7isTSV40DeaGfgNHh9QcUmo-96Drs4EL_uPwv4TMkOb9yzQfBPaTNtQY24EdeCekFCgs04MU0rS8o4PUlPGOsYlRLvuuZa3kQlNJfn4BheuLHw:1vtfHq:zcGOwUZOc4Zup0Bf4i8Onkrn4wa8fwBpa1nBFXPi90Y', '2026-02-21 06:12:14.015789'),
	('ph5nsxhhqhsgtod9dt45f30uufmnhb22', '.eJxtkMlugzAURf_F6wh5wghWTfohloeHcAN25CFdVP33GkoFkerNk-65vm_4QrA8ZlA2SGfRwGlPOibayyEbsGVWaEB4f-gEfVh0hFTp1S7On5F6wDw7G_6FJsQIoRL4WLXw9is0JixnG6RcyxpgsnuGipyVJRUVXZDj_TyvS1KVPIHPzqgMVj6dkqakXBOHHAtc0Gao3yFuu6IWvWhamTv4FewdUrNLqXnfgq5HAxf8bfe_hEwqTdutNO0ZdKM22BgrlO2pYJwzYJbonjNuWipwzzUmVBAyEkx5J1rScso05jXUw-cx69-e3z9RoY-T:1w0Wr5:7RDOo8zu9xsABK8FXoVhJSrAaDdlb2qChL9PsgMq-iQ', '2026-03-12 04:36:59.000000'),
	('pp5u18zm21cznuwbme40p8jrqou25kix', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vvhrg:aXqvMJYfxOf4paMhOPKLxk6nrFFhhlTxRRI2lyeQhuw', '2026-02-26 21:21:40.000000'),
	('qg906x7d73yf2m7mdkg7vo2kkaj6nfwv', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vzPZS:4V7j78Avh5vlPHr2OfZvhO8KuBr9R17kBpeNXVRtJSU', '2026-03-09 02:38:10.000000'),
	('rdfguv1mweyxs8q12k4s80nq8qpiyedx', '.eJxVkMtugzAQRf_F6yjyCyismnbXD-jWGttDcAN25Aebqv9eByGFeGPpnjt3Hr8El_uMYINylgyS96wTzdvpKRu0ZQYyELo_coA-LDpiqvQreMgT-COFO86zs-HBvyFeIR2pCTFiqOhnL103y_t1ATefTViOZky5ftUMJrs1VOSsKqlAdEGNt-PkLikoeUKfnYGMVq0OlCkp18Qhx4InshlqOcZtayLJi6bB3NA_wN4hnXcpnT-3oMuzgQv-Y_e_hEyQpu1qmvcCu1Ebaoxtwfa8FVIKFJbpXgppGt7SXmrKeMvYyCiXXduwRnKhqSR__z07jQM:1vpGSo:j6hkvkMpyxcxk6deokQMgPpjv53EThal5U_jZTHSgn8', '2026-02-09 02:53:22.067755'),
	('sk66qx7qb1pihw26nu0y726dl32jet53', '.eJxVkMtugzAQRf9l1ijCD6CwatpdP6Bba2wPwQ3YkR9sqv57BUIKmeU9Zx72L9DymAltUM7CIHnPOtG8Vc_YkC0zwgD1UXCCPiw6UoIBvoLHPKE_U3zQPDsbNv6N8YbpTE2IkQIM8HO0rrvyflvQzRcTlrNMKaPdZDTZrQEqcFaVVDC6oMb7-XKXFJY8kc_OYCarVofKlJTDAkOOhSrYBVUSxf3VIOEl02ju5DdwbEiXI0qXz33Q9bnABf9x-C9DJkzT_mua94K6UZvaGNui7XkrpBQkLNO9FNI0vK17qWvGW8ZGVnPZtQ1rJBe6lvD3Dz07jQM:1votnq:MDlV5WBCtCL4u4G9aXs_psJ34O4TmYj3ect6wSKWBjs', '2026-02-08 02:41:34.427605'),
	('v81sp9cup2pz2f5a5abko1bdcd3odp1h', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vzL9O:gJfm3v8Q5QYkzaLaO6RrKbCJc-cGzglsLj7fGiy6tB4', '2026-03-08 21:54:58.000000'),
	('va388zbzowfqgp3gh93ds1ldgho3r8to', '.eJxVkMtugzAQRf9l1ijCD6CwatpdP6Bba2wPwQ3YkR9sqv57BUIKmeU9Zx72L9DymAltUM7CIHnPOtG8Vc_YkC0zwgD1UXCCPiw6UoIBvoLHPKE_U3zQPDsbNv6N8YbpTE2IkQIM8HO0rrvyflvQzRcTlrNMKaPdZDTZrQEqcFaVVDC6oMb7-XKXFJY8kc_OYCarVofKlJTDAkOOhSrYBVUSxf3VIOEl02ju5DdwbEiXI0qXz33Q9bnABf9x-C9DJkzT_mua94K6UZvaGNui7XkrpBQkLNO9FNI0vK17qWvGW8ZGVnPZtQ1rJBe6lvD3Dz07jQM:1vosJ6:TB61snR7ZXM8yOGHwEsBG37Ce7PW9D7762dA7UB5XZs', '2026-02-08 01:05:44.226875'),
	('x4h9m3392w4l70hw2p2begv4m5sbypm1', '.eJxtkMtuwyAQRf-FdWTxsl171bQfggYYyzQ2RDyyqfrvxa6lOFLZjLjncmeGb4LrfUGwQTlLRskH1ov27fKUDdqyABkJPQ45QR9WHTFVerWr8_zM4I7L4mz4n5oQI4aK8GvTwt_9HVdwS2PCevZiyrVsMSa7R6jIWVVSgeiCmm7nsV1SUPKMPjsDGa16OFCmpFwTxxwLXshuqM8x7isTSV40DeaGfgNHh9QcUmo-96Drs4EL_uPwv4TMkOb9yzQfBPaTNtQY24EdeCekFCgs04MU0rS8o4PUlPGOsYlRLvuuZa3kQlNJfn4BheuLHw:1vr5Fq:TOlMrIqkrsephq3re85xNTJbjl25h6F_b2yC7jbqt3I', '2026-02-14 03:19:30.737633'),
	('xfhhqcadqp10vjew3rak35q3sz5d47e8', '.eJxtkMtuwyAQRf-FdWTxsl171bQfggYYyzQ2RDyyqfrvxa6lOFLZjLjncmeGb4LrfUGwQTlLRskH1ov27fKUDdqyABkJPQ45QR9WHTFVerWr8_zM4I7L4mz4n5oQI4aK8GvTwt_9HVdwS2PCevZiyrVsMSa7R6jIWVVSgeiCmm7nsV1SUPKMPjsDGa16OFCmpFwTxxwLXshuqM8x7isTSV40DeaGfgNHh9QcUmo-96Drs4EL_uPwv4TMkOb9yzQfBPaTNtQY24EdeCekFCgs04MU0rS8o4PUlPGOsYlRLvuuZa3kQlNJfn4BheuLHw:1vu8of:axVu_tvDyy-qmVEV00FizjHIcsJ0fzKWvsH7SpqlWeo', '2026-02-22 13:44:05.162117'),
	('xw18asnx1gnss05w4jwa83cdndgyn4ay', '.eJxtkMtqwzAQRf9l1sboZQd71aYfIkbSGItYVtAjm9J_L1Vd4kC1vOdwRzOfQOG-EbqovYOZs-4ZWHJ1Q5iBHQ9OcI_BJMowA7rg9zPCO22bd_FfaGNKFP_IGwX0W29jODuUC7rm2OIfETrwTtdcMfmol9vvN33WWMtKe_EWCzn98KhtzSUGmEuq1EETdM2U2nIg4CUzaG-0_4CjO_dHlPuPVvT-HODjfj38l5IV89pOZMQk6bIYy6x1I7pJjFIpSdJxMymp7CBGNinDuBg5XzgT6jIOfFBCGqbg6xuE2YUg:1voWVD:8w1LvcpzHIUw7JQTjugjoZpemDzuCUhK-4wGpWmBIyk', '2026-02-07 01:48:47.457260'),
	('z1ege2xkmtttu59j1qkhiil7dmtthsje', '.eJxdkEluwzAMRe_CtWFosgN71eEgAkUxsFDbCjRkU_TuRVUXccrd_--TBPkJvN1WRh9t8DCb7qGJfV0RZhBHwQnucXOJM8yAfgv7GeGN1zX4eMB_lGJKHP_6Xn5lT3E7hzgX9C1EJdwjdBCyxVoW3ksgLOztPaClmkvcYC6pcgctYGvm1E4BCU-eQ_rg_QfUXDGFmPvDyv17G_T6WBDi_nbkn4YsmJf2EacmzZerI0HkR_STGrUxmrWXbjLa0KBGMRknpBqlvEqhzGUc5GCUdsLA1zfASn9y:1vnqgf:BEZ38BmSFJjsAN9xH-Tjhk-9dnRYlzd3D1HSEmViV9o', '2026-02-05 05:09:49.674347'),
	('zmfhlc9frdoic60u8ukfq6iutyc96kjw', '.eJxtkMtuwyAQRf-FdWTxMpa9atIPQTCMZRrbRDyyqfrvxa6lOFLZIJ1zuQN8E1weMxoXtHdkkLxnnVDt5YUBXZkNGQg9FjnJNSw2Yqr26ha_npV54Dx7F_6VEGLEUA1-bSx8_IEGwnKOYcp12wog-2eoyjtdUjHRBz3ez_f1SZuSJ1yzB5PR6ac3GkrKtXHIseCF7IF6HOP-VtKSN2YN3HHdxDEhNQdKzededH0N8GG9Hfm3ksmkaf8ry3uB3WiBAjhlXM-VkFKgcMz2UkhouaK9tJRxxdjIKJedalkrubBUkp9fsjWIsA:1vzl4q:beqx5J8kaPBwum4R8mtOKdxZMZ1AqcsNE36JR_rexG0', '2026-03-10 01:36:00.000000');

-- Volcando estructura para tabla identia_db.horarios_jornada
CREATE TABLE IF NOT EXISTS `horarios_jornada` (
  `id_pk` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del horario.',
  `tipo_fk` varchar(50) NOT NULL COMMENT 'Relación con Tipos_Personal.',
  `fecha` date DEFAULT NULL COMMENT 'Fecha específica de la jornada.',
  `hora_entrada` time DEFAULT NULL COMMENT 'Hora prevista de ingreso.',
  `tolerancia_entrada` varchar(10) DEFAULT NULL COMMENT 'Minutos permitidos de retraso.',
  `hora_salida` time DEFAULT NULL COMMENT 'Hora prevista de egreso.',
  `tolerancia_salida` varchar(10) DEFAULT NULL COMMENT 'Minutos de gracia para salida.',
  PRIMARY KEY (`id_pk`),
  KEY `FK_horariois_tipo` (`tipo_fk`),
  CONSTRAINT `FK_horariois_tipo` FOREIGN KEY (`tipo_fk`) REFERENCES `tipos_personal` (`id_nombre_tipo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Define las reglas de entrada y salida según el tipo de personal.';

-- Volcando datos para la tabla identia_db.horarios_jornada: ~150 rows (aproximadamente)
INSERT INTO `horarios_jornada` (`id_pk`, `tipo_fk`, `fecha`, `hora_entrada`, `tolerancia_entrada`, `hora_salida`, `tolerancia_salida`) VALUES
	(1, 'Administrativo/a', '2016-01-04', '08:00:00', '15', '12:00:00', '15'),
	(2, 'Desarrollador/a', '2016-01-04', '09:00:00', '15', '13:00:00', '15'),
	(3, 'Técnico/a', '2016-01-05', '08:00:00', '15', '12:00:00', '15'),
	(4, 'Obrero/a', '2016-01-06', '07:00:00', '10', '11:00:00', '10'),
	(5, 'Administrativo/a', '2016-02-15', '08:00:00', '15', '12:00:00', '15'),
	(6, 'Desarrollador/a', '2016-02-20', '09:00:00', '15', '13:00:00', '15'),
	(7, 'Supervisor/a', '2016-03-10', '08:00:00', '10', '12:00:00', '10'),
	(8, 'Gerente/a', '2016-04-05', '08:30:00', '20', '12:30:00', '20'),
	(9, 'Técnico/a', '2016-05-12', '08:00:00', '15', '12:00:00', '15'),
	(10, 'Obrero/a', '2016-06-20', '07:00:00', '10', '11:00:00', '10'),
	(11, 'Administrativo/a', '2017-01-09', '08:00:00', '15', '12:00:00', '15'),
	(12, 'Desarrollador/a', '2017-02-14', '09:00:00', '15', '13:00:00', '15'),
	(13, 'Técnico/a', '2017-03-22', '08:00:00', '15', '12:00:00', '15'),
	(14, 'Obrero/a', '2017-04-18', '07:00:00', '10', '11:00:00', '10'),
	(15, 'Supervisor/a', '2017-05-25', '08:00:00', '10', '12:00:00', '10'),
	(16, 'Gerente/a', '2017-06-30', '08:30:00', '20', '12:30:00', '20'),
	(17, 'Administrativo/a', '2017-08-08', '08:00:00', '15', '12:00:00', '15'),
	(18, 'Desarrollador/a', '2017-09-15', '09:00:00', '15', '13:00:00', '15'),
	(19, 'Técnico/a', '2017-10-20', '08:00:00', '15', '12:00:00', '15'),
	(20, 'Obrero/a', '2017-11-10', '07:00:00', '10', '11:00:00', '10'),
	(21, 'Administrativo/a', '2018-01-08', '08:00:00', '15', '12:00:00', '15'),
	(22, 'Desarrollador/a', '2018-02-12', '09:00:00', '15', '13:00:00', '15'),
	(23, 'Técnico/a', '2018-03-25', '08:00:00', '15', '12:00:00', '15'),
	(24, 'Obrero/a', '2018-04-30', '07:00:00', '10', '11:00:00', '10'),
	(25, 'Supervisor/a', '2018-06-05', '08:00:00', '10', '12:00:00', '10'),
	(26, 'Gerente/a', '2018-07-18', '08:30:00', '20', '12:30:00', '20'),
	(27, 'Administrativo/a', '2018-08-22', '08:00:00', '15', '12:00:00', '15'),
	(28, 'Desarrollador/a', '2018-09-10', '09:00:00', '15', '13:00:00', '15'),
	(29, 'Técnico/a', '2018-10-28', '08:00:00', '15', '12:00:00', '15'),
	(30, 'Obrero/a', '2018-11-15', '07:00:00', '10', '11:00:00', '10'),
	(31, 'Administrativo/a', '2019-01-07', '08:00:00', '15', '12:00:00', '15'),
	(32, 'Desarrollador/a', '2019-02-18', '09:00:00', '15', '13:00:00', '15'),
	(33, 'Técnico/a', '2019-03-20', '08:00:00', '15', '12:00:00', '15'),
	(34, 'Obrero/a', '2019-04-25', '07:00:00', '10', '11:00:00', '10'),
	(35, 'Supervisor/a', '2019-05-30', '08:00:00', '10', '12:00:00', '10'),
	(36, 'Gerente/a', '2019-07-08', '08:30:00', '20', '12:30:00', '20'),
	(37, 'Administrativo/a', '2019-08-15', '08:00:00', '15', '12:00:00', '15'),
	(38, 'Desarrollador/a', '2019-09-22', '09:00:00', '15', '13:00:00', '15'),
	(39, 'Técnico/a', '2019-10-30', '08:00:00', '15', '12:00:00', '15'),
	(40, 'Obrero/a', '2019-11-18', '07:00:00', '10', '11:00:00', '10'),
	(41, 'Administrativo/a', '2020-01-06', '08:00:00', '15', '12:00:00', '15'),
	(42, 'Desarrollador/a', '2020-02-17', '09:00:00', '15', '13:00:00', '15'),
	(43, 'Técnico/a', '2020-03-19', '08:00:00', '15', '12:00:00', '15'),
	(44, 'Obrero/a', '2020-04-23', '07:00:00', '10', '11:00:00', '10'),
	(45, 'Supervisor/a', '2020-05-28', '08:00:00', '10', '12:00:00', '10'),
	(46, 'Gerente/a', '2020-07-06', '08:30:00', '20', '12:30:00', '20'),
	(47, 'Administrativo/a', '2020-08-13', '08:00:00', '15', '12:00:00', '15'),
	(48, 'Desarrollador/a', '2020-09-21', '09:00:00', '15', '13:00:00', '15'),
	(49, 'Técnico/a', '2020-10-29', '08:00:00', '15', '12:00:00', '15'),
	(50, 'Obrero/a', '2020-11-16', '07:00:00', '10', '11:00:00', '10'),
	(51, 'Administrativo/a', '2021-01-04', '08:00:00', '15', '12:00:00', '15'),
	(52, 'Desarrollador/a', '2021-02-15', '09:00:00', '15', '13:00:00', '15'),
	(53, 'Técnico/a', '2021-03-18', '08:00:00', '15', '12:00:00', '15'),
	(54, 'Obrero/a', '2021-04-22', '07:00:00', '10', '11:00:00', '10'),
	(55, 'Supervisor/a', '2021-05-27', '08:00:00', '10', '12:00:00', '10'),
	(56, 'Gerente/a', '2021-07-05', '08:30:00', '20', '12:30:00', '20'),
	(57, 'Administrativo/a', '2021-08-12', '08:00:00', '15', '12:00:00', '15'),
	(58, 'Desarrollador/a', '2021-09-20', '09:00:00', '15', '13:00:00', '15'),
	(59, 'Técnico/a', '2021-10-28', '08:00:00', '15', '12:00:00', '15'),
	(60, 'Obrero/a', '2021-11-17', '07:00:00', '10', '11:00:00', '10'),
	(61, 'Administrativo/a', '2022-01-03', '08:00:00', '15', '12:00:00', '15'),
	(62, 'Desarrollador/a', '2022-02-14', '09:00:00', '15', '13:00:00', '15'),
	(63, 'Técnico/a', '2022-03-21', '08:00:00', '15', '12:00:00', '15'),
	(64, 'Obrero/a', '2022-04-21', '07:00:00', '10', '11:00:00', '10'),
	(65, 'Supervisor/a', '2022-05-26', '08:00:00', '10', '12:00:00', '10'),
	(66, 'Gerente/a', '2022-07-04', '08:30:00', '20', '12:30:00', '20'),
	(67, 'Administrativo/a', '2022-08-11', '08:00:00', '15', '12:00:00', '15'),
	(68, 'Desarrollador/a', '2022-09-19', '09:00:00', '15', '13:00:00', '15'),
	(69, 'Técnico/a', '2022-10-27', '08:00:00', '15', '12:00:00', '15'),
	(70, 'Obrero/a', '2022-11-16', '07:00:00', '10', '11:00:00', '10'),
	(71, 'Administrativo/a', '2023-01-02', '08:00:00', '15', '12:00:00', '15'),
	(72, 'Desarrollador/a', '2023-02-13', '09:00:00', '15', '13:00:00', '15'),
	(73, 'Técnico/a', '2023-03-20', '08:00:00', '15', '12:00:00', '15'),
	(74, 'Obrero/a', '2023-04-20', '07:00:00', '10', '11:00:00', '10'),
	(75, 'Supervisor/a', '2023-05-25', '08:00:00', '10', '12:00:00', '10'),
	(76, 'Gerente/a', '2023-07-03', '08:30:00', '20', '12:30:00', '20'),
	(77, 'Administrativo/a', '2023-08-10', '08:00:00', '15', '12:00:00', '15'),
	(78, 'Desarrollador/a', '2023-09-18', '09:00:00', '15', '13:00:00', '15'),
	(79, 'Técnico/a', '2023-10-26', '08:00:00', '15', '12:00:00', '15'),
	(80, 'Obrero/a', '2023-11-15', '07:00:00', '10', '11:00:00', '10'),
	(81, 'Administrativo/a', '2024-01-08', '08:00:00', '15', '12:00:00', '15'),
	(82, 'Desarrollador/a', '2024-02-12', '09:00:00', '15', '13:00:00', '15'),
	(83, 'Técnico/a', '2024-03-18', '08:00:00', '15', '12:00:00', '15'),
	(84, 'Obrero/a', '2024-04-22', '07:00:00', '10', '11:00:00', '10'),
	(85, 'Supervisor/a', '2024-05-27', '08:00:00', '10', '12:00:00', '10'),
	(86, 'Gerente/a', '2024-07-04', '08:30:00', '20', '12:30:00', '20'),
	(87, 'Administrativo/a', '2024-08-12', '08:00:00', '15', '12:00:00', '15'),
	(88, 'Desarrollador/a', '2024-09-19', '09:00:00', '15', '13:00:00', '15'),
	(89, 'Técnico/a', '2024-10-28', '08:00:00', '15', '12:00:00', '15'),
	(90, 'Obrero/a', '2024-11-14', '07:00:00', '10', '11:00:00', '10'),
	(91, 'Administrativo/a', '2025-01-06', '08:00:00', '15', '12:00:00', '15'),
	(92, 'Desarrollador/a', '2025-02-17', '09:00:00', '15', '13:00:00', '15'),
	(93, 'Técnico/a', '2025-03-19', '08:00:00', '15', '12:00:00', '15'),
	(94, 'Obrero/a', '2025-04-21', '07:00:00', '10', '11:00:00', '10'),
	(95, 'Supervisor/a', '2025-05-26', '08:00:00', '10', '12:00:00', '10'),
	(96, 'Gerente/a', '2025-07-03', '08:30:00', '20', '12:30:00', '20'),
	(97, 'Administrativo/a', '2025-08-11', '08:00:00', '15', '12:00:00', '15'),
	(98, 'Desarrollador/a', '2025-09-18', '09:00:00', '15', '13:00:00', '15'),
	(99, 'Técnico/a', '2025-10-27', '08:00:00', '15', '12:00:00', '15'),
	(100, 'Obrero/a', '2025-11-13', '07:00:00', '10', '11:00:00', '10'),
	(101, 'Administrativo/a', '2026-01-06', '08:00:00', '15', '12:00:00', '15'),
	(102, 'Desarrollador/a', '2026-01-07', '09:00:00', '15', '13:00:00', '15'),
	(103, 'Técnico/a', '2026-01-08', '08:00:00', '15', '12:00:00', '15'),
	(104, 'Obrero/a', '2026-01-09', '07:00:00', '10', '11:00:00', '10'),
	(105, 'Supervisor/a', '2026-01-10', '08:00:00', '10', '12:00:00', '10'),
	(106, 'Gerente/a', '2026-01-13', '08:30:00', '20', '12:30:00', '20'),
	(107, 'Administrativo/a', '2026-01-14', '08:00:00', '15', '12:00:00', '15'),
	(108, 'Desarrollador/a', '2026-01-15', '09:00:00', '15', '13:00:00', '15'),
	(109, 'Técnico/a', '2026-01-16', '08:00:00', '15', '12:00:00', '15'),
	(110, 'Obrero/a', '2026-01-17', '07:00:00', '10', '11:00:00', '10'),
	(111, 'Administrativo/a', '2026-01-20', '08:00:00', '15', '12:00:00', '15'),
	(112, 'Desarrollador/a', '2026-01-21', '09:00:00', '15', '13:00:00', '15'),
	(113, 'Técnico/a', '2026-01-22', '08:00:00', '15', '12:00:00', '15'),
	(114, 'Obrero/a', '2026-01-23', '07:00:00', '10', '11:00:00', '10'),
	(115, 'Supervisor/a', '2026-01-24', '08:00:00', '10', '12:00:00', '10'),
	(116, 'Gerente/a', '2026-01-27', '08:30:00', '20', '12:30:00', '20'),
	(117, 'Administrativo/a', '2026-01-28', '08:00:00', '15', '12:00:00', '15'),
	(118, 'Desarrollador/a', '2026-01-29', '09:00:00', '15', '13:00:00', '15'),
	(119, 'Técnico/a', '2026-01-30', '08:00:00', '15', '12:00:00', '15'),
	(120, 'Obrero/a', '2026-01-31', '07:00:00', '10', '11:00:00', '10'),
	(121, 'Administrativo/a', '2026-02-03', '08:00:00', '15', '12:00:00', '15'),
	(122, 'Desarrollador/a', '2026-02-04', '09:00:00', '15', '13:00:00', '15'),
	(123, 'Técnico/a', '2026-02-05', '08:00:00', '15', '12:00:00', '15'),
	(124, 'Obrero/a', '2026-02-06', '07:00:00', '10', '11:00:00', '10'),
	(125, 'Supervisor/a', '2026-02-07', '08:00:00', '10', '12:00:00', '10'),
	(126, 'Gerente/a', '2026-02-10', '08:30:00', '20', '12:30:00', '20'),
	(127, 'Administrativo/a', '2026-02-11', '08:00:00', '15', '12:00:00', '15'),
	(128, 'Desarrollador/a', '2026-02-12', '09:00:00', '15', '13:00:00', '15'),
	(129, 'Técnico/a', '2026-02-13', '08:00:00', '15', '12:00:00', '15'),
	(130, 'Obrero/a', '2026-02-14', '07:00:00', '10', '11:00:00', '10'),
	(131, 'Administrativo/a', '2026-02-17', '08:00:00', '15', '12:00:00', '15'),
	(132, 'Desarrollador/a', '2026-02-18', '09:00:00', '15', '13:00:00', '15'),
	(133, 'Técnico/a', '2026-02-19', '08:00:00', '15', '12:00:00', '15'),
	(134, 'Obrero/a', '2026-02-20', '07:00:00', '10', '11:00:00', '10'),
	(135, 'Supervisor/a', '2026-02-21', '08:00:00', '10', '12:00:00', '10'),
	(136, 'Gerente/a', '2026-02-24', '08:30:00', '20', '12:30:00', '20'),
	(137, 'Administrativo/a', '2026-02-25', '08:00:00', '15', '12:00:00', '15'),
	(138, 'Desarrollador/a', '2026-02-26', '09:00:00', '15', '13:00:00', '15'),
	(139, 'Técnico/a', '2026-02-27', '08:00:00', '15', '12:00:00', '15'),
	(140, 'Obrero/a', '2026-02-28', '07:00:00', '10', '11:00:00', '10'),
	(141, 'Administrativo/a', '2026-03-03', '08:00:00', '15', '12:00:00', '15'),
	(142, 'Desarrollador/a', '2026-03-04', '09:00:00', '15', '13:00:00', '15'),
	(143, 'Técnico/a', '2026-03-05', '08:00:00', '15', '12:00:00', '15'),
	(144, 'Obrero/a', '2026-03-06', '07:00:00', '10', '11:00:00', '10'),
	(145, 'Supervisor/a', '2026-03-07', '08:00:00', '10', '12:00:00', '10'),
	(146, 'Gerente/a', '2026-03-10', '08:30:00', '20', '12:30:00', '20'),
	(147, 'Administrativo/a', '2026-03-11', '08:00:00', '15', '12:00:00', '15'),
	(148, 'Desarrollador/a', '2026-03-12', '09:00:00', '15', '13:00:00', '15'),
	(149, 'Técnico/a', '2026-03-13', '08:00:00', '15', '12:00:00', '15'),
	(150, 'Obrero/a', '2026-03-14', '07:00:00', '10', '11:00:00', '10');

-- Volcando estructura para tabla identia_db.notificaciones_leidas
CREATE TABLE IF NOT EXISTS `notificaciones_leidas` (
  `id_pk` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID único del registro de lectura.',
  `id_usuario_fk` int(8) unsigned NOT NULL COMMENT 'ID del usuario que leyó la notificación (FK -> usuarios.id_pk).',
  `id_incidente_fk` int(11) NOT NULL COMMENT 'ID del incidente/notificación leída (FK -> bitacora_incidentes.id_pk).',
  `fecha_lectura` datetime DEFAULT current_timestamp() COMMENT 'Fecha y hora en que se marcó como leída.',
  PRIMARY KEY (`id_pk`),
  UNIQUE KEY `unique_usuario_incidente` (`id_usuario_fk`,`id_incidente_fk`) COMMENT 'Un usuario no puede tener el mismo incidente marcado como leído más de una vez.',
  KEY `idx_notificaciones_usuario` (`id_usuario_fk`) COMMENT 'Índice para búsquedas por usuario.',
  KEY `idx_notificaciones_incidente` (`id_incidente_fk`) COMMENT 'Índice para búsquedas por incidente.',
  CONSTRAINT `fk_notificaciones_incidente` FOREIGN KEY (`id_incidente_fk`) REFERENCES `bitacora_incidentes` (`id_pk`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_notificaciones_usuario` FOREIGN KEY (`id_usuario_fk`) REFERENCES `usuarios` (`id_pk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Registro de notificaciones leídas por cada usuario.';

-- Volcando datos para la tabla identia_db.notificaciones_leidas: ~0 rows (aproximadamente)

-- Volcando estructura para tabla identia_db.rostros_usuarios
CREATE TABLE IF NOT EXISTS `rostros_usuarios` (
  `id_pk` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del rostro.',
  `id_usuario_fk` int(8) unsigned zerofill NOT NULL DEFAULT 00000000 COMMENT 'Relación con Usuarios.',
  `vector_facial` blob NOT NULL COMMENT 'Datos biométricos del rostro.',
  PRIMARY KEY (`id_pk`),
  KEY `FK_rostros_usuarios` (`id_usuario_fk`),
  CONSTRAINT `FK_rostros_usuarios` FOREIGN KEY (`id_usuario_fk`) REFERENCES `usuarios` (`id_pk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Almacena la biometría facial para el reconocimiento.';

-- Volcando datos para la tabla identia_db.rostros_usuarios: ~1 rows (aproximadamente)
INSERT INTO `rostros_usuarios` (`id_pk`, `id_usuario_fk`, `vector_facial`) VALUES
	(10, 42917365, _binary 0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000);

-- Volcando estructura para tabla identia_db.tipos_personal
CREATE TABLE IF NOT EXISTS `tipos_personal` (
  `id_nombre_tipo` varchar(50) NOT NULL DEFAULT 'AUTO_INCREMENT' COMMENT 'Identificador único del tipo.',
  PRIMARY KEY (`id_nombre_tipo`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Clasifica a los usuarios por categorías (ej. Administrativos, Operativos). Está relacionada con Usuarios y Horarios_Jornada para definir perfiles y sus reglas de tiempo.';

-- Volcando datos para la tabla identia_db.tipos_personal: ~6 rows (aproximadamente)
INSERT INTO `tipos_personal` (`id_nombre_tipo`) VALUES
	('Administrativo/a'),
	('Desarrollador/a'),
	('Gerente/a'),
	('Obrero/a'),
	('Supervisor/a'),
	('Técnico/a');

-- Volcando estructura para tabla identia_db.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_pk` int(8) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID único del usuario.',
  `tipo_fk` varchar(50) NOT NULL DEFAULT '0' COMMENT 'Relación con Tipos_Personal.',
  `cedula` varchar(8) NOT NULL DEFAULT '0' COMMENT 'Documento de identidad (Único).',
  `nombres` varchar(100) NOT NULL DEFAULT '0' COMMENT 'Nombres del usuario.',
  `apellidos` varchar(100) NOT NULL DEFAULT '0' COMMENT 'Apellidos del usuario.',
  `direccion_habitacional` text NOT NULL COMMENT 'Dirección de vivienda.',
  `correo` varchar(150) NOT NULL DEFAULT '' COMMENT 'Email institucional o personal.',
  `numero` varchar(20) NOT NULL DEFAULT '' COMMENT 'Teléfono de contacto.',
  `estado` varchar(20) NOT NULL DEFAULT '' COMMENT 'Ej. Activo, Inactivo, Suspendido.',
  `area_trabajo` varchar(100) NOT NULL DEFAULT '' COMMENT 'Departamento o sección.',
  `rol` varchar(50) NOT NULL DEFAULT '' COMMENT 'Rol dentro del sistema.',
  PRIMARY KEY (`id_pk`),
  KEY `FK_usuarios_tipo` (`tipo_fk`),
  CONSTRAINT `FK_usuarios_tipo` FOREIGN KEY (`tipo_fk`) REFERENCES `tipos_personal` (`id_nombre_tipo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=42917381 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Almacena la información personal y laboral básica de cada individuo.';

-- Volcando datos para la tabla identia_db.usuarios: ~25 rows (aproximadamente)
INSERT INTO `usuarios` (`id_pk`, `tipo_fk`, `cedula`, `nombres`, `apellidos`, `direccion_habitacional`, `correo`, `numero`, `estado`, `area_trabajo`, `rol`) VALUES
	(42917356, 'Desarrollador/a', '11111111', 'Daniel', 'Betancourt', 'Av. Principal, Caracas', 'daniel.betancourt@identia.com', '04120000001', 'Activo', 'Desarrollo', 'Desarrollador'),
	(42917357, 'Técnico/a', '22222222', 'María', 'González', 'Calle 5, Maracaibo', 'maria.gonzalez@identia.com', '04120000002', 'Activo', 'Técnico', 'Técnico'),
	(42917358, 'Administrativo/a', '33333333', 'Carlos', 'López', 'Av. Libertador, Valencia', 'carlos.lopez@identia.com', '04120000003', 'Activo', 'Administración', 'Administrativo'),
	(42917359, 'Obrero/a', '44444444', 'Ana', 'Rodríguez', 'Calle Central, Barquisimeto', 'ana.rodriguez@identia.com', '04120000004', 'Activo', 'Producción', 'Obrero'),
	(42917360, 'Supervisor/a', '55555555', 'Pedro', 'Martínez', 'Av. Industrial, Puerto La Cruz', 'pedro.martinez@identia.com', '04120000005', 'Activo', 'Supervisión', 'Supervisor'),
	(42917361, 'Gerente/a', '66666666', 'Laura', 'Fernández', 'Urbanización El Parque, Ciudad Bolívar', 'laura.fernandez@identia.com', '04120000006', 'Activo', 'Gerencia', 'Gerente'),
	(42917362, 'Desarrollador/a', '77777777', 'José', 'Hernández', 'Sector Norte, San Cristóbal', 'jose.hernandez@identia.com', '04120000007', 'Activo', 'Desarrollo', 'Desarrollador'),
	(42917363, 'Técnico/a', '88888888', 'Sofia', 'Díaz', 'Av. Universidad, Mérida', 'sofia.diaz@identia.com', '04120000008', 'Activo', 'Técnico', 'Técnico'),
	(42917364, 'Administrativo/a', '99999999', 'Miguel', 'Torres', 'Calle Comercio, Barinas', 'miguel.torres@identia.com', '04120000009', 'Activo', 'Administración', 'Administrativo'),
	(42917365, 'Desarrollador/a', '10101010', 'Admin', 'Admin', 'Dirección Principal', 'admin@identia.com', '04120000010', 'Activo', 'Desarrollo', 'Desarrollador'),
	(42917366, 'Obrero/a', '12121212', 'Carmen', 'Ramos', 'Sector Industrial, Cumaná', 'carmen.ramos@identia.com', '04120000011', 'Activo', 'Producción', 'Obrero'),
	(42917367, 'Técnico/a', '13131313', 'Roberto', 'García', 'Av. Bolívar, Puerto Ordaz', 'roberto.garcia@identia.com', '04120000012', 'Activo', 'Técnico', 'Técnico'),
	(42917368, 'Supervisor/a', '14141414', 'Patricia', 'Morales', 'Urbanización Los Samanes, Acarigua', 'patricia.morales@identia.com', '04120000013', 'Activo', 'Supervisión', 'Supervisor'),
	(42917369, 'Desarrollador/a', '15151515', 'Luis', 'Ramírez', 'Calle Principal, Guanare', 'luis.ramirez@identia.com', '04120000014', 'Activo', 'Desarrollo', 'Desarrollador'),
	(42917370, 'Administrativo/a', '16161616', 'Isabel', 'Castillo', 'Av. Libertador, San Juan de los Morros', 'isabel.castillo@identia.com', '04120000015', 'Inactivo', 'Administración', 'Administrativo'),
	(42917371, 'Obrero/a', '17171717', 'Francisco', 'Vega', 'Sector Este, Valle de la Pascua', 'francisco.vega@identia.com', '04120000016', 'Activo', 'Producción', 'Obrero'),
	(42917372, 'Gerente/a', '18181818', 'Elena', 'Mendoza', 'Urbanización Villa Rosa, Punto Fijo', 'elena.mendoza@identia.com', '04120000017', 'Activo', 'Gerencia', 'Gerente'),
	(42917373, 'Técnico/a', '19191919', 'Andrés', 'Navarro', 'Calle Norte, Carúpano', 'andres.navarro@identia.com', '04120000018', 'Activo', 'Técnico', 'Técnico'),
	(42917374, 'Desarrollador/a', '20202020', 'Verónica', 'Herrera', 'Av. Industrial, Tocuyito', 'veronica.herrera@identia.com', '04120000019', 'Activo', 'Desarrollo', 'Desarrollador'),
	(42917375, 'Administrativo/a', '21212121', 'Ricardo', 'Aguilar', 'Sector Centro, Araure', 'ricardo.aguilar@identia.com', '04120000020', 'Activo', 'Administración', 'Administrativo'),
	(42917376, 'Obrero/a', '22222223', 'Diana', 'Rivas', 'Av. Principal, Chivacoa', 'diana.rivas@identia.com', '04120000021', 'Suspendido', 'Producción', 'Obrero'),
	(42917377, 'Supervisor/a', '23232323', 'Oscar', 'Medina', 'Urbanización Buenos Aires, Tinaquillo', 'oscar.medina@identia.com', '04120000022', 'Activo', 'Supervisión', 'Supervisor'),
	(42917378, 'Desarrollador/a', '24242424', 'Natalia', 'Sosa', 'Calle Vargas, Guacara', 'natalia.sosa@identia.com', '04120000023', 'Activo', 'Desarrollo', 'Desarrollador'),
	(42917379, 'Técnico/a', '25252525', 'Gabriel', 'Pérez', 'Sector Industrial, Nirgua', 'gabriel.perez@identia.com', '04120000024', 'Activo', 'Técnico', 'Técnico'),
	(42917380, 'Gerente/a', '26262626', 'Andrea', 'Ruiz', 'Av. Libertador, Santa Rita', 'andrea.ruiz@identia.com', '04120000025', 'Activo', 'Gerencia', 'Gerente');

-- Volcando estructura para tabla identia_db.usuarios_administrativos
CREATE TABLE IF NOT EXISTS `usuarios_administrativos` (
  `id_pk` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID de la cuenta.',
  `id_usuario_fk` int(8) unsigned DEFAULT NULL COMMENT 'Relación con Usuarios.',
  `password` varchar(255) DEFAULT NULL COMMENT 'Contraseña (siempre hasheada).',
  PRIMARY KEY (`id_pk`),
  KEY `FK_usuarios_administrativos_usuarios` (`id_usuario_fk`),
  CONSTRAINT `FK_usuarios_administrativos_usuarios` FOREIGN KEY (`id_usuario_fk`) REFERENCES `usuarios` (`id_pk`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Credenciales para que ciertos usuarios accedan al sistema.';

-- Volcando datos para la tabla identia_db.usuarios_administrativos: ~3 rows (aproximadamente)
INSERT INTO `usuarios_administrativos` (`id_pk`, `id_usuario_fk`, `password`) VALUES
	(3, 42917356, 'pbkdf2_sha256$1200000$SSsjddvCyrcCmjMrlqQkLR$p++Fn6dLxhSUGvaqW4r8YVq6ZRKw72ZStLKcoQjD/3c='),
	(6, 42917365, 'pbkdf2_sha256$870000$A6ptpS0kObwTywdV3o6Jo2$aj9qU97slndPlBaOVxkY2y9h0TufdvH3dhe0byTFgKo='),
	(7, 42917366, '0432883e9d9b84d55f110caa400646c4cdcb5b0661ef225bc550ba6251fde179');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
