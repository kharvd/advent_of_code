use std::io;

fn parse_line(s: &str) -> Vec<i64> {
    s.split_whitespace().map(|s| s.parse().unwrap()).collect()
}

fn read_input() -> Vec<Vec<i64>> {
    io::stdin()
        .lines()
        .map(|l| parse_line(&l.unwrap()))
        .collect::<Vec<_>>()
}

fn is_safe(report: &Vec<i64>, skip: Option<usize>) -> bool {
    let filtered = report.iter().enumerate().filter_map(|(i, x)| match skip {
        Some(ii) if ii == i => None,
        _ => Some(x),
    });
    let diffs = filtered
        .clone()
        .zip(filtered.clone().skip(1))
        .map(|(x1, x2)| x2 - x1);

    let max = diffs.clone().max().unwrap();
    let min = diffs.min().unwrap();
    ((1..=3).contains(&max) && (1..=3).contains(&min))
        || ((-3..=-1).contains(&max) && (-3..=-1).contains(&min))
}

fn is_safe_dampened(report: &Vec<i64>) -> bool {
    is_safe(report, None) || (0..report.len()).any(|skip| is_safe(report, Some(skip)))
}

fn part1() -> usize {
    let reports = read_input();
    reports
        .iter()
        .filter(|report| is_safe(report, None))
        .count()
}

fn part2() -> usize {
    let reports = read_input();
    reports
        .iter()
        .filter(|report| is_safe_dampened(report))
        .count()
}

fn main() {
    let part = &std::env::args().collect::<Vec<_>>()[1];
    if part == "1" {
        println!("part1: {}", part1());
    } else {
        println!("part2: {}", part2());
    }
}
