
# /*
 SELECT
	prioridad, count(*)
 FROM consolidados
WHERE 1 = 1
  AND orden = 1
  AND exclusion_total = 0
  AND (
        vicidial_calls <= 8
        OR tipificacion_mejor_gestion_soul IS NULL
      )
  AND DATE_FORMAT(fecha_fin_vigencia_actual, '%m%d') 
  BETWEEN  DATE_FORMAT(CURDATE() + INTERVAL 1 DAY, '%m%d') AND DATE_FORMAT(CURDATE() + INTERVAL 15 DAY, '%m%d')

GROUP by prioridad
ORDER BY  fecha_asignacion DESC, vicidial_calls asc, tipificacion_ultima_gestion_soul ASC, co_id asc

#/*