Esta aplicación CLI extrae información de historicos de notas, con la cual es posible realizar:

- La relación de materias homologables (con información de una base de datos SQLite), donde llena un formato Excel de homologación con la información del estudiante.
- (EN PROGRESO) Mostrar un listado de materias faltantes o por ver priorizadas por semestre y materias de línea.

# Entrada

El archivo PDF del historico de notas para extraer los siguientes datos:

- Nombre
- Documento de identidad
- Número total de créditos homologados
- Asignaturas aprobadas

# Salida

El resultado final es un formato Excel oficial llenado con:

- Nombre del estudiante
- Nivel de formación (semestre)
- Tipo de documento (no se puede extraer)
- Documento de identidad
- Tipo de homologación o reconocimiento de créditos = "Trancisión de plan de estudios"
- Institución de educación superior de destino = "Universidad Santo Tomás"
- Ciudad = "Tunja"
- Pais = "Colombia"
- Programa de origen = "Ingeniería de Sistemas"
- Programa de destino = "Ingeniería de Sistemas"
- Plan de origen = "2018-2"
- Plan de destino = "2026-2"
- Número total de créditos homologados o reconocidos en el programa destino = suma de créditos homologados
- Relación de materias homologadas del programa antiguo al nuevo

# Entidades

ApprovedSubject: Relación de materia homologada exitosamente
  - OriginSubject
  - DestinationSubject
  - Nota

NewPensumSubject & OldPensumSubject: Materias de pensum viejo y nuevo
  - Código = Code
  - Espacio Acádemico = Subject
  - Creditos = Credits
  - Nota = Grade

# Estructura SQLite

Asignatura (viejo pensum):
  - Código tinyint (PK)
  - Nombre text
  - Creditos tinyint
  - Semestre tinyint

Asignatura (nuevo pensum):
  - Código tinyint (PK)
  - Nombre text
  - Creditos tinyint
  - Semestre tinyint

Prerequisito: Lista de condiciones en forma de asignaturas requeridas para ver la siguiente
  - Codigo asignatura (FK asignatura)
  - Codigo asignatura prerequisito (FK asignatura)

Homologable: Relación de asignaturas homologables entre pensums
  - Codigo asignatura viejo pensum (FK asignatura)
  - Codigo asignatura nuevo pensum (FK asignatura)

# Arquitectura

![Application architecture](assets/architecture.png)
