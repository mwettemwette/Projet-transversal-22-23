#!/bin/bash

function verif_prog_running ()
{
    if pgrep "$1" >/dev/null; then
        return 0
    else
        return 1
    fi
}

cd Desktop

python3 envoie.py
run=true

while run
do
    # événement de clavier non bloquant
    read -t 0.1 input

    if [[ -n "$input" ]]; then

        if [ "$input" -eq "k" ];then

            #On kill le code python
            pid=$(pgrep monprogramme)
            # on demande l'arrêt gentilment
            kill "$pid"

            # on vérif si le programe c'est bien arrêté
            if [ "$(verif_prog_running "envoi.py" )" -eq 1];then
                #arrêt immédiat
                kill -SIGKILL "$pid"
            else 
                echo "prog terminé"
            fi

            # on sort du while
            run=false
        fi
    else
        echo "Aucun événement de clavier détecté"
    fi
done