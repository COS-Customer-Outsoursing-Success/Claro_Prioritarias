SELECT 
numero_de_poliza_o_contrato AS `Número del caso`,
 numero_del_caso AS `Número del caso`,
 documento AS `Número de documento del tomador`,
 nombre_del_tomador AS `Nombre del tomador`,
 apellido_del_tomador AS `Apellido del tomador`,
 celular_del_tomador AS `Celular del tomador`,
 correo_electronico_del_tomador AS `Correo electrónico del tomador`,
 placa AS Placa,
 ramo AS Ramo,
 tipo_de_tramite AS `Tipo de Trámite`,
 subtipologia AS Subtipologia,
 estado AS Estado,
 sucursal AS Sucursal,
 propietario_del_caso__nombre_completo AS `Propietario del caso: Nombre completo`,
 cola_de_gestion AS `Cola de Gestión`,
 horaenproceso AS `Hora En Proceso`,
 motivo_de_cancelacion AS `Motivo de cancelación` 
FROM bbdd_cos_bog_grupo_axa.tb_asignacion_desertores_whatsapp_v2
WHERE periodo = '202508'