SELECT *
    FROM bbdd_cos_bog_grupo_axa.tb_asignacion_bienvenida_tradicional_v2_coalesce
    WHERE periodo = 202510
    AND nombre_base = 'Bienvenida tradicional 9102025 325 reg'
    AND tipo_phone='celular'
    ORDER BY fecha_asignacion desc
;