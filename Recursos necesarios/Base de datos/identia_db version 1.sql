-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         12.1.2-MariaDB - MariaDB Server
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.11.0.7065
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
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla identia_db.auth_user: ~4 rows (aproximadamente)
REPLACE INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, '', '2026-02-06 01:21:41.315291', 0, '00000000', 'admin', 'admmin', 'admin@correo.com', 1, 1, '2026-02-05 04:06:25.725158'),
	(2, '', '2026-02-07 00:49:18.969268', 0, '10', 'admin', 'admin', 'admin@email.com', 1, 1, '2026-02-06 16:48:58.256056'),
	(3, '', '2026-02-19 20:25:22.030635', 0, '42917356', 'Daniel', 'Betancourt', 'josedaniel@gmail.com', 1, 1, '2026-02-07 01:10:40.238259'),
	(4, '', '2026-02-13 22:09:51.708035', 0, '42917358', 'Admin2', 'Admin2', 'ejemplocorreo@email.com', 1, 1, '2026-02-07 02:10:44.162149');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Registra los movimientos reales de entrada y salida de los usuarios.';

-- Volcando datos para la tabla identia_db.bitacora_asistencia: ~0 rows (aproximadamente)

-- Volcando estructura para tabla identia_db.bitacora_incidentes
CREATE TABLE IF NOT EXISTS `bitacora_incidentes` (
  `id_pk` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del incidente.',
  `novedad` varchar(100) NOT NULL DEFAULT '0' COMMENT 'Título o resumen del evento.',
  `detalles` text NOT NULL COMMENT 'Descripción amplia del suceso.',
  `hora` time NOT NULL COMMENT 'Hora del reporte.',
  `fecha` date NOT NULL COMMENT 'Fecha del reporte.',
  PRIMARY KEY (`id_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Registro de novedades o eventos fuera de lo común.';

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
REPLACE INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
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
REPLACE INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
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

-- Volcando datos para la tabla identia_db.django_session: ~13 rows (aproximadamente)
REPLACE INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('07srgw678p0ed2sma4chyygau30rwp62', '.eJxdkEluwzAMRe_CtWFosgN71eEgAkUxsFDbCjRkU_TuRVUXccrd_--TBPkJvN1WRh9t8DCb7qGJfV0RZhBHwQnucXOJM8yAfgv7GeGN1zX4eMB_lGJKHP_6Xn5lT3E7hzgX9C1EJdwjdBCyxVoW3ksgLOztPaClmkvcYC6pcgctYGvm1E4BCU-eQ_rg_QfUXDGFmPvDyv17G_T6WBDi_nbkn4YsmJf2EacmzZerI0HkR_STGrUxmrWXbjLa0KBGMRknpBqlvEqhzGUc5GCUdsLA1zfASn9y:1vnqmS:eXSwZZDNyGuLTnJuDjHxdPhgygkPUXZh2o7SQUiP5VI', '2026-02-05 05:15:48.882411'),
	('5qccok2f05stsv7pektek5b4ndevptlx', '.eJxVkMtugzAQRf_F6yjyCyismnbXD-jWGttDcAN25Aebqv9eByGFeGPpnjt3Hr8El_uMYINylgyS96wTzdvpKRu0ZQYyELo_coA-LDpiqvQreMgT-COFO86zs-HBvyFeIR2pCTFiqOhnL103y_t1ATefTViOZky5ftUMJrs1VOSsKqlAdEGNt-PkLikoeUKfnYGMVq0OlCkp18Qhx4InshlqOcZtayLJi6bB3NA_wN4hnXcpnT-3oMuzgQv-Y_e_hEyQpu1qmvcCu1Ebaoxtwfa8FVIKFJbpXgppGt7SXmrKeMvYyCiXXduwRnKhqSR__z07jQM:1vpGSo:j6hkvkMpyxcxk6deokQMgPpjv53EThal5U_jZTHSgn8', '2026-02-09 02:53:22.067755'),
	('bd87h4z1fn3wtj6lnuimne9qalvvosci', '.eJxtzjsOAjEMBNC7uF6hpU3FTSwTG2ERx6vE2QZxdyQ-IgVTzpti7iC2FSF2VIZ0XJdfkYVHIUiwfgITVrdzkw4JiE3rTLRJKcr-F7O3Jv6VkxhpOWS3eSM9iF-bHLo7LKCMow9q6ni5vW9qRxpxlRqaKYRxV8I8erhBijbk8QRjsU1A:1voRCv:nPdyD3_l4wPuKRCScmfbvwgeSW3EGNScMo0OnN-1v14', '2026-02-06 20:09:33.489639'),
	('cuxwjbdm7kfxbbeao2ly0tiyfszr5ou0', '.eJxVkMtugzAQRf_F6yjyCyismnbXD-jWGttDcAN25Aebqv9eByGFeGPpnjt3Hr8El_uMYINylgyS96wTzdvpKRu0ZQYyELo_coA-LDpiqvQreMgT-COFO86zs-HBvyFeIR2pCTFiqOhnL103y_t1ATefTViOZky5ftUMJrs1VOSsKqlAdEGNt-PkLikoeUKfnYGMVq0OlCkp18Qhx4InshlqOcZtayLJi6bB3NA_wN4hnXcpnT-3oMuzgQv-Y_e_hEyQpu1qmvcCu1Ebaoxtwfa8FVIKFJbpXgppGt7SXmrKeMvYyCiXXduwRnKhqSR__z07jQM:1vp6vs:8SG2MADtDX5rmts_W43mjg7HxAaONOhMTM_4W-LXlPw', '2026-02-08 16:42:44.155358'),
	('d2pdsbzh4tkp8orp4fi1py452jj0h9p3', '.eJxVkMtugzAQRf9l1ijCD6CwatpdP6Bba2wPwQ3YkR9sqv57BUIKmeU9Zx72L9DymAltUM7CIHnPOtG8Vc_YkC0zwgD1UXCCPiw6UoIBvoLHPKE_U3zQPDsbNv6N8YbpTE2IkQIM8HO0rrvyflvQzRcTlrNMKaPdZDTZrQEqcFaVVDC6oMb7-XKXFJY8kc_OYCarVofKlJTDAkOOhSrYBVUSxf3VIOEl02ju5DdwbEiXI0qXz33Q9bnABf9x-C9DJkzT_mua94K6UZvaGNui7XkrpBQkLNO9FNI0vK17qWvGW8ZGVnPZtQ1rJBe6lvD3Dz07jQM:1vouHm:WKjG7ga5sfNA_gK31mUWG9TF0Wp-AE14z-8Nd9Dp7y0', '2026-02-08 03:12:30.231102'),
	('edgl5ugxv2kmyzwnlujingpinkim4lbb', 'e30:1vtBW4:VvYvDnE7cr7fyRRIRXIT1Bnf0YGaZXKg8rkfVYy-F5Y', '2026-02-19 22:24:56.399207'),
	('kuln0s0r49yo75lqunchhrqvbmlomcky', '.eJxtkMtqwzAQRf9l1sboZQd71aYfIkbSGItYVtAjm9J_L1Vd4kC1vOdwRzOfQOG-EbqovYOZs-4ZWHJ1Q5iBHQ9OcI_BJMowA7rg9zPCO22bd_FfaGNKFP_IGwX0W29jODuUC7rm2OIfETrwTtdcMfmol9vvN33WWMtKe_EWCzn98KhtzSUGmEuq1EETdM2U2nIg4CUzaG-0_4CjO_dHlPuPVvT-HODjfj38l5IV89pOZMQk6bIYy6x1I7pJjFIpSdJxMymp7CBGNinDuBg5XzgT6jIOfFBCGqbg6xuE2YUg:1voUAp:23t5jPvcjO0DLjxc_3sc_FIHO1sxCJHFrGTdbKvbPus', '2026-02-06 23:19:35.702252'),
	('rdfguv1mweyxs8q12k4s80nq8qpiyedx', '.eJxVkMtugzAQRf_F6yjyCyismnbXD-jWGttDcAN25Aebqv9eByGFeGPpnjt3Hr8El_uMYINylgyS96wTzdvpKRu0ZQYyELo_coA-LDpiqvQreMgT-COFO86zs-HBvyFeIR2pCTFiqOhnL103y_t1ATefTViOZky5ftUMJrs1VOSsKqlAdEGNt-PkLikoeUKfnYGMVq0OlCkp18Qhx4InshlqOcZtayLJi6bB3NA_wN4hnXcpnT-3oMuzgQv-Y_e_hEyQpu1qmvcCu1Ebaoxtwfa8FVIKFJbpXgppGt7SXmrKeMvYyCiXXduwRnKhqSR__z07jQM:1vpGSo:j6hkvkMpyxcxk6deokQMgPpjv53EThal5U_jZTHSgn8', '2026-02-09 02:53:22.067755'),
	('sk66qx7qb1pihw26nu0y726dl32jet53', '.eJxVkMtugzAQRf9l1ijCD6CwatpdP6Bba2wPwQ3YkR9sqv57BUIKmeU9Zx72L9DymAltUM7CIHnPOtG8Vc_YkC0zwgD1UXCCPiw6UoIBvoLHPKE_U3zQPDsbNv6N8YbpTE2IkQIM8HO0rrvyflvQzRcTlrNMKaPdZDTZrQEqcFaVVDC6oMb7-XKXFJY8kc_OYCarVofKlJTDAkOOhSrYBVUSxf3VIOEl02ju5DdwbEiXI0qXz33Q9bnABf9x-C9DJkzT_mua94K6UZvaGNui7XkrpBQkLNO9FNI0vK17qWvGW8ZGVnPZtQ1rJBe6lvD3Dz07jQM:1votnq:MDlV5WBCtCL4u4G9aXs_psJ34O4TmYj3ect6wSKWBjs', '2026-02-08 02:41:34.427605'),
	('va388zbzowfqgp3gh93ds1ldgho3r8to', '.eJxVkMtugzAQRf9l1ijCD6CwatpdP6Bba2wPwQ3YkR9sqv57BUIKmeU9Zx72L9DymAltUM7CIHnPOtG8Vc_YkC0zwgD1UXCCPiw6UoIBvoLHPKE_U3zQPDsbNv6N8YbpTE2IkQIM8HO0rrvyflvQzRcTlrNMKaPdZDTZrQEqcFaVVDC6oMb7-XKXFJY8kc_OYCarVofKlJTDAkOOhSrYBVUSxf3VIOEl02ju5DdwbEiXI0qXz33Q9bnABf9x-C9DJkzT_mua94K6UZvaGNui7XkrpBQkLNO9FNI0vK17qWvGW8ZGVnPZtQ1rJBe6lvD3Dz07jQM:1vosJ6:TB61snR7ZXM8yOGHwEsBG37Ce7PW9D7762dA7UB5XZs', '2026-02-08 01:05:44.226875'),
	('x4h9m3392w4l70hw2p2begv4m5sbypm1', '.eJxtkMtuwyAQRf-FdWTxsl171bQfggYYyzQ2RDyyqfrvxa6lOFLZjLjncmeGb4LrfUGwQTlLRskH1ov27fKUDdqyABkJPQ45QR9WHTFVerWr8_zM4I7L4mz4n5oQI4aK8GvTwt_9HVdwS2PCevZiyrVsMSa7R6jIWVVSgeiCmm7nsV1SUPKMPjsDGa16OFCmpFwTxxwLXshuqM8x7isTSV40DeaGfgNHh9QcUmo-96Drs4EL_uPwv4TMkOb9yzQfBPaTNtQY24EdeCekFCgs04MU0rS8o4PUlPGOsYlRLvuuZa3kQlNJfn4BheuLHw:1vr5Fq:TOlMrIqkrsephq3re85xNTJbjl25h6F_b2yC7jbqt3I', '2026-02-14 03:19:30.737633'),
	('xw18asnx1gnss05w4jwa83cdndgyn4ay', '.eJxtkMtqwzAQRf9l1sboZQd71aYfIkbSGItYVtAjm9J_L1Vd4kC1vOdwRzOfQOG-EbqovYOZs-4ZWHJ1Q5iBHQ9OcI_BJMowA7rg9zPCO22bd_FfaGNKFP_IGwX0W29jODuUC7rm2OIfETrwTtdcMfmol9vvN33WWMtKe_EWCzn98KhtzSUGmEuq1EETdM2U2nIg4CUzaG-0_4CjO_dHlPuPVvT-HODjfj38l5IV89pOZMQk6bIYy6x1I7pJjFIpSdJxMymp7CBGNinDuBg5XzgT6jIOfFBCGqbg6xuE2YUg:1voWVD:8w1LvcpzHIUw7JQTjugjoZpemDzuCUhK-4wGpWmBIyk', '2026-02-07 01:48:47.457260'),
	('z1ege2xkmtttu59j1qkhiil7dmtthsje', '.eJxdkEluwzAMRe_CtWFosgN71eEgAkUxsFDbCjRkU_TuRVUXccrd_--TBPkJvN1WRh9t8DCb7qGJfV0RZhBHwQnucXOJM8yAfgv7GeGN1zX4eMB_lGJKHP_6Xn5lT3E7hzgX9C1EJdwjdBCyxVoW3ksgLOztPaClmkvcYC6pcgctYGvm1E4BCU-eQ_rg_QfUXDGFmPvDyv17G_T6WBDi_nbkn4YsmJf2EacmzZerI0HkR_STGrUxmrWXbjLa0KBGMRknpBqlvEqhzGUc5GCUdsLA1zfASn9y:1vnqgf:BEZ38BmSFJjsAN9xH-Tjhk-9dnRYlzd3D1HSEmViV9o', '2026-02-05 05:09:49.674347');

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Define las reglas de entrada y salida según el tipo de personal.';

-- Volcando datos para la tabla identia_db.horarios_jornada: ~0 rows (aproximadamente)
REPLACE INTO `horarios_jornada` (`id_pk`, `tipo_fk`, `fecha`, `hora_entrada`, `tolerancia_entrada`, `hora_salida`, `tolerancia_salida`) VALUES
	(1, 'Administrativo/a', '2026-02-09', '08:00:00', '15', '12:00:00', '15');

-- Volcando estructura para tabla identia_db.rostros_usuarios
CREATE TABLE IF NOT EXISTS `rostros_usuarios` (
  `id_pk` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del rostro.',
  `id_usuario_fk` int(8) unsigned zerofill NOT NULL DEFAULT 00000000 COMMENT 'Relación con Usuarios.',
  `vector_facial` blob NOT NULL COMMENT 'Datos biométricos del rostro.',
  PRIMARY KEY (`id_pk`),
  KEY `FK_rostros_usuarios` (`id_usuario_fk`),
  CONSTRAINT `FK_rostros_usuarios` FOREIGN KEY (`id_usuario_fk`) REFERENCES `usuarios` (`id_pk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Almacena la biometría facial para el reconocimiento.';

-- Volcando datos para la tabla identia_db.rostros_usuarios: ~1 rows (aproximadamente)

-- Volcando estructura para tabla identia_db.tipos_personal
CREATE TABLE IF NOT EXISTS `tipos_personal` (
  `id_nombre_tipo` varchar(50) NOT NULL DEFAULT 'AUTO_INCREMENT' COMMENT 'Identificador único del tipo.',
  PRIMARY KEY (`id_nombre_tipo`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Clasifica a los usuarios por categorías (ej. Administrativos, Operativos). Está relacionada con Usuarios y Horarios_Jornada para definir perfiles y sus reglas de tiempo.';

-- Volcando datos para la tabla identia_db.tipos_personal: ~2 rows (aproximadamente)
REPLACE INTO `tipos_personal` (`id_nombre_tipo`) VALUES
	('Administrativo/a'),
	('Desarrollador/a');

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
) ENGINE=InnoDB AUTO_INCREMENT=42917364 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Almacena la información personal y laboral básica de cada individuo.';

-- Volcando datos para la tabla identia_db.usuarios: ~2 rows (aproximadamente)
REPLACE INTO `usuarios` (`id_pk`, `tipo_fk`, `cedula`, `nombres`, `apellidos`, `direccion_habitacional`, `correo`, `numero`, `estado`, `area_trabajo`, `rol`) VALUES
	(42917356, 'Desarrollador/a', '11111111', 'Daniel', 'Betancourt', 'Maitana', 'josedaniel@gmail.com', '04120000000', 'Activo', 'admin', 'desarrollador'),
	(42917358, 'Desarrollador/a', '00000000', 'Admin2', 'Admin2', 'Ejemplo_Direccion', 'ejemplocorreo@email.com', '04121111111', 'Activo', 'admin', 'desarrollador');

-- Volcando estructura para tabla identia_db.usuarios_administrativos
CREATE TABLE IF NOT EXISTS `usuarios_administrativos` (
  `id_pk` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID de la cuenta.',
  `id_usuario_fk` int(8) unsigned DEFAULT NULL COMMENT 'Relación con Usuarios.',
  `password` varchar(255) DEFAULT NULL COMMENT 'Contraseña (siempre hasheada).',
  PRIMARY KEY (`id_pk`),
  KEY `FK_usuarios_administrativos_usuarios` (`id_usuario_fk`),
  CONSTRAINT `FK_usuarios_administrativos_usuarios` FOREIGN KEY (`id_usuario_fk`) REFERENCES `usuarios` (`id_pk`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='Credenciales para que ciertos usuarios accedan al sistema.';

-- Volcando datos para la tabla identia_db.usuarios_administrativos: ~1 rows (aproximadamente)
REPLACE INTO `usuarios_administrativos` (`id_pk`, `id_usuario_fk`, `password`) VALUES
	(3, 42917356, 'pbkdf2_sha256$1200000$SSsjddvCyrcCmjMrlqQkLR$p++Fn6dLxhSUGvaqW4r8YVq6ZRKw72ZStLKcoQjD/3c='),
	(4, 42917358, 'pbkdf2_sha256$1200000$AAW1mTrCCVvUjKAX5cBjQi$uMK8hBTYzzveI9yZiMCfSYptrwto/NfLoSOV+ci1Mxc=');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
