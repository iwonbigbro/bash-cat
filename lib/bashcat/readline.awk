#!/bin/awk -f

BEGIN {
    here = ""
    lineno = 0
    s = gensub(/\n.*/, "", "ms", s)
}

s ~ /readline.awk/ { exit }
f ~ /bashcat\/rcfile.sh/ { exit }

{ lineno += 1 }

here != "" && $0 == here {
    here = ""
    next
}

here != "" {
    next
}

/<</ {
    #here = gensub(/^.*<<\ *'?([^\ ']+).*/, "\\1", "")
    here = ""
}

! l || lineno == l {
    printf "BASHCAT:::%s:::%s:::%s:::%s:::BASHCAT\n", f, l, s, $0;
    
    if (l || l == 0) exit
}
