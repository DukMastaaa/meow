open Core;;

type state = {
  horiz: int;
  depth: int;
  aim: int;
}

type direction =
  | Down
  | Up
  | Forward

let string_to_direction = function
  | "down" -> Down
  | "up" -> Up
  | "forward" -> Forward
  | _ -> Down

let soln_from_state s =
  s.horiz * s.depth

let q1_transition s cmd =
  match cmd with
  | Down, num     -> {horiz = s.horiz; depth = s.depth + num; aim = s.aim}
  | Up, num       -> {horiz = s.horiz; depth = s.depth - num; aim = s.aim}
  | Forward, num  -> {horiz = s.horiz + num; depth = s.depth; aim = s.aim}

let q2_transition s cmd =
  match cmd with
  | Down, num     -> {horiz = s.horiz; depth = s.depth; aim = s.aim + num}
  | Up, num       -> {horiz = s.horiz; depth = s.depth; aim = s.aim - num}
  | Forward, num  -> {horiz = s.horiz + num; depth = s.depth + s.aim * num; aim = s.aim}

let general_solution transition data =
  let initial_state: state = {horiz = 0; depth = 0; aim = 0} in
  soln_from_state (
    List.fold data ~init:initial_state ~f:transition
  )

let parse_data unparsed_data =
  let parse_command command =
    match String.split command ~on:' ' with
    | [dir; num] -> (string_to_direction dir, int_of_string num)
    | _ -> (Down, 0)
  in
  List.map ~f:parse_command unparsed_data

let run filename =
  let unparsed_data = List.map ~f:String.strip (In_channel.read_lines filename) in
  let data = parse_data unparsed_data in
  (general_solution q1_transition data, general_solution q2_transition data)
