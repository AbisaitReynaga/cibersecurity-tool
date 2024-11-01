#!/bin/bash

# Definir la ruta del archivo JSON
JSON_FILE="/home/cibersecurity-tool/web_application/data/scanning_data.json"
CONT=1
cve_list="/home/cibersecurity-tool/web_application/data/cve_data/cve_list/"
cve_data="/home/cibersecurity-tool/web_application/data/cve_data/cve_data_list/"
cve_raw="/home/cibersecurity-tool/web_application/data/cve_data/cve_raw/"
rm -r $cve_list
rm -r $cve_data
rm -r $cve_raw

mkdir $cve_list
mkdir $cve_data
mkdir $cve_raw
# Comprobar si el archivo JSON existe
if [[ ! -f "$JSON_FILE" ]]; then
    echo "Error: El archivo $JSON_FILE no existe."
    exit 1
fi

# Obtener cuántos datos registros hay en el archivo JSON
LEN_HOST=$(jq "length" "$JSON_FILE")

# Declarar un array asociativo para almacenar servicios únicos
# Declarar un array asociativo para almacenar servicios únicos
declare -A UNIQUE_SERVICES

# Analizar cada host
for ((i=0; i<LEN_HOST; i++)); do
    # Obtener la longitud de Services
    LEN_SERVICES=$(jq --argjson index "$i" '.[$index].Services | length' "$JSON_FILE")

    # Analizar cada servicio del host
    for ((j=0; j<LEN_SERVICES; j++)); do
        # Obtener el nombre del servicio sin comillas
        SERVICE_NAME=$(jq --argjson index "$i" --argjson serviceIndex "$j" '.[$index].Services[$serviceIndex].Service' "$JSON_FILE" | tr -d '"')

        # Reemplazar caracteres especiales con %
        SERVICE_NAME=$(echo "$SERVICE_NAME" | sed 's/\//%/g')

        # Filtrar el servicio de Microsoft
        if [[ "$SERVICE_NAME" != *"Microsoft"* && -n "$SERVICE_NAME" ]]; then
            # Almacenar el servicio en el array asociativo para eliminar duplicados
            UNIQUE_SERVICES["$SERVICE_NAME"]=1
        fi
    done
done


# Mostrar información sobre cada servicio único desde CVE
for service in "${!UNIQUE_SERVICES[@]}"; do
    # Usar guiones bajos o sin paréntesis en el nombre del archivo
    raw_data_file="/home/cibersecurity-tool/web_application/data/cve_data/cve_raw/${service}_raw_data.txt"
    cve_data_list_file="/home/cibersecurity-tool/web_application/data/cve_data/cve_data_list/${service}_list.txt"
    cve_list_file="/home/cibersecurity-tool/web_application/data/cve_data/cve_list/${service}_list.txt"

    # Obtener datos y guardarlos en el archivo raw_data
    curl -s "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=$service" | grep '<td valign="top"' | sed 's/^[ \t]*//' > "$raw_data_file"

    # Filtrar datos para cve_data_list
    grep '<td valign="top">' "$raw_data_file" | awk -F'[<>]' '{print $3}' > "$cve_data_list_file"

    # Filtrar datos para cve_list
    grep ">CVE" "$raw_data_file" | awk -F'[<>]' '{print $5}' > "$cve_list_file"
done
# Archivos de entrada

# Archivo de salida JSON
output_file="/home/cibersecurity-tool/web_application/data/cve_vulnerabilities.json"

# Comenzamos la estructura del JSON
echo '[{' > "$output_file"

# Iteramos sobre los archivos en cve_list
for file in "$cve_list"*; do
    file_name=$(basename "$file" _list.txt)

    # Usamos comillas dobles para permitir la expansión de la variable
    echo "  \"Service\": \"$file_name\"," >> "$output_file"
    echo "  \"Vulnerability\": [" >> "$output_file"

    total_lines=$(wc -l < "$file")
    for i in $(seq 1 $total_lines); do
        # Tomamos la línea i de cada archivo
        cve_id=$(sed -n "${i}p" "$cve_list/${file_name}_list.txt")
        description=$(sed -n "${i}p" "$cve_data/${file_name}_list.txt")

        # Escapamos caracteres especiales para JSON
        cve_id=$(echo "$cve_id" | sed 's/\\/\\\\/g; s/"/\\"/g')
        description=$(echo "$description" | sed 's/\\/\\\\/g; s/"/\\"/g')

        # Agregamos la entrada en formato JSON
        printf '    {"%s": "%s"}' "$cve_id" "$description" >> "$output_file"

        # Añadimos una coma al final si no es la última línea
        if [ "$i" -lt "$total_lines" ]; then
            echo "," >> "$output_file"
        else
            echo "" >> "$output_file"
        fi
    done
    echo "  ]" >> "$output_file"
    echo "  },{">> "$output_file"
done

echo '}]' >> "$output_file"
