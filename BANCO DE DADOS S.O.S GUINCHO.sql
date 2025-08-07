CREATE DATABASE IF NOT EXISTS guincho_db_def;
USE guincho_db_def;

-- Tabela cidade
CREATE TABLE cidade (
    CEP VARCHAR(8) PRIMARY KEY,
    Nome VARCHAR(30),
    Estado CHAR(2)
);

-- Tabela caminhao 
CREATE TABLE caminhao (
    placa VARCHAR(10) PRIMARY KEY NOT NULL,
    fabricante_modelo VARCHAR(40) NOT NULL,
    cor VARCHAR(15) NOT NULL,
    status ENUM('Disponível', 'Em Serviço', 'Indisponível') NOT NULL
);

-- Tabela motorista
CREATE TABLE motorista (
    id_motorista INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome_motorista VARCHAR(50),
    guincho VARCHAR(10), 
    status_motorista VARCHAR(1),
    cep_motorista VARCHAR(8),
    FOREIGN KEY (cep_motorista) REFERENCES cidade(CEP),
    FOREIGN KEY (guincho) REFERENCES caminhao(placa) 
);

INSERT INTO caminhao (placa, fabricante_modelo, cor, status) 
VALUES ('00', 'Sem Caminhão', 'Vermelho', 'Disponível');


INSERT INTO cidade (CEP, Nome, Estado) 
VALUES ('00', 'Sem Cidade', 'NA');