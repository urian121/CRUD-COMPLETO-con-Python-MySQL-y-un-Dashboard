-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.30 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando estructura para tabla bd_consignaciones.consignaciones
CREATE TABLE IF NOT EXISTS `consignaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `valor_consignacion` bigint NOT NULL,
  `name_archivo` mediumtext COLLATE utf8mb4_general_ci,
  `url_archivo` mediumtext COLLATE utf8mb4_general_ci NOT NULL,
  `nota_consignacion` mediumtext COLLATE utf8mb4_general_ci,
  `estatus_leido` tinyint(1) DEFAULT '0',
  `bandeja` bigint DEFAULT '0',
  `code_tienda` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ip_consignacion` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `nombre_tienda` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla bd_consignaciones.consignaciones: ~7 rows (aproximadamente)
INSERT INTO `consignaciones` (`id`, `valor_consignacion`, `name_archivo`, `url_archivo`, `nota_consignacion`, `estatus_leido`, `bandeja`, `code_tienda`, `ip_consignacion`, `nombre_tienda`) VALUES
	(1, 10000, '822edc32e73c470e997a6aa5b9ef8b9073757ea8996d4ac29cb2af317c70ad3d7604230a1c764fa38e1c4c333d3aae705879.png', 'consignment_files/June_2023/822edc32e73c470e997a6aa5b9ef8b9073757ea8996d4ac29cb2af317c70ad3d7604230a1c764fa38e1c4c333d3aae705879.png', 'primera consignacion', 0, 0, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1'),
	(2, 5000, '19c9e83fd3bc4c6aafd6a3465dff46df74e20d53a39343f7900ab4d52db3191e48fbc478499d4f7281f910a4381e80983300.png', 'consignment_files/June_2023/19c9e83fd3bc4c6aafd6a3465dff46df74e20d53a39343f7900ab4d52db3191e48fbc478499d4f7281f910a4381e80983300.png', 'segunda consignacion', 1, 1, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1'),
	(3, 2500000, '3a2d40c5981e45668921747e68d7e0c43da624cbe97140cbb3342defaa5f9a827faaaec0812b4c3591a14b2e6e02885773e3.jpg', 'consignment_files/June_2023/3a2d40c5981e45668921747e68d7e0c43da624cbe97140cbb3342defaa5f9a827faaaec0812b4c3591a14b2e6e02885773e3.jpg', 'tercera consignacion', 1, 1, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1'),
	(4, 1400, '1cd43feea8d04ea1aa6a069a1ab76d8e67da6ec26b2a4327b204d150f6aa22149634745530d949aeb802a25a8c9e6b66301a.jpg', 'consignment_files/June_2023/1cd43feea8d04ea1aa6a069a1ab76d8e67da6ec26b2a4327b204d150f6aa22149634745530d949aeb802a25a8c9e6b66301a.jpg', 'Primera Consignacion grupal', 1, 0, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1'),
	(5, 12000, 'c62f35dcc3b9451ebc2914f37941d45462c07635e9b346b7bc714b1dcd2e4413bbef68e8a24b4a718e00c988cbaf5191784b.png', 'consignment_files/June_2023/c62f35dcc3b9451ebc2914f37941d45462c07635e9b346b7bc714b1dcd2e4413bbef68e8a24b4a718e00c988cbaf5191784b.png', 'Hoy es viernes', 1, 0, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1'),
	(6, 3000, 'b5993196486a42d9b77c1f23fffe8cfc2cd9c7c0cfba4a1aaefac85bf8679d32259f45fafcad405299bc8b40995e78c11cae.jpg', 'consignment_files/June_2023/b5993196486a42d9b77c1f23fffe8cfc2cd9c7c0cfba4a1aaefac85bf8679d32259f45fafcad405299bc8b40995e78c11cae.jpg', 'son 3 en una', 1, 0, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1'),
	(7, 60000, '1ac9b1691d6742459b8efcc87ffafe15f5653cfaec1547c79c21fd7a2840298c3c488b01519646a587a82f02f3fcc0f79c82.PNG', 'consignment_files/June_2023/1ac9b1691d6742459b8efcc87ffafe15f5653cfaec1547c79c21fd7a2840298c3c488b01519646a587a82f02f3fcc0f79c82.PNG', 'yyrty', 1, 0, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1'),
	(8, 12000, '28062097da844394ade64e0d29613cf0ba4cc5c040c24b369f1b663f6736148dab121a1fdb0541d8abb6c202d6408fbb7a23.PNG', 'consignment_files/July_2023/28062097da844394ade64e0d29613cf0ba4cc5c040c24b369f1b663f6736148dab121a1fdb0541d8abb6c202d6408fbb7a23.PNG', 'hola', 0, 0, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1'),
	(9, 534543, 'b89269f3a74f4627abd9c147333e9bd7393bf8f1ae65462eb1661f091a0cff5d2b6373a0d1824582ae716fc7660ad63d9b3b.png', 'consignment_files/July_2023/b89269f3a74f4627abd9c147333e9bd7393bf8f1ae65462eb1661f091a0cff5d2b6373a0d1824582ae716fc7660ad63d9b3b.png', '4535', 0, 0, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1'),
	(10, 4000000, 'eddf549329d249339437d89b6b6e3c7a94bb3192223146bc90813e10642e0a7196d80930fac54e5e9092f487c1817b2a2bc5.PNG', 'consignment_files/July_2023/eddf549329d249339437d89b6b6e3c7a94bb3192223146bc90813e10642e0a7196d80930fac54e5e9092f487c1817b2a2bc5.PNG', 'quiero una mac pro m2', 0, 0, '1', '10.0.8.152', 'D&G SANTANDER CUCUTA 1');

-- Volcando estructura para tabla bd_consignaciones.detalles_consignaciones
CREATE TABLE IF NOT EXISTS `detalles_consignaciones` (
  `id_detalles_consignaciones` int NOT NULL AUTO_INCREMENT,
  `id_consignacion` int DEFAULT NULL,
  `valor_venta` int DEFAULT NULL,
  `dia_venta` date DEFAULT NULL,
  `fecha_consignacion_banco` date DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_detalles_consignaciones`),
  KEY `FK_CONSIGNACION` (`id_consignacion`),
  CONSTRAINT `FK_CONSIGNACION` FOREIGN KEY (`id_consignacion`) REFERENCES `consignaciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla bd_consignaciones.detalles_consignaciones: ~11 rows (aproximadamente)
INSERT INTO `detalles_consignaciones` (`id_detalles_consignaciones`, `id_consignacion`, `valor_venta`, `dia_venta`, `fecha_consignacion_banco`, `fecha_registro`) VALUES
	(1, 1, 10000, '2023-06-05', '2023-06-29', '2023-06-29 22:21:32'),
	(2, 2, 5000, '2023-06-06', '2023-06-29', '2023-06-29 22:23:26'),
	(3, 3, 2500000, '2023-06-15', '2023-06-29', '2023-06-29 22:26:03'),
	(4, 4, 600, '2023-06-23', '2023-06-29', '2023-06-29 22:28:05'),
	(5, 4, 500, '2023-06-14', '2023-06-29', '2023-06-29 22:28:05'),
	(6, 4, 300, '2023-06-21', '2023-06-29', '2023-06-29 22:28:05'),
	(7, 5, 12000, '2023-06-20', '2023-06-30', '2023-06-30 12:51:52'),
	(8, 6, 1200, '2023-06-27', '2023-06-30', '2023-06-30 13:06:05'),
	(9, 6, 800, '2023-06-28', '2023-06-30', '2023-06-30 13:06:05'),
	(10, 6, 1000, '2023-06-29', '2023-06-30', '2023-06-30 13:06:05'),
	(11, 7, 60000, '2023-06-19', '2023-06-30', '2023-06-30 17:12:11'),
	(12, 8, 12000, '2023-07-03', '2023-07-04', '2023-07-04 20:15:16'),
	(13, 9, 534543, '2023-07-03', '2023-07-04', '2023-07-04 20:22:32'),
	(14, 10, 4000000, '2023-07-02', '2023-07-04', '2023-07-04 20:23:55');

-- Volcando estructura para tabla bd_consignaciones.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name_surname` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `email_user` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `pass_user` text COLLATE utf8mb4_general_ci NOT NULL,
  `created_user` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla bd_consignaciones.users: ~0 rows (aproximadamente)
INSERT INTO `users` (`id`, `name_surname`, `email_user`, `pass_user`, `created_user`) VALUES
	(1, 'Urian', 'dev@gmail.com', 'sha256$K0WIbCmlZStNb2P3$79468fd6870db9ccb849767694df5ffa16ffc3660940427c7b7b7ee3ce7f894e', '2023-05-08 14:04:57');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
