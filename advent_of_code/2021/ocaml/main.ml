open Core;;

let get_answer day_number run_test_input =
  let filename = 
    "../input/" 
    ^ (if day_number < 10 then "0" else "")
    ^ string_of_int day_number
    ^ (if run_test_input then "test" else "")
    ^ ".txt"
  in
  match day_number with
  | 1 -> Some (Day01.run filename)
  | 2 -> Some (Day02.run filename)
  (* | 4 -> Some (Day04.run filename) *)
  | 6 -> Some (Day06.run filename)
  | 7 -> Some (Day07.run filename)
  | 9 -> Some (Day09.run filename)
  | _ -> None

let print_answer (q1ans, q2ans) = Printf.printf "Q1: %d\nQ2: %d\n" q1ans q2ans

let solution_runner day_number run_test_input =
  try
    let start_time = Time.now () in
    let result = get_answer day_number run_test_input in
    let elapsed_time = Time.diff (Time.now ()) start_time |> Time.Span.to_string in
    match result with
    | Some answer -> print_answer answer;
                     Printf.printf "Time elapsed: %s\n" elapsed_time
    | None -> Printf.printf "No solution for day %d.\n" day_number
  with Sys_error s -> Printf.printf "No test input for day %d.\nError: %s\n" day_number s

let command =
  Command.basic
    ~summary:"Run Advent of Code solutions"
    Command.Let_syntax.(
      let%map_open
        day_number =
          anon ("day_number" %: int)
        and run_test_input = flag "--test" no_arg ~doc:"Use test input instead of real puzzle input"
      in
      fun () ->
        solution_runner day_number run_test_input
    )

let () =
  Command.run command ~version:"1.0" ~build_info:"dune"
