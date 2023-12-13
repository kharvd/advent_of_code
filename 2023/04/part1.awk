BEGIN { FS = ":|\\|" }

{
    split($2, winning, " ");
    for (i in winning) {
        win[winning[i]] = 1;
    }

    round_points = 0;

    split($3, given, " ");
    for (i in given) {
        if (win[given[i]] == 1) {
            round_points++;
        }
    }

    round_points = round_points > 0 ? (2 ^ (round_points - 1)) : 0;
    sum += round_points;

    delete win;
}
END {
    print sum;
}
