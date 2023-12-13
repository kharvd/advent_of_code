BEGIN { FS = ":|;" }
{
    gc["red"] = 0; gc["green"] = 0; gc["blue"] = 0;

    for (i = 2; i <= NF; i++) {
        split($i, col, ",");
        for (j in col) {
            split(col[j], h, " ");
            gc[h[2]] = gc[h[2]] < h[1] ? h[1] : gc[h[2]];
        }
    }

    sum += gc["red"] * gc["green"] * gc["blue"];
}
END { print sum }
