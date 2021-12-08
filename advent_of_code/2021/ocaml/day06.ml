open Core;;

(* let print_array arr =
  Array.iter ~f:(Printf.printf "%d ") !arr *)

let transition counter = 
  let next_state = ref (Array.create ~len:9 0) in
  let new_element index =
    match index with
    | 8 -> !counter.(0)
    | 6 -> !counter.(7) + !counter.(0)
    | n -> !counter.(n+1)
  in
  Array.iter ~f:(fun n -> !next_state.(n) <- new_element n) (Array.init 9 ~f:Fun.id);
  next_state

let rec general_solution data iterations = 
  if iterations = 0
    then Array.fold !data ~init:0 ~f:(+)
  else general_solution (transition data) (iterations - 1)

let parse_data raw_input =
  let counter = ref (Array.create ~len:9 0) in
  Array.iter ~f:(fun n -> !counter.(n) <- !counter.(n) + 1) raw_input;
  counter

let run filename =
  let input = In_channel.read_lines filename in
  let raw_input = List.hd_exn input 
    |> String.strip 
    |> String.split ~on:',' 
    |> List.map ~f:int_of_string
    |> List.to_array in
  let data = parse_data raw_input in
  (general_solution data 80, general_solution data 256)
