WITH base AS (
    SELECT *,
        CASE 
            WHEN excluir = 1        
              OR placa IN (
					SELECT placa 
					FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos 
					WHERE periodo = 202510
              )
/*
              OR phone IN ( 
					SELECT 
						phone_number_dialed 
                    FROM bbdd_cos_bog_grupo_axa.tb_markings_2300_daily
					WHERE campana = "Falabella"
                    )
*/
            THEN 1 ELSE 0 
        END AS exclusiones_general
    FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_coalesce
    WHERE periodo = 202510
)
, consolidados AS (
    SELECT *,
           MAX(exclusiones_general) OVER(PARTITION BY placa) AS exclusion_total
    FROM base
)
SELECT 
	*
FROM consolidados 
WHERE exclusion_total = 0
and placa not in (
"KUY512",
"NLU870",
"KRU764",
"JYL272",
"FSX453",
"JPV318",
"KQN318",
"LOZ490",
"KXP290",
"FSX165",
"LJP218",
"KPV115",
"LFS968",
"NLU242",
"EPU494",
"NLZ865",
"NTY090",
"LGX998",
"NMM306",
"NIO626",
"LEQ185",
"RZL264",
"FOR387",
"LLK175",
"GZV550",
"GAX024",
"NZO872",
"NYY881",
"NYL133",
"KRT163",
"FQO300",
"NLU159",
"UGW719",
"NFN829",
"FZY765",
"EPZ196",
"NTX963",
"LIQ668",
"NUL951",
"JUP023",
"KHW821",
"NIO300",
"NLV124",
"NXV475",
"NLZ646",
"LJL730",
"NLR601",
"FQN838",
"LKY797",
"JDX924",
"NHZ216",
"NXV520",
"IOV232",
"NHX213",
"KQN185",
"LEQ311",
"GRQ486",
"LMY774",
"NTL624",
"LGK997",
"FZO977",
"DVZ858",
"JMN246",
"NNR889",
"KXR979",
"EOO822",
"IML080",
"JMT274",
"KQR122",
"LLN714",
"NTW880",
"KQN233",
"KVQ142",
"LWR715",
"NXV057",
"HBZ659",
"FZT429",
"JML543",
"UCX415",
"JYS419",
"NMM034",
"LRV194",
"IJX371",
"LTZ583",
"IMW417",
"FKL763",
"JKZ277",
"LQV114",
"KVX295",
"LSQ523",
"NHV707",
"NJP775",
"LQS797",
"LSN553",
"KRV776",
"NNP085",
"NLV601",
"JYR258",
"NUM021",
"EPL540",
"KQY503",
"EPU816",
"JEY409",
"KUP036",
"DJP960",
"KTQ175",
"MYK641",
"NTW486",
"FYO743",
"LCX237",
"NHZ179",
"GVX150",
"KSL882",
"GWT631",
"KRR465",
"KOQ808",
"NWL753",
"NON118",
"IEP915",
"MYT858",
"NUL920",
"DJY042",
"JPY941",
"GFM790",
"HZL916",
"LOM771",
"LRU981",
"LYM436",
"NGU884",
"LES521",
"LMV804",
"NTX639",
"JVO301",
"LOZ921",
"NIO559",
"KTQ248",
"HRW487",
"JSR149",
"JPV443",
"LRR057",
"LGX173",
"LIM540",
"NPQ811",
"KVS769",
"NTX449",
"UGW709",
"KOP362",
"LZY304",
"LRW024",
"NLZ683",
"JRX070",
"NYN787",
"LXV364",
"LPU385",
"IUB986"
)
#and left(no_temporario_plus, 5) = 16181
#AND tipo_phone IN ("telefono1") #,"telefono2"
#AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") 
#	BETWEEN  DATE_FORMAT("2025-10-10", "%%m%%d") AND DATE_FORMAT("2025-10-13", "%%m%%d");


-- -----------------------------------------------------------------------------------------
-- Predictivo Sin Gestion: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------
#/*
    #AND aseguradora_actual IN ("ALLIANZ", "HDI-LIBERTY")
	AND tipo_phone IN ("telefono1") #,"telefono2"
	AND (
		vicidial_calls = 0 
        OR 
        vicidial_calls IS NULL
        )
    
    AND tipificacion_mejor_gestion_soul IS NULL
          
	AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") 
	BETWEEN  DATE_FORMAT("2025-10-16", "%%m%%d") AND DATE_FORMAT("2025-10-25", "%%m%%d")
     
#   AND prioridad = "POTENCIAL PREMIUM"
#   AND prioridad IN ("ALTO POTENCIAL")
    AND prioridad = "NORMAL"

#*/

-- -----------------------------------------------------------------------------------------
-- Predictivo No Contacto: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------
/*

	and tipo_phone IN ("telefono1") #,"telefono2"
		
		AND ( 
		vicidial_calls <= 3
		#AND 
		#vicidial_calls IS NOT NULL 
		)

		AND Tipificacion_mejor_gestion_soul IN ("No Contestan") #or
        #Tipificacion_mejor_gestion_soul IS NULL)#


		AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") 
		BETWEEN  DATE_FORMAT("2025-10-14", "%%m%%d") AND DATE_FORMAT("2025-10-31", "%%m%%d")
		
	#	AND tipificacion_mejor_gestion IN ("Agent Not Available", "Agent Altnum", "No Contacto","ADAIR")    
	#	AND tipificacion_mejor_gestion NOT IN ("Agent Not Available", "Agent Altnum", "No Contacto","ADAIR")
		
	#     AND prioridad IN ("POTENCIAL PREMIUM") #   
	#	 AND prioridad IN ("ALTO POTENCIAL") #, "BUEN POTENCIAL"
	#    AND prioridad = "NORMAL"

*/

-- -----------------------------------------------------------------------------------------
-- Blaster : Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- --------------------------------------b---------------------------------------------------

/*
	AND tipo_phone IN ("telefono1") #,"telefono2"
	AND ( 
    vicidial_calls <= 3
    AND 
    vicidial_calls IS NOT NULL 
    )

    AND (
    tipificacion_mejor_gestion_soul = "No Contestan" 
    OR 
    tipificacion_mejor_gestion_soul IS NULL
    )
    
    AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") 
	BETWEEN  DATE_FORMAT("2025-09-01", "%%m%%d") AND DATE_FORMAT("2025-09-14", "%%m%%d")

    AND tipo_ultima_gestion <> "Blaster - Contacto"
    AND tipo_mejor_gestion <> "Blaster - Contacto"
*/

-- -----------------------------------------------------------------------------------------
-- Seguimientos Manuales: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------

/*
    AND vicidial_calls <= 10
	AND (tipificacion_ultima_gestion_soul IN ("Cliente solicita envío de cotización", "Llamar después")
	
    AND DATE_FORMAT(fecha_ultima_gestion_soul, "%%m%%d") 
	BETWEEN  DATE_FORMAT(CURDATE() - INTERVAL 5 DAY, "%%m%%d") AND DATE_FORMAT(CURDATE(), "%%m%%d")
    )
	
    AND (
		fecha_ultima_gestion IS NULL OR DATE(fecha_ultima_gestion) < CURDATE() - INTERVAL 2 DAY
	)
	AND (
		fecha_ultima_gestion_soul IS NULL OR DATE(fecha_ultima_gestion_soul) < CURDATE() - INTERVAL 2 DAY
	)
    
*/  

-- -----------------------------------------------------------------------------------------
-- SMS : Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------

/*
	AND tipo_phone IN ("telefono1") #,"telefono2"
	AND (vicidial_calls = 0 OR vicidial_calls IS NULL)
	AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") 
	BETWEEN DATE_FORMAT("2025-09-11", "%%m%%d") AND DATE_FORMAT("2025-09-25", "%%m%%d")
*/
-- ---------------------------------------------------------------------------- --
-- No comentar esta parte, evita que se marquen registros marcados entre hoy y ayer
-- ---------------------------------------------------------------------------- --
#/*
    AND (
		fecha_ultima_gestion IS NULL OR DATE(fecha_ultima_gestion) < CURDATE() - INTERVAL 1 DAY
	)
	AND (
		fecha_ultima_gestion_soul IS NULL OR DATE(fecha_ultima_gestion_soul) < CURDATE() - INTERVAL 1 DAY
	)


#*/
ORDER BY DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") ASC, prima_temporario_plus DESC, tasa ASC, vicidial_calls ASC, tipo_phone ASC, prioridad ASC
;