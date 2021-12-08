(* see comments in python solution and ../07part2.png *)

open Core;;

let median l =
  let len = List.length l in
  let sorted = List.sort l ~compare:Int.compare in
  if len mod 2 = 1
    then List.nth_exn sorted (len / 2) |> float_of_int
  else 
    float_of_int 
    (List.nth_exn sorted (len / 2) + List.nth_exn sorted (len / 2 + 1)) 
    /. 2.0

let mean l =
  float_of_int (List.fold l ~init:0 ~f:(+)) /. (float_of_int @@ List.length l)

let q1objective xs y =
  List.sum (module Int) xs ~f:(fun n -> abs (n - y))

let q2objective xs y =
  List.sum (module Int) xs ~f:(fun n ->
    let d = abs (n - y) in d * (d + 1) / 2
  )

let general_solution data objective h_pos_calculator =
  let h_pos = h_pos_calculator data in
  Int.min 
    (objective data (Float.iround_up_exn   h_pos))
    (objective data (Float.iround_down_exn h_pos))

let run filename =
  let data = List.hd_exn (In_channel.read_lines filename)  
    |> String.split ~on:','
    |> List.map ~f:(fun c -> String.strip c |> int_of_string) in
  (general_solution data q1objective median, general_solution data q2objective mean)
