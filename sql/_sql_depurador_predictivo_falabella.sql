with base as (
    select *,
        case 
            -- exclusiones_general
            when tipificacion_mejor_gestion REGEXP 'Venta'
            OR tipificacion_ultima_gestion REGEXP 'Venta'
			OR placa IN (SELECT placa FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos WHERE periodo IN (
#            202507 
            202508
				)
            )
            then 1 
            else 0 
        end as exclusiones_general
    from bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_coalesce
    where 
    periodo IN (
#    '202507'
    '202508'
    )
),
consolidados as (
    select *,
        max(exclusiones_general) over(partition by co_id) as exclusion_total,
        row_number() over(partition by co_id order by fecha_ultima_gestion asc) as orden
    from base
)
select 
*
from consolidados
WHERE 1 = 1
  AND orden = 1
  AND exclusion_total = 0
  AND (
        vicidial_calls <= 0
        OR tipificacion_mejor_gestion IS NULL
      )
  AND fecha_fin_vigencia_actual >= (CURDATE() + INTERVAL 1 DAY)
  AND fecha_fin_vigencia_actual <= (CURDATE() + INTERVAL 15 DAY)

ORDER BY  fecha_asignacion DESC, vicidial_calls asc, tipificacion_ultima_gestion ASC, co_id asc;