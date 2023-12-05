use std::cmp::{min, max};
use std::env;
use std::iter::zip;
use std::fs::read_to_string;

fn read_lines(filename: &str) -> Vec<String> {
    read_to_string(filename).unwrap().lines().map(String::from).collect()
}

fn parse_seeds(line: &String) -> Vec<(i64, i64)> {
    let numbers: Vec<_> = line.split(": ").nth(1).unwrap().split(' ').map(|s| s.parse::<i64>().unwrap()).collect();
    let starts = numbers.iter().step_by(2).copied();
    let lengths = numbers.iter().skip(1).step_by(2).copied();
    return zip(starts, lengths).map(|(s, l)| (s, s + l)).collect::<Vec<_>>()
}

fn parse_mapping_line(line: &String) -> (i64, i64, i64) {
    let values: Vec<_> = line.split(" ").map(|s| s.parse::<i64>().unwrap()).collect();
    return (values[1], values[1] + values[2], values[0] - values[1])    
}

fn parse_map(chunk: &[String]) -> Vec<(i64, i64, i64)> {
    let mut mapping_lines = chunk.iter().skip(1).map(parse_mapping_line).collect::<Vec<_>>();
    mapping_lines.sort();
    return mapping_lines
}

fn apply(data: &(i64, i64), map: &Vec<(i64, i64, i64)>) -> Vec<(i64, i64)> {
    let mut new_data = Vec::new();

    let (data_start, data_end) = data;
    let mut current_pos = *data_start;

    for mapping_line in map {
        let (source_start, source_end, diff) = mapping_line;

        if source_start >= data_end {
            break
        }

        if source_end < data_start {
            continue
        }

        if current_pos < *source_start {
            new_data.push((current_pos, *source_start))
        }

        let start_point = max(current_pos, *source_start);
        let end_point = *min(source_end, data_end);

        if *source_start < end_point {
            new_data.push((start_point + diff, end_point + diff))
        }

        current_pos = end_point
    }

    if current_pos < *data_end {
        new_data.push((current_pos, *data_end))
    }

    return new_data
}

fn main() {
    let args: Vec<_> = env::args().collect();
    let lines = read_lines(&args[1]);
    let mut chunks = lines.split(|s| s == "");

    let mut data = parse_seeds(&chunks.next().unwrap()[0]);
    let maps: Vec<_> = chunks.map(parse_map).collect();

    for map in maps {
        data = data.iter().flat_map(|d| apply(d, &map)).collect();
    }

    data.sort();

    println!("{}", data[0].0);
}
