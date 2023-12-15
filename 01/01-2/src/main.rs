use regex::Regex;
use std::collections::HashMap;
use std::env;
use std::fs::read_to_string;

fn read_lines(filename: &str) -> Vec<String> {
    read_to_string(filename).unwrap().lines().map(String::from).collect()
}

fn word_to_number(s: &str) -> u32 {
    match s {
        "one" | "eno" => 1,
        "two" | "owt" => 2,
        "three" | "eerht" => 3,
        "four" | "ruof" => 4,
        "five" | "evif" => 5,
        "six" | "xis" => 6,
        "seven" | "neves" => 7,
        "eight" | "thgie" => 8,
        "nine" | "enin" => 9,
        _ => s.parse::<u32>().unwrap()
   }
}

fn part2(s: &String) -> u32 {
    let re = Regex::new("(one|two|three|four|five|six|seven|eight|nine|[1-9])").unwrap();
    let f = word_to_number(re.find(s).unwrap().as_str());

    let re2 = Regex::new("(eno|owt|eerht|ruof|evif|xis|neves|thgie|enin|[1-9])").unwrap();
    let s2 = s.chars().rev().collect::<String>();
    let l = word_to_number(re2.find(&s2).unwrap().as_str());

    10 * f + l
}

fn main() {
    let args: Vec<_> = env::args().collect();
    let lines = read_lines(&args[1]);
    println!("{}", lines.iter().map(part2).sum::<u32>())
}
