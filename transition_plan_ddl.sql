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
	semester            tinyint not null,
	is_main				boolean not null default false
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
(99101, 'CATEDRA HENRI DIDON I', 0, 1),
(99102, 'CATEDRA HENRI DIDON I', 0, 1),
(95108, 'FILOSOFIA INSTITUCIONAL', 2, 1),
(10240, 'FILOSOFIA INSTITUCIONAL', 2, 1),
(95125, 'INGLÉS I', 2, 1),
(95081, 'INGLÉS I', 2, 3),
(41111, 'INTRODUCCION A LA INGENIERIA DE SISTEMAS', 3, 1),
(41112, 'INTRODUCCION A LA PROGRAMACION', 3, 1),
(11711, 'QUIMICA GENERAL', 3, 1),
(96111, 'ALGEBRA LINEAL', 3, 2),
(96500, 'BASES DE DATOS', 3, 2),
(96113, 'CALCULO INTEGRAL', 3, 2),
(95304, 'CATEDRA HENRI DIDON II', 0, 2),
(99103, 'CATEDRA HENRI DIDON II', 0, 2),
(15135, 'COMUNICACION ORAL Y ESCRITA', 2, 2),
(95127, 'INGLÉS II', 2, 2),
(95082, 'INGLÉS II', 2, 3),
(96181, 'PROGRAMACION ORIENTADA A OBJETOS', 3, 2),
(95109, 'ANTROPOLOGIA', 2, 3),
(62337, 'ANTROPOLOGIA', 2, 6),
(96200, 'CALCULO VECTORIAL', 3, 3),
(96115, 'CALCULO VECTORIAL', 3, 3),
(96400, 'ESTRUCTURAS DE DATOS', 3, 3),
(96112, 'FISICA MECANICA', 3, 3),
(95128, 'INGLÉS III', 2, 3),
(95345, 'INGLÉS III / INGLES III', 2, 3),
(95083, 'INGLÉS III', 2, 3),
(41114, 'REQUERIMIENTOS Y DISEÑO DE SOFTWARE', 3, 3),
(96300, 'ARQUITECTURA DEL COMPUTADOR', 3, 4),
(96503, 'CONSTRUCCION DE SOFTWARE', 3, 4),
(42822, 'ECUACIONES DIFERENCIALES', 3, 4),
(43002, 'ELECTRICIDAD Y MAGNETISMO', 3, 4),
(96161, 'ELECTRICIDAD Y MAGNETISMO', 3, 4),
(95110, 'EPISTEMOLOGIA', 2, 4),
(10271, 'EPISTEMOLOGIA', 2, 5),
(95129, 'INGLÉS IV', 2, 4),
(95084, 'INGLÉS IV', 2, 4),
(37604, 'ARQUITECTURA EMPRESARIAL', 3, 5),
(95111, 'CULTURA TEOLOGICA', 2, 5),
(10263, 'CULTURA TEOLOGICA', 2, 5),
(40748, 'DESARROLLO EMPRESARIAL', 3, 5),
(95130, 'INGLÉS V', 2, 5),
(95085, 'INGLÉS V', 2, 5),
(83007, 'METODOS NUMERICOS', 3, 5),
(48004, 'SISTEMAS OPERATIVOS', 3, 5),
(41115, 'DESARROLLO ORIENTADO A SERVICIOS', 3, 6),
(96701, 'GERENCIA DE SOFTWARE', 3, 6),
(95348, 'INGLÉS VI', 2, 6),
(95086, 'INGLÉS VI', 2, 6),
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
(96097, 'TRABAJO DE GRADO II', 7, 10),
(96501, 'REDES / REDES I', 3, 5),
(34102, 'REQUERIMIENTOS Y DISEÑO DE SOFTWARE / DISEÑO DE SOFTWARE', 3, 4),
(96601, 'REDES / REDES II', 3, 6),
(20652, 'FISICA MECANICA', 3, 3),
(98150, 'COMUNICACION ORAL Y ESCRITA', 2, 1);

insert into new_curriculum_subject (code, name, credits, semester, is_main) values
-- Semester 1
(96103, 'ALGEBRA LINEAL', 2, 1, false),
(11701, 'CALCULO DIFERENCIAL', 3, 1, false),
(31161, 'DISEÑO WEB', 3, 1, true),
(10240, 'FILOSOFIA INSTITUCIONAL', 2, 1, false),
(41111, 'INTRODUCCION A LA INGENIERIA SISTEMAS', 3, 1, true),
(15650, 'LENGUA EXTRANJERA I', 2, 1, false),
(31160, 'PROGRAMACION ESTRUCTURADA PARA INGENIERÍAS', 2, 1, true),

-- Semester 2
(96500, 'BASES DE DATOS', 3, 2, true),
(96113, 'CALCULO INTEGRAL', 3, 2, false),
(33126, 'CATEDRA OPCIONAL INSTITUCIONAL', 2, 2, false),
(91504, 'ESTADISTICA Y PROBABILIDAD', 2, 2, false),
(15651, 'LENGUA EXTRANJERA II', 2, 2, false),
(30115, 'METODOS NUMERICOS', 2, 2, false),
(96181, 'PROGRAMACION ORIENTADA A OBJETOS', 3, 2, true),

-- Semester 3
(82355, 'ANALISIS NUMERICO', 2, 3, false),
(41151, 'BASES DE DATOS NOSQL', 3, 3, true),
(96115, 'CALCULO VECTORIAL', 3, 3, false),
(40748, 'DESARROLLO EMPRESARIAL', 3, 3, true),
(96112, 'FISICA MECANICA', 3, 3, false),
(15652, 'LENGUA EXTRANJERA III', 2, 3, false),
(30597, 'PERSONA HUMANA, SOCIEDAD Y CONOCIMIENTO', 2, 3, false),

-- Semester 4
(41170, 'ANALÍTICA DE DATOS', 2, 4, true),
(96117, 'ECUACIONES DIFERENCIALES', 2, 4, false),
(30670, 'ELECTIVA', 2, 4, true),
(96161, 'ELECTRICIDAD Y MAGNETISMO', 3, 4, false),
(96400, 'ESTRUCTURAS DE DATOS', 3, 4, true),
(15653, 'LENGUA EXTRANJERA IV', 2, 4, false),
(31162, 'MICROSERVICIOS', 3, 4, true),

-- Semester 5
(96300, 'ARQUITECTURA DEL COMPUTADOR', 3, 5, true),
(37604, 'ARQUITECTURA EMPRESARIAL', 3, 5, true),
(31163, 'BROKER DE MENSAJERIA', 3, 5, true),
(15654, 'LENGUA EXTRANJERA V', 2, 5, false),
(41158, 'MACHINE LEARNING', 3, 5, true),
(30672, 'OPTATIVA I', 3, 5, true),

-- Semester 6
(41150, 'BIG DATA', 2, 6, true),
(62345, 'CULTURA TEOLOGICA Y HECHO RELIGIOSO', 2, 6, false),
(96701, 'GERENCIA Y CALIDAD DE SOFTWARE', 3, 6, true),
(31164, 'OPTATIVA DE PROFUNDIZACION 1', 3, 6, true),
(96904, 'SIMULACION', 3, 6, true),
(48004, 'SISTEMAS OPERATIVOS', 3, 6, true),

-- Semester 7
(37606, 'AUDITORIA DE SISTEMAS', 3, 7, true),
(41131, 'DEEP LEARNING', 3, 7, true),
(30650, 'ETICA Y FORMACIÓN CIUDADANA', 2, 7, false),
(30673, 'OPTATIVA 2', 3, 7, true),
(31165, 'OPTATIVA DE PROFUNDIZACION 2', 3, 7, true),
(41116, 'REDES', 3, 7, true),

-- Semester 8
(30423, 'OPCIÓN DE GRADO', 7, 8, true),
(31167, 'OPTATIVA DE PROFUNDIZACION 3', 3, 8, true);

insert into prerequisite (subject_code, prerequisite_subject_code) values
(96113, 11701), -- Cálculo Integral -> Cálculo Diferencial
(96115, 96103), -- Cálculo Vectorial -> Álgebra Lineal
(96115, 96113), -- Cálculo Vectorial -> Cálculo Integral
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
(41131, 41158), -- Deep Learning -> Machine Learning
(30673, 30672), -- Optativa II -> Optativa I
(31165, 31164), -- Optativa de profundización II -> Optativa de profundización I
(31167, 31165); -- Optativa de profundización III -> Optativa de profundización II

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
(95303,33126), -- catedra henry didon
-- New homologations from homologables.csv
(10240,10240), -- filosofia institucional (dup)
(95109,30597), -- Antropología -> Persona Humana, Sociedad y Conocimiento
(96400,96400), -- Estructuras de Datos -> Estructura de Datos
(43002,96161), -- Electricidad y Magnetismo -> Electricidad y Magnetismo
(42822,96117), -- Ecuaciones Diferenciales -> Ecuaciones Diferenciales
(95129,15653), -- Inglés IV -> Lengua Extranjera 4
(96300,96300), -- Arquitectura del Computador -> Arquitectura del Computador
(96503,31161), -- Construcción de Software -> Diseño Web
(95110,30597), -- Epistemología -> Persona Humana, Sociedad y Conocimiento
(95130,15654), -- Inglés V -> Lengua Extranjera 5
(37604,37604), -- Arquitectura Empresarial -> Arquitectura Empresarial
(48004,48004), -- Sistemas Operativos -> Sistemas Operativos
(95111,62345), -- Cultura Teológica -> Cultura Teológica y Hecho Religioso
(95602,82355), -- Optimización -> Análisis Numérico
(41115,31162), -- Desarrollo Orientado a Servicios -> Microservicios
(41116,41116), -- Redes -> Redes
(96906,33126), -- Electiva Socio-Humanística -> Cátedra Opcional Institucional
(96904,96904), -- Simulación -> Simulación
(41117,30672), -- Electiva I Interdisciplinaria -> Optativa 1
(41118,31164), -- Electiva I Profundización -> Optativa de Profundización 1
(41120,30673), -- Electiva II Interdisciplinaria -> Optativa 2
(41121,31167), -- Electiva III Interdisciplinaria -> Optativa de Profundización 3
(41122,31165), -- Electiva II Profundización -> Optativa de Profundización 2
(96805,33126), -- Filosofía Política -> Cátedra Opcional Institucional
(37606,37606), -- Auditoría de Sistemas -> Auditoría de Sistemas
(41123,31167), -- Electiva III Profundización -> Optativa de Profundización 3
(41124,30670), -- Electiva Ingeniería Aplicada -> Electiva
(96905,30423), -- Trabajo de Grado I -> Opción de Grado
(96097,30423), -- Trabajo de Grado II -> Opción de Grado
(96098,30650), -- Ética -> Ética y Formación Ciudadana
-- Duplicate old curriculum subjects (same name, different code)
(96501,41116), -- Redes I -> Redes (dup)
(96601,41116), -- Redes II -> Redes (dup)
(95084,15653), -- Inglés IV -> Lengua Extranjera 4 (dub)
(96161,96161), -- Electricidad y Magnetismo (dup)
(96115,96115), -- Cálculo Vectorial (dup)
(62337,30597), -- Antropología (dup) -> Persona Humana, Sociedad y Conocimiento
(99102,33126), -- CATEDRA HENRI DIDON I (dup) -> Cátedra Opcional Institucional
(99101,33126), -- CATEDRA HENRI DIDON I (dup) -> Cátedra Opcional Institucional
(95304,33126), -- CATEDRA HENRI DIDON II (dup) -> Cátedra Opcional Institucional
(99103,33126), -- CATEDRA HENRI DIDON II (dup) -> Cátedra Opcional Institucional
(95081,15650), -- Inglés I (dup) -> Lengua Extranjera I
(95082,15651), -- Inglés II (dup) -> Lengua Extranjera II
(95083,15652), -- Inglés III (dup) -> Lengua Extranjera III
(95085,15654), -- Inglés V (dup) -> Lengua Extranjera V
(95348,15653), -- Inglés VI -> Lengua Extranjera IV
(95086,15654), -- Inglés VI (dup) -> Lengua Extranjera V
(10271,30597), -- Epistemología (dup) -> Persona Humana, Sociedad y Conocimiento
(10263,62345), -- Cultura Teológica (dup) -> Cultura Teológica y Hecho Religioso
(20652,96112); -- Física Mecánica (dup) -> Física Mecánica
