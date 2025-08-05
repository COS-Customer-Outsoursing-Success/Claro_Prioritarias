with base as (
    select *,
        case 
            when excluir = 1
			OR placa IN (SELECT placa FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos WHERE periodo IN (
            202508
				)
            )
            then 1 
            else 0 
        end as exclusiones_general
    from bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_coalesce
    where 
    periodo IN (
    202508
    )
),
consolidados as (
    select *,
        max(exclusiones_general) over(partition by co_id) as exclusion_total,
        row_number() over(partition by co_id order by fecha_ultima_gestion asc) as orden
    from base
)

SELECT 
*
FROM consolidados
WHERE 1 = 1
  AND orden = 1
  AND exclusion_total = 0
  AND (
        vicidial_calls <= 1
        OR tipificacion_mejor_gestion_soul IS NULL
      )
  AND DATE_FORMAT(fecha_fin_vigencia_actual, '%%m%%d') 
  BETWEEN  DATE_FORMAT(CURDATE() + INTERVAL 1 DAY, '%%m%%d') AND DATE_FORMAT(CURDATE() + INTERVAL 15 DAY, '%%m%%d')
  ORDER BY  fecha_asignacion DESC, vicidial_calls asc, tipificacion_ultima_gestion_soul ASC, co_id asc