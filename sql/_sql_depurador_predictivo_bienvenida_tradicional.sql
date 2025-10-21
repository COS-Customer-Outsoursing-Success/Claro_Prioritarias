SELECT *
    FROM bbdd_cos_bog_grupo_axa.tb_asignacion_bienvenida_tradicional_v2
    WHERE periodo = 202510
    AND nombre_base IN ('Bienvenida tradicional 9102025 325 reg', 'Bienvenida tradicional 9102025 152 reg')
    ORDER BY fecha_asignacion desc
;