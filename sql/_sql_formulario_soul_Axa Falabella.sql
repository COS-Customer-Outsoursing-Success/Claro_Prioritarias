SELECT 
asi.nombre AS `Primer Nombre`,
asi.apellido AS `Primer Apellido`,
asi.segundo_nombre AS `Segundo Nombre`,
asi.segundo_apellido AS `Segundo Apellido`,
'CC' AS 'Tipo de Documento',
asi.co_id AS `No. Documento`, 
# 8726482 AS `No. Documento`,
asi.telefono1 AS `Teléfono`,
# 3116609895 AS `Teléfono`,
asi.email AS `Correo electrónico`,
asi.cod_municipio AS `Cod Municipio`,

asi.cod_departamento AS `Cod Departamento`,
asi.cod_fasecolda AS `Cod Fasecolda`,
asi.telefono2 AS `Teléfono 2`,
asi.aseguradora_actual AS `Aseguradora Actual`,
asi.clase_vehiculo AS `Clase de vehiculo`,

0 AS `Diferencia con la Aseguradora Actual`,
asi.direccion AS Dirección,
DATE_FORMAT(asi.fecha_fin_vigencia_actual, "%%Y-%%m-%%d") AS `Fecha Fin vigencia Actual`,
DATE_FORMAT(asi.fecha_fin_vigencia_actual, "%%Y-%%m-%%d") AS `Fecha Inicio vigencia Actual`,
DATE_FORMAT(asi.fecha_nacimiento, "%%Y-%%m-%%d") AS `Fecha Nacimiento`,
asi.genero AS Genero,
asi.linea AS Línea,
asi.marca AS Marca,
asi.modelo AS Modelo,
CASE
    WHEN TRIM(a.no_temporario_tradicional) = '-' THEN 0
    WHEN a.no_temporario_tradicional REGEXP '^[0-9]+(\.[0-9]+)?$' THEN CAST(a.no_temporario_tradicional AS DECIMAL(10,2))
    ELSE 0
END AS `N° Temporario 1 TRADICIONAL`,
'0' AS `N° Temporario AUTOSUFICIENTE`,
a.placa AS Placa,
0 AS `Prima Autosuficiente`,
0 AS `Prima con IVA Aseguradora Actual`,
0 AS `Prima sin IVA AUTOSUFICIENTE`,
CASE
    WHEN TRIM(a.prima_tradicional_sin_iva) = '-' THEN 0
    WHEN a.prima_tradicional_sin_iva REGEXP '^[0-9]+(\.[0-9]+)?$' THEN CAST(a.prima_tradicional_sin_iva AS DECIMAL(10,2))
    ELSE 0
END AS `Prima sin IVA TRADICIONAL`,
CASE
    WHEN TRIM(a.prima_tradicional ) = '-' THEN 0
    WHEN a.prima_tradicional  REGEXP '^[0-9]+(\.[0-9]+)?$' THEN CAST(a.prima_tradicional  AS DECIMAL(10,2))
    ELSE 0
END AS `Prima Tradicional`,
asi.servicio AS Servicio,

asi.municipio AS Ciudades,
#'San Estanislao' AS Ciudades,
asi.departamento AS Departamento,
#'BOLIVAR' AS Departamento,

#a.no_temporario_plus AS `N° Temporario 1 plus`,
165071328 AS `N° Temporario 1 plus`,
#a.prima_temporario_sin_iva_plus AS `Prima sin IVA Plus`,
1531118 AS `Prima sin IVA Plus`,
#a.prima_temporario_plus AS `Prima Plus`,
1845831 AS `Prima Plus`,
#a.suma_asegurada AS `suma aseguadora`
152500000 AS `suma aseguadora`


FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2 asi
LEFT JOIN bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_recotizada_v2 a
    ON a.placa = asi.placa 
   AND a.periodo = asi.periodo
LEFT JOIN bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos npt
    ON asi.placa = npt.placa 
   AND asi.periodo = npt.periodo
WHERE a.periodo = 202510
  AND asi.periodo = 202510
  AND npt.placa IS NULL
  AND A.Placa = 'KRM597';