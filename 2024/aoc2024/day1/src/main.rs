use std::io;

fn parse_line(s: &str) -> (u64, u64) {
    let (a, b) = s.split_once("   ").unwrap();
    (a.parse().unwrap(), b.parse().unwrap())
}

fn read_input() -> (Vec<u64>, Vec<u64>) {
    let (vec1, vec2): (Vec<u64>, Vec<u64>) =
        io::stdin().lines().map(|l| parse_line(&l.unwrap())).unzip();

    (vec1, vec2)
}

fn part1() -> u64 {
    let (mut vec1, mut vec2) = read_input();
    vec1.sort();
    vec2.sort();

    vec1.iter().zip(vec2).map(|(x, y)| x.abs_diff(y)).sum()
}

fn part2() -> u64 {
    let (vec1, vec2) = read_input();
    vec1.iter()
        .map(|x| (vec2.iter().filter(|y| *y == x).count() as u64) * x)
        .sum()
}

fn main() {
    let part = &std::env::args().collect::<Vec<_>>()[1];
    if part == "1" {
        println!("part1: {}", part1());
    } else {
        println!("part2: {}", part2());
    }
}
