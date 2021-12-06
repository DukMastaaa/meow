open Core;;


(* let transition counter = *)



(* let general_solution data iterations = 1 *)

let rec compose_n_times n f init =
  if n = 0 then f init else compose_n_times (n-1) f (f init) 

let print_array arr =
  Array.iter ~f:(Printf.printf "%d ") !arr

let parse_data raw_input =
  let counter = ref [| 0; 0; 0; 0; 0; 0; 0; 0; 0; |] in
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
  (* (general_solution data 80, general_solution data 256) *)
  (!data.(1), !data.(1))