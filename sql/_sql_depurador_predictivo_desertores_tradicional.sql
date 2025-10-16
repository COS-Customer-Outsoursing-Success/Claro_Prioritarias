SELECT
    contrato,
    phone,
    primer_apellido,
    direccion_correspondencia,
    sucursal,
    correo_electronico,
    no_identificacion_contrante,
    nombres,
    contrato

FROM bbdd_cos_bog_grupo_axa.tb_asignacion_desertores_tradicional_v2_coalesce
where periodo = 202510 
    and tipo_phone = 'celular' 
    and nombre_base = 'Bienvenida tradicional 9102025 152 reg'
    ORDER BY fecha_asignacion desc
;

