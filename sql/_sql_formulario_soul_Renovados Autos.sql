SELECT 
placa,
fecha_de_asignacion,
tipo_identificacion,
no_identificacion,
nombre,
fecha_de_nacimiento,
no_celular,
no_telefono2,
correo_electronico,
telefono_actualizado,
correo_electronico_actualizado,
chasis,
motor,
plan,
no_poliza,
inicio_renovacion,
valor_asegurado,
valor_prima,
oneroso,
nombre_agente,
sarlaft_tomador,
sarlaft_asegurado
FROM bbdd_cos_bog_grupo_axa.tb_asignacion_renovados_autos_v2
WHERE periodo = '202510'
and nombre_base = 'Base call center renovados 700 reg 20 Octubre 2025 Aptos';