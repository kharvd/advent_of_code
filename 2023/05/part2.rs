use std::io::{self, BufRead};

fn get_seeds(lines: &mut io::Lines<io::StdinLock>) -> Vec<u64> {
    let line = lines.next().unwrap().unwrap();
    line.split(": ")
        .nth(1)
        .unwrap()
        .split(" ")
        .map(|x| x.parse::<u64>().unwrap())
        .collect()
}

fn get_ranges(lines: &mut io::Lines<io::StdinLock>) -> Vec<(u64, u64, u64)> {
    lines.next();
    let mut ranges = Vec::new();
    for line in lines {
        let line = line.unwrap().trim().to_string();
        if line.is_empty() {
            break;
        }
        let parts: Vec<u64> = line.split(" ").map(|x| x.parse::<u64>().unwrap()).collect();
        ranges.push((parts[0], parts[1], parts[2]));
    }
    ranges
}

fn map(seed: u64, ranges: &Vec<(u64, u64, u64)>) -> u64 {
    for &(to, fro, l) in ranges {
        if fro <= seed && seed < fro + l {
            return to + (seed - fro);
        }
    }
    seed
}

fn main() {
    let mut lines = io::stdin().lock().lines();

    let seeds = get_seeds(&mut lines);
    lines.next();
    let seed_to_soil = get_ranges(&mut lines);
    let soil_to_fertilizer = get_ranges(&mut lines);
    let fertilizer_to_water = get_ranges(&mut lines);
    let water_to_light = get_ranges(&mut lines);
    let light_to_temperature = get_ranges(&mut lines);
    let temperature_to_humidity = get_ranges(&mut lines);
    let humidity_to_location = get_ranges(&mut lines);

    let min_location = seeds
        .iter()
        .step_by(2)
        .zip(seeds.iter().skip(1).step_by(2))
        .map(|(seed, count)| {
            (*seed..seed + count)
                .map(|seed| {
                    let soil = map(seed, &seed_to_soil);
                    let fertilizer = map(soil, &soil_to_fertilizer);
                    let water = map(fertilizer, &fertilizer_to_water);
                    let light = map(water, &water_to_light);
                    let temperature = map(light, &light_to_temperature);
                    let humidity = map(temperature, &temperature_to_humidity);
                    let location = map(humidity, &humidity_to_location);
                    location
                })
                .min()
                .unwrap()
        })
        .min()
        .unwrap();

    println!("{}", min_location);
}
