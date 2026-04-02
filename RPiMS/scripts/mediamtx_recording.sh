#!/usr/bin/env bash

#
#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"

SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
URL="http://localhost:9997/v3/config/paths"
HEADER="Content-Type: application/json"
GET_ENDPOINT="get/cam"
PATCH_ENDPOINT="patch/cam"

record_status(){
    curl -s "${URL}"/"$GET_ENDPOINT" | jq -r '.record'
}

record_off(){
    rs=$(record_status)
    if [[ $rs == 'true' ]]; then
        response=$(curl -s -X PATCH "${URL}"/"$PATCH_ENDPOINT" \
                -H '$HEADER' -d '{"record": false}')
        r=$(echo $response | jq -r '.status')
        if [[ $r == 'ok' ]]; then echo "recording was disabled"; fi
    fi
}

record_on(){
    rs=$(record_status)
    if [[ $rs == 'false' ]]; then
        response=$(curl -s -X PATCH "${URL}"/"$PATCH_ENDPOINT" \
            -H '$HEADER' -d '{"record": true}')
        r=$(echo $response | jq -r '.status')
        if [[ $r == 'ok' ]]; then echo "recording was enabled"; fi
    fi
}

show_help(){ echo "use $SCRIPT_NAME true|false"; }

main(){
    if [[ $arg == 'true' ]]; then
        record_on
    elif [[ $arg == 'false' ]]; then
        record_off
    else
        show_help
    fi
}

arg=$1
main
