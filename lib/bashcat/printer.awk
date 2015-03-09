#!/usr/bin/awk -f

s ~ /printer.awk/ { exit }
f ~ /bashcat\/helper\.sh/ { exit }

NR == l {
    printf "BASHCAT:::%s:::%s:::%s:::%s:::BASHCAT\n",\
        f, l, gensub(/\n.*/, "", "ms", s), $0;
    exit;
}
