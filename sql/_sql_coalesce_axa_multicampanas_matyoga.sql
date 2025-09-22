SELECT 
    periodo,
    nombre,
    plan,
    clave_asesor,
    nombre_asesor,
	IF(telefono_1 REGEXP '^(3[0-9]{9}|60[0-9]{8})$', telefono_1, NULL) AS telefono_1,
	IF(telefono_2 REGEXP '^(3[0-9]{9}|60[0-9]{8})$', telefono_2, NULL) AS telefono_2,
    IF(telefono_3 REGEXP '^(3[0-9]{9}|60[0-9]{8})$', telefono_3, NULL) AS telefono_3,
    direccion,
    correo_electronico,
    tipificacion,
    subtipificacion,
    fecha_asignacion,
    anio,
    nombre_base,
    hoja
FROM
    bbdd_cos_bog_grupo_axa.tb_asignacion_matyoga_v2
WHERE
    periodo = DATE_FORMAT('2025-09-01', '%%Y%%m')
;