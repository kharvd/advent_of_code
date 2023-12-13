BEGIN { FS = ":|\\|" }

{
    split($1, card, " ");
    card_num = card[2];

    num_cards[card_num] += 1;

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

    delete win;

    for (i = card_num + 1; i <= card_num + round_points; i++) {
        num_cards[i] += num_cards[card_num];
    }
}

END {
    sum = 0;
    for (i in num_cards) {
        print i, num_cards[i];
        sum += num_cards[i];
    }
    print sum;
}
