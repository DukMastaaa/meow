open Core;;

let rec q1 = function
  | first :: second :: tail -> (if second > first then 1 else 0) + q1 (second :: tail)
  | _ -> 0

(* this is essentially Rogue's solution *)
let rec q2 = function
  | first :: second :: third :: fourth :: tail -> (if fourth > first then 1 else 0) + q2 (second :: third :: fourth :: tail)
  | _ -> 0

let run filename =
  let data = List.map ~f:(fun c -> String.strip c |> int_of_string) (In_channel.read_lines filename) in
  (q1 data, q2 data)