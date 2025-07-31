WITH final AS (
    SELECT a.* 
    FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2 a
    LEFT JOIN bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos b
        ON a.placa = b.placa 
        AND a.periodo = b.periodo_asignado
    WHERE b.placa IS NULL
    AND a.periodo = '202508'
)

SELECT 
prioridad, count(*)
FROM final
GROUP BY prioridad
