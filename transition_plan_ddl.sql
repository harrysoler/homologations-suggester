drop table if exists prerequisite;
drop table if exists homologable;
drop table if exists old_curriculum_subject;
drop table if exists new_curriculum_subject;

create table old_curriculum_subject (
	code                int primary key,
	name                text not null,
	credits             tinyint not null,
	semester            tinyint not null
);

create table new_curriculum_subject (
	code                int primary key,
	name                text not null,
	credits             tinyint not null,
	semester            tinyint not null
);

create table prerequisite (
	subject_code              int not null,
	prerequisite_subject_code int not null,
	primary key (subject_code, prerequisite_subject_code),
	foreign key (subject_code)              references new_curriculum_subject(code),
	foreign key (prerequisite_subject_code) references new_curriculum_subject(code)
);

create table homologable (
	old_subject_code  int not null,
	new_subject_code  int not null,
	primary key (old_subject_code, new_subject_code),
	foreign key (old_subject_code) references old_curriculum_subject(code),
	foreign key (new_subject_code) references new_curriculum_subject(code)
);

insert into old_curriculum_subject (code, name, credits, semester) values
(96110, 'CALCULO DIFERENCIAL', 3, 1),
(95303, 'CATEDRA HENRI DIDON I', 0, 1),
(95108, 'FILOSOFIA INSTITUCIONAL', 2, 1),
(95125, 'INGLÉS I', 2, 1),
(41111, 'INTRODUCCION A LA INGENIERIA DE SISTEMAS', 3, 1),
(41112, 'INTRODUCCION A LA PROGRAMACION', 3, 1),
(11711, 'QUIMICA GENERAL', 3, 1),
(96111, 'ALGEBRA LINEAL', 3, 2),
(96500, 'BASES DE DATOS', 3, 2),
(96113, 'CALCULO INTEGRAL', 3, 2),
(95304, 'CATEDRA HENRI DIDON II', 0, 2),
(15135, 'COMUNICACION ORAL Y ESCRITA', 2, 2),
(95127, 'INGLÉS II', 2, 2),
(96181, 'PROGRAMACION ORIENTADA A OBJETOS', 3, 2),
(95109, 'ANTROPOLOGIA', 2, 3),
(96200, 'CALCULO VECTORIAL', 3, 3),
(96400, 'ESTRUCTURAS DE DATOS', 3, 3),
(96112, 'FISICA MECANICA', 3, 3),
(95128, 'INGLÉS III', 2, 3),
(41114, 'REQUERIMIENTOS Y DISEÑO DE SOFTWARE', 3, 3),
(96300, 'ARQUITECTURA DEL COMPUTADOR', 3, 4),
(96503, 'CONSTRUCCION DE SOFTWARE', 3, 4),
(42822, 'ECUACIONES DIFERENCIALES', 3, 4),
(43002, 'ELECTRICIDAD Y MAGNETISMO', 3, 4),
(95110, 'EPISTEMOLOGIA', 2, 4),
(95129, 'INGLÉS IV', 2, 4),
(37604, 'ARQUITECTURA EMPRESARIAL', 3, 5),
(95111, 'CULTURA TEOLOGICA', 2, 5),
(40748, 'DESARROLLO EMPRESARIAL', 3, 5),
(95130, 'INGLÉS V', 2, 5),
(83007, 'METODOS NUMERICOS', 3, 5),
(48004, 'SISTEMAS OPERATIVOS', 3, 5),
(41115, 'DESARROLLO ORIENTADO A SERVICIOS', 3, 6),
(96701, 'GERENCIA DE SOFTWARE', 3, 6),
(95348, 'INGLÉS VI', 2, 6),
(95602, 'OPTIMIZACION', 3, 6),
(30107, 'PROBABILIDAD Y ESTADISTICA', 2, 6),
(41116, 'REDES', 3, 6),
(41119, 'CALIDAD DE SOFTWARE', 4, 7),
(41117, 'ELECTIVA I INTERDISCIPLINARIA', 3, 7),
(41118, 'ELECTIVA I PROFUNDIZACION', 3, 7),
(96906, 'ELECTIVA SOCIOHUMANISTICA', 3, 7),
(96904, 'SIMULACION', 3, 7),
(41121, 'ELECTIVA III INTERDISCIPLINARIA', 3, 8),
(41120, 'ELECTIVA II INTERDISCIPLINARIA', 3, 8),
(41122, 'ELECTIVA II PROFUNDIZACION', 3, 8),
(96805, 'FILOSOFIA POLITICA', 2, 8),
(96804, 'PRACTICA EMPRESARIAL', 4, 8),
(37606, 'AUDITORIA DE SISTEMAS', 4, 9),
(41123, 'ELECTIVA III PROFUNDIZACION', 3, 9),
(41124, 'ELECTIVA INGENIERIA APLICADA', 3, 9),
(96905, 'TRABAJO DE GRADO I', 4, 9),
(96098, 'ETICA', 2, 10),
(18689, 'LEGISLACION INFORMATICA', 2, 10),
(96097, 'TRABAJO DE GRADO II', 7, 10);

insert into new_curriculum_subject (code, name, credits, semester) values
-- Semester 1
(96103, 'ALGEBRA LINEAL', 2, 1),
(11701, 'CALCULO DIFERENCIAL', 3, 1),
(31161, 'DISEÑO WEB', 3, 1),
(10240, 'FILOSOFIA INSTITUCIONAL', 2, 1),
(99102, 'CATEDRA HENRI DIDON I', 0, 1),
(99101, 'CATEDRA HENRI DIDON I', 0, 1),
(41111, 'INTRODUCCION A LA INGENIERIA SISTEMAS', 3, 1),
(15650, 'LENGUA EXTRANJERA I', 2, 1),
(95081, 'INGLÉS I', 2, 3),
(31160, 'PROGRAMACION ESTRUCTURADA PARA INGENIERÍAS', 2, 1),
(98150, 'COMUNICACION ORAL Y ESCRITA', 2, 1),

-- Semester 2
(96500, 'BASES DE DATOS', 3, 2),
(96113, 'CALCULO INTEGRAL', 3, 2),
(33126, 'CATEDRA OPCIONAL INSTITUCIONAL', 2, 2),
(99103, 'CATEDRA HENRI DIDON II', 0, 2),
(91504, 'ESTADISTICA Y PROBABILIDAD', 2, 2),
(15651, 'LENGUA EXTRANJERA II', 2, 2),
(95082, 'INGLÉS II', 2, 3),
(30115, 'METODOS NUMERICOS', 2, 2),
(96181, 'PROGRAMACION ORIENTADA A OBJETOS', 3, 2),

-- Semester 3
(82355, 'ANALISIS NUMERICO', 2, 3),
(41151, 'BASES DE DATOS NOSQL', 3, 3),
(96115, 'CALCULO VECTORIAL', 3, 3),
(40748, 'DESARROLLO EMPRESARIAL', 3, 3),
(96112, 'FISICA MECANICA', 3, 3),
(15652, 'LENGUA EXTRANJERA III', 2, 3),
(95083, 'INGLÉS III', 2, 3),
(95345, 'INGLÉS III / INGLES III', 2, 3),
(30597, 'PERSONA HUMANA, SOCIEDAD Y CONOCIMIENTO', 2, 3),
(20652, 'FISICA MECANICA', 3, 3),

-- Semester 4
(41170, 'ANALÍTICA DE DATOS', 2, 4),
(96117, 'ECUACIONES DIFERENCIALES', 2, 4),
(30670, 'ELECTIVA', 2, 4),
(96161, 'ELECTRICIDAD Y MAGNETISMO', 3, 4),
(96400, 'ESTRUCTURA DE DATOS', 3, 4),
(15653, 'LENGUA EXTRANJERA IV', 2, 4),
(95084, 'INGLÉS IV', 2, 4),
(31162, 'MICROSERVICIOS', 3, 4),
(34102, 'REQUERIMIENTOS Y DISEÑO DE SOFTWARE / DISEÑO DE SOFTWARE', 3, 4),

-- Semester 5
(96300, 'ARQUITECTURA DEL COMPUTADOR', 3, 5),
(37604, 'ARQUITECTURA EMPRESARIAL', 3, 5),
(31163, 'BROKER DE MENSAJERIA', 3, 5),
(15654, 'LENGUA EXTRANJERA V', 2, 5),
(95085, 'INGLÉS V', 2, 5),
(41158, 'MACHINE LEARNING', 3, 5),
(30672, 'OPTATIVA I', 3, 5),
(96501, 'REDES / REDES I', 3, 5),
(10271, 'EPISTEMOLOGIA', 2, 5),
(10263, 'CULTURA TEOLOGICA', 2, 5),

-- Semester 6
(41150, 'BIG DATA', 2, 6),
(62345, 'CULTURA TEOLOGICA Y HECHO RELIGIOSO', 2, 6),
(96701, 'GERENCIA Y CALIDAD DE SOFTWARE', 3, 6),
(31164, 'OPTATIVA DE PROFUNDIZACION 1', 3, 6),
(96904, 'SIMULACION', 3, 6),
(48004, 'SISTEMAS OPERATIVOS', 3, 6),
(62337, 'ANTROPOLOGIA', 2, 6),
(96601, 'REDES / REDES II', 3, 6),
(95086, 'INGLÉS VI', 2, 6),

-- Semester 7
(37606, 'AUDITORIA DE SISTEMAS', 3, 7),
(41131, 'DEEP LEARNING', 3, 7),
(30650, 'ETICA Y FORMACIÓN CIUDADANA', 2, 7),
(30673, 'OPTATIVA 2', 3, 7),
(31165, 'OPTATIVA DE PROFUNDIZACION 2', 3, 7),
(41116, 'REDES', 3, 7),

-- Semester 8
(30423, 'OPCIÓN DE GRADO', 7, 8),
(31167, 'OPTATIVA DE PROFUNDIZACION 3', 3, 8);

insert into prerequisite (subject_code, prerequisite_subject_code) values
(96113, 11701), -- Cálculo Integral -> Cálculo Diferencial
(96115, 96103), -- Cálculo Vectorial -> Álgebra Lineal
(96112, 11701), -- Física Mecánica -> Cálculo Diferencial
(96161, 96112), -- Electricidad y Magnetismo -> Física Mecánica
(96117, 96113), -- Ecuaciones Diferenciales -> Cálculo Integral
(15651, 15650), -- Lengua Extranjera 2 -> Lengua Extranjera 1
(15652, 15651), -- Lengua Extranjera 3 -> Lengua Extranjera 2
(15653, 15652), -- Lengua Extranjera 4 -> Lengua Extranjera 3
(15654, 15653), -- Lengua Extranjera 5 -> Lengua Extranjera 4
(96181, 31160), -- Programación Orientada a Objetos -> Programación Estructurada para Ingenierías
(40748, 96181), -- Desarrollo Empresarial -> Programación Orientada a Objetos
(40748, 31161), -- Desarrollo Empresarial -> Diseño Web
(40748, 96500), -- Desarrollo Empresarial -> Base de Datos
(96400, 96181), -- Estructura de Datos -> Programación Orientada a Objetos
(31162, 40748), -- Microservicios -> Desarrollo Empresarial
(37604, 40748), -- Arquitectura Empresarial -> Desarrollo Empresarial
(31163, 31162), -- Broker de Mensajería -> Microservicios
(48004, 96300), -- Sistemas Operativos -> Arquitectura del Computador
(41151, 96500), -- Bases de Datos NoSQL -> Bases de Datos
(41131, 41158); -- Deep Learning -> Machine Learning

insert into homologable(old_subject_code, new_subject_code) values
(96110,11701), -- calculo diferencial
(41112,31160), -- introducción a la programación -> programacion para ingenierias
(96111,96103), -- algebra lineal
(95125,15650), -- ingles 1 -> lengua extranjera 1
(95108,10240), -- filosofia institucional
(41111,41111), -- introducción a la ing de sistemas
(96113,96113), -- calculo integral
(83007,30115), -- metodos numericos
(30107,91504), -- probabilidad y estadistica
(95127,15651), -- ingles 2 -> lengua extranjera 2
(96181,96181), -- programación orientada a objetos
(96500,96500), -- bases de datos
(96200,96115), -- calculo vectorial
(40748,40748), -- desarrollo empresarial
(96112,96112), -- fisica mecanica
(95128,15652), -- ingles 3 -> lengua extranjera 3
(95303,33126); -- catedra henry didon
