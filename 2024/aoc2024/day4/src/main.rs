use std::io;

struct Field {
    data: Vec<Vec<u8>>,
}

impl Field {
    fn new(data: Vec<Vec<u8>>) -> Field {
        Field { data }
    }

    fn height(&self) -> usize {
        self.data.len()
    }

    fn width(&self) -> usize {
        self.data[0].len()
    }

    fn index(&self, i: usize, j: usize) -> Option<u8> {
        self.data.get(i)?.get(j).copied()
    }

    fn check_direction(&self, needle: &[u8], i: usize, j: usize, di: i64, dj: i64) -> bool {
        let i = i as i64;
        let j = j as i64;
        (0..needle.len()).all(|n| {
            let actual = self.index(
                (i + di * (n as i64)) as usize,
                (j + dj * (n as i64)) as usize,
            );
            let expected = needle[n];
            actual == Some(expected)
        })
    }

    fn check_index(&self, needle: &[u8], i: usize, j: usize) -> usize {
        let mut count = 0usize;
        for di in -1..=1 {
            for dj in -1..=1 {
                if self.check_direction(needle, i, j, di, dj) {
                    count += 1;
                }
            }
        }
        count
    }

    fn count_needle(&self, needle: &[u8]) -> usize {
        let mut count = 0usize;
        for i in 0..self.height() {
            for j in 0..self.width() {
                count += self.check_index(needle, i, j);
            }
        }
        count
    }

    fn count_cross(&self, needle: &[u8]) -> usize {
        let mut count = 0usize;
        for i in 0..self.height() {
            for j in 0..self.width() {
                if (self.check_direction(needle, i, j, 1, 1)
                    || self.check_direction(
                        needle,
                        i + needle.len() - 1,
                        j + needle.len() - 1,
                        -1,
                        -1,
                    ))
                    && (self.check_direction(needle, i, j + needle.len() - 1, 1, -1)
                        || self.check_direction(needle, i + needle.len() - 1, j, -1, 1))
                {
                    count += 1;
                }
            }
        }
        count
    }
}

fn read_input() -> Field {
    Field::new(
        io::stdin()
            .lines()
            .map(|s| Vec::from(s.unwrap().as_bytes()))
            .collect(),
    )
}

fn part1() -> usize {
    read_input().count_needle("XMAS".as_bytes())
}

fn part2() -> usize {
    read_input().count_cross("MAS".as_bytes())
}

fn main() {
    let part = &std::env::args().collect::<Vec<_>>()[1];
    if part == "1" {
        println!("part1: {}", part1());
    } else {
        println!("part2: {}", part2());
    }
}
