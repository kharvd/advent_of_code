use std::io::{self, Read};

use regex::{Captures, Regex};

fn read_input() -> String {
    let mut result = String::new();
    io::stdin().read_to_string(&mut result).unwrap();
    result
}

fn multiply(r: Captures) -> i64 {
    r.get(1).unwrap().as_str().parse::<i64>().unwrap()
        * r.get(2).unwrap().as_str().parse::<i64>().unwrap()
}

fn part1() -> i64 {
    let s = read_input();
    let pat = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    pat.captures_iter(&s).map(multiply).sum()
}

fn part2() -> i64 {
    let s = read_input();
    let pat = Regex::new(r"(?:mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))").unwrap();
    pat.captures_iter(&s)
        .scan(true, |on, capt| {
            match capt.get(0).unwrap().as_str() {
                "do()" => *on = true,
                "don't()" => *on = false,
                _ if *on => return Some(multiply(capt)),
                _ => {}
            }
            Some(0)
        })
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
