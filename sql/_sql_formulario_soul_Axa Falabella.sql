SELECT 
asi.aseguradora_actual AS `Aseguradora Actual`,
asi.departamento AS Ciudades,
asi.clase_vehiculo AS `Clase de vehiculo`,
asi.cod_departamento AS `Cod Departamento`,
asi.cod_fasecolda AS `Cod Fasecolda`,
asi.cod_municipio AS `Cod Municipio`,
asi.email AS `Correo electrónico`,
asi.departamento AS Departamento,
0 AS `Diferencia con la Aseguradora Actual`,
asi.direccion AS Dirección,
asi.fecha_fin_vigencia_actual AS `Fecha Fin vigencia Actual`,
asi.fecha_fin_vigencia_actual AS `Fecha Inicio Nueva Vigencia`,
asi.fecha_nacimiento AS `Fecha Nacimiento`,
asi.genero AS Genero,
asi.linea AS Línea,
asi.marca AS Marca,
asi.modelo AS Modelo,
a.no_temporario_plus AS `N° Temporario 1 plus`,
a.no_temporario_tradicional AS `N° Temporario 1 TRADICIONAL`,
'0' AS `N° Temporario AUTOSUFICIENTE`,
asi.co_id AS `No. Documento`,
a.placa AS Placa,
0 AS `Prima Autosuficiente`,
0 AS `Prima con IVA Aseguradora Actual`,
a.prima_temporario_plus AS `Prima Plus`,
0 AS `Prima sin IVA AUTOSUFICIENTE`,
a.prima_temporario_sin_iva_plus AS `Prima sin IVA Plus`,
a.prima_tradicional_sin_iva AS `Prima sin IVA TRADICIONAL`,
a.prima_tradicional AS `Prima Tradicional`,
asi.apellido AS `Primer Apellido`,
asi.nombre AS `Primer Nombre`,
asi.segundo_apellido AS `Segundo Apellido`,
asi.segundo_nombre AS `Segundo Nombre`,
asi.servicio AS Servicio,
a.suma_asegurada AS `suma aseguadora`,
asi.telefono1 AS `Teléfono`,
asi.telefono2 AS `Teléfono 2`,
asi.telefono3 AS `Teléfono 3`,
'CC' AS `Tipo de documento`
FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_recotizada_v2 a
LEFT JOIN bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2 asi
    ON a.placa = asi.placa 
   AND a.periodo = asi.periodo
LEFT JOIN bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos npt
    ON asi.placa = npt.placa 
   AND asi.periodo = npt.periodo_asignado
WHERE a.periodo = 202508
  AND asi.periodo = 202508
  AND npt.placa IS NULL;