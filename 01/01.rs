use std::env;
use std::fs::read_to_string;

fn read_lines(filename: &str) -> Vec<String> {
    read_to_string(filename).unwrap().lines().map(String::from).collect()
}

fn part1_pred(c: &char) -> bool {
    c.is_digit(10)
}

fn part1(s: &String) -> u32 {
    let f = s.chars().find(part1_pred).unwrap().to_digit(10).unwrap();
    let l = s.chars().rev().find(part1_pred).unwrap().to_digit(10).unwrap();
    10 * f + l
}

fn main() {
    let args: Vec<_> = env::args().collect();
    println!("{}", read_lines(&args[1]).iter().map(part1).sum::<u32>())
}
