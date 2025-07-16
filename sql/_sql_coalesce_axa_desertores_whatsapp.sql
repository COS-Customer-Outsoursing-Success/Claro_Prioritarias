SELECT 
    numero_de_poliza_o_contrato,
    anio,
    numero_del_caso,
    clave,
    periodo,
    nombre_base,
    documento,
    nombre_del_tomador,
    apellido_del_tomador,
    CONCAT(nombre_del_tomador, ' ', apellido_del_tomador) AS nombre_completo,
	IF(celular_del_tomador REGEXP '^(3[0-9]{9}|60[0-9]{8})$', celular_del_tomador, NULL) AS celular_del_tomador,
    correo_electronico_del_tomador,
    placa,
    ramo,
    tipo_de_tramite,
    subtipologia,
    estado,
    sucursal,
    propietario_del_caso__nombre_completo,
    cola_de_gestion,
    horaenproceso,
    motivo_de_cancelacion,
    fecha_asignacion
FROM
    bbdd_cos_bog_grupo_axa.tb_asignacion_desertores_whatsapp_v2
		WHERE periodo = DATE_FORMAT('2025-07-01','%%Y%%m')