-- --------------------------------------------------------
-- Database: `kripto_sakti`
-- --------------------------------------------------------

-- 
-- Table structure for table `dosen`
-- 
CREATE TABLE `dosen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  `nidn` varchar(20) NOT NULL UNIQUE,
  `jurusan` varchar(50) NOT NULL,
  `fakultas` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

-- 
-- Table structure for table `mahasiswa`
-- 
CREATE TABLE `mahasiswa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  `nim` varchar(20) NOT NULL UNIQUE,
  `jurusan` varchar(50) NOT NULL,
  `fakultas` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `dosen_wali_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`dosen_wali_id`) REFERENCES `dosen` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

-- 
-- Table structure for table `tugas`
-- 
CREATE TABLE `tugas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dosen_id` int(11) NOT NULL,
  `mahasiswa_id` int(11) NOT NULL,
  `judul` varchar(200) NOT NULL,
  `deskripsi` text NOT NULL,
  `file_encrypted` longblob DEFAULT NULL,
  `file_name` varchar(200) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Belum Upload',
  `komentar` text DEFAULT NULL,
  `tanggal_buat` datetime DEFAULT CURRENT_TIMESTAMP,
  `tanggal_kumpul` datetime DEFAULT NULL,
  `kunci_rahasia` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`dosen_id`) REFERENCES `dosen` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`mahasiswa_id`) REFERENCES `mahasiswa` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

-- 
-- Table structure for table `transkrip`
-- 
CREATE TABLE `transkrip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mahasiswa_id` int(11) NOT NULL,
  `dosen_id` int(11) NOT NULL,
  `nilai_image_encrypted` longblob NOT NULL,
  `tanggal_verifikasi` datetime DEFAULT CURRENT_TIMESTAMP,
  `verif_info` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`dosen_id`) REFERENCES `dosen` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`mahasiswa_id`) REFERENCES `mahasiswa` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
