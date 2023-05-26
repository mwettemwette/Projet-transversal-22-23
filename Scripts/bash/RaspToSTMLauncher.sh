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

chmod u+x envoie.py

python3 envoie.py
run=true

while run
do
    # événement de clavier non bloquant
    read -t 0.1 input

    #si l'input n'est pas vide
    if [[ -n "$input" ]]; then

        #si l'input est un k 
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