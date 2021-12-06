open Core;;

let get_answer day_number =
  let filename = 
    "../input/" 
    ^ (if day_number < 10 then "0" else "")
    ^ string_of_int day_number
    ^ ".txt"
  in
  match day_number with
  | 1 -> Some (Day01.run filename)
  | 2 -> Some (Day02.run filename)
  (* | 4 -> Some (Day04.run filename) *)
  | 6 -> Some (Day06.run filename)
  | _ -> None

let print_answer = function
  | (q1ans, q2ans) -> Printf.printf "Q1: %d\nQ2: %d\n" q1ans q2ans

let solution_runner day_number =
  match get_answer day_number with
  | Some answer -> print_answer answer
  | None -> Printf.printf "No solution for day %d.\n" day_number

let day_number_param =
  let open Command.Param in
  anon ("day_number" %: int)

let command =
  Command.basic
    ~summary:"Run Advent of Code solutions"
    (Command.Param.map day_number_param 
    ~f:(fun day_number -> (fun () -> solution_runner day_number)))

let () =
  Command.run command
