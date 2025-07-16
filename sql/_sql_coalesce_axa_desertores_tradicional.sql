SELECT 
    contrato,
    anio,
    
    tipo,
    plan,
    frecuencia_de_pago,
    tarifa,
    nombre_colectivo,
    
    tipo__identificacion_beneficiario,
    no_identificacion_colectivo,
    tipo_identificacion_contrante,
    no_identificacion_contrante,
    
    primer_apellido,
    segundo_apellido,
    nombres,
    CONCAT(nombres, ' ', primer_apellido, ' ', segundo_apellido) AS nombre_completo,
    correo_electronico,
	IF(celular REGEXP '^(3[0-9]{9}|60[0-9]{8})$', celular, NULL) AS celular,
	IF(celular_2 REGEXP '^(3[0-9]{9}|60[0-9]{8})$', celular_2, NULL) AS celular_2,
	IF(telefono_fijo REGEXP '^(3[0-9]{9}|60[0-9]{8})$', telefono_fijo, NULL) AS telefono_fijo,
	IF(telefono_3 REGEXP '^(3[0-9]{9}|60[0-9]{8})$', telefono_3, NULL) AS telefono_3,
	IF(telefono_4 REGEXP '^(3[0-9]{9}|60[0-9]{8})$', telefono_4, NULL) AS telefono_4,
	IF(telefono_5 REGEXP '^(3[0-9]{9}|60[0-9]{8})$', telefono_5, NULL) AS telefono_5,
	IF(telefono_correspondencia REGEXP '^(3[0-9]{9}|60[0-9]{8})$', telefono_correspondencia, NULL) AS telefono_correspondencia,

    direccion_correspondencia,
    cod_ciudad_correspondencia,
    
    dia_de_gestion,
    mes_envio,
    mes_gestion_emermedica,
    tipo_consulta,
    sucursal,
    tipologia_contactabilidad,
    observacion,
    fecha_asignacion,
    
    asesor,
    director,
    clave,
    clave_director,
    
    periodo,
    nombre_base,
    hoja

FROM
    bbdd_cos_bog_grupo_axa.tb_asignacion_desertores_tradicional_v2
	WHERE periodo = DATE_FORMAT('2025-07-01','%%Y%%m')