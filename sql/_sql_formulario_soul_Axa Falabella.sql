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
asi.municipio AS Ciudades,
asi.cod_departamento AS `Cod Departamento`,
asi.cod_fasecolda AS `Cod Fasecolda`,
asi.telefono2 AS `Teléfono 2`,
asi.aseguradora_actual AS `Aseguradora Actual`,
asi.clase_vehiculo AS `Clase de vehiculo`,
asi.departamento AS Departamento,
0 AS `Diferencia con la Aseguradora Actual`,
asi.direccion AS Dirección,
DATE_FORMAT(asi.fecha_fin_vigencia_actual, "%%Y-%%m-%%d") AS `Fecha Fin vigencia Actual`,
DATE_FORMAT(asi.fecha_fin_vigencia_actual, "%%Y-%%m-%%d") AS `Fecha Inicio vigencia Actual`,
DATE_FORMAT(asi.fecha_nacimiento, "%%Y-%%m-%%d") AS `Fecha Nacimiento`,
asi.genero AS Genero,
asi.linea AS Línea,
asi.marca AS Marca,
asi.modelo AS Modelo,
a.no_temporario_tradicional AS `N° Temporario 1 TRADICIONAL`,
'0' AS `N° Temporario AUTOSUFICIENTE`,
a.placa AS Placa,
0 AS `Prima Autosuficiente`,
0 AS `Prima con IVA Aseguradora Actual`,
0 AS `Prima sin IVA AUTOSUFICIENTE`,
a.prima_tradicional_sin_iva AS `Prima sin IVA TRADICIONAL`,
a.prima_tradicional AS `Prima Tradicional`,
asi.servicio AS Servicio,

#a.no_temporario_plus AS `N° Temporario 1 plus`,
164614345 AS `N° Temporario 1 plus`,
#a.prima_temporario_sin_iva_plus AS `Prima sin IVA Plus`,
1404492 AS `Prima sin IVA Plus`,
#a.prima_temporario_plus AS `Prima Plus`,
1695146 AS `Prima Plus`,
#a.suma_asegurada AS `suma aseguadora`
56500000 AS `suma aseguadora`

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
  AND A.Placa = 'DFQ758';