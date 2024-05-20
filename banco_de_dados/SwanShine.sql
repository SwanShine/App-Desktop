-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 20/05/2024 às 13:40
-- Versão do servidor: 10.4.28-MariaDB
-- Versão do PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `glamtech`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `admins`
--

CREATE TABLE `admins` (
  `Nome` varchar(50) NOT NULL,
  `Usuario` varchar(25) NOT NULL,
  `Senha` int(25) NOT NULL,
  `Id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `admins`
--

INSERT INTO `admins` (`Nome`, `Usuario`, `Senha`, `Id`) VALUES
('Wellington', 'wl', 12345, 1001);

-- --------------------------------------------------------

--
-- Estrutura para tabela `clientes`
--

CREATE TABLE `clientes` (
  `Nome` text NOT NULL,
  `Endereço` text NOT NULL,
  `Email` varchar(255) NOT NULL,
  `CPF` varchar(11) NOT NULL,
  `Telefone` varchar(15) NOT NULL,
  `Id_clientes` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `profissionais`
--

CREATE TABLE `profissionais` (
  `Id_profissionais` int(11) NOT NULL,
  `CPF` varchar(11) NOT NULL,
  `Telefone` varchar(15) NOT NULL,
  `Nome` text NOT NULL,
  `Email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `serviços`
--

CREATE TABLE `serviços` (
  `Nome` int(11) NOT NULL,
  `Preço` varchar(11) NOT NULL,
  `Descrição` int(11) NOT NULL,
  `Id_clientes` int(11) NOT NULL,
  `id_profissionais` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `serv_pro`
--

CREATE TABLE `serv_pro` (
  `Id_profissionais` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`Id`);

--
-- Índices de tabela `serviços`
--
ALTER TABLE `serviços`
  ADD PRIMARY KEY (`Nome`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
