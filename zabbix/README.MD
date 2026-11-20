# Monitoreo Zabbix - SDN DMVPN Dual Hub

Exportaciones de Zabbix 7.0: seis hosts R1-R6, grupo SDN-Routers, plantilla Cisco IOS by SNMP (referencia), 22 items personalizados y 22 triggers. R7 no figura en esta exportacion.

## Importacion
1. Verificar que la plantilla Cisco IOS by SNMP exista en Zabbix.
2. Importar zbx_export_hosts.yaml desde Data collection > Hosts > Import.
3. Configurar en cada host las macros {$SNMP_AUTH_PASSPHRASE} y {$SNMP_PRIV_PASSPHRASE} de tipo Secret text con las claves reales del dispositivo, o sustituir las referencias en la interfaz SNMP de forma privada. No publicar valores reales.
4. Importar zbx_export_maps.yaml desde Monitoring > Maps > Import despues de importar los hosts y triggers.

La exportacion no incluye el dashboard, historial de metricas ni la plantilla completa. La importacion no se ha probado en otra instancia.
