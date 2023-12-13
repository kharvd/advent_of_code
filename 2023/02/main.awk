BEGIN {
    FS = ":|;";
}

{
    gc["red"] = 0;
    gc["green"] = 0;
    gc["blue"] = 0;

    for (i = 2; i <= NF; i++) {
        num_colors = split($i, g, ",");
        for (j = 1; j <= num_colors; j++) {
            split(g[j], h, " ");
            gc[h[2]] = gc[h[2]] < h[1] ? h[1] : gc[h[2]];
        }
    }

    split($1, game_id, " ");

    printf "%s ", game_id[2];
    if (gc["red"] > 12 || gc["green"] > 13 || gc["blue"] > 14) {
        printf "impossible\n";
    } else {
        printf "possible\n";
        sum += game_id[2];
    }
}

END {
    printf "sum: %s\n", sum;
}
