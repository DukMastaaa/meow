open Core

type operation =
  | Sum
  | Product
  | Minimum
  | Maximum
  | GreaterThan
  | LessThan
  | Equal

type packet_contents =
  | Literal of int
  | Operator of operation * packet list
and packet =
  { version  : int;
    contents : packet_contents;
  }

let operation_of_int = function
  | 0 -> Sum
  | 1 -> Product
  | 2 -> Minimum
  | 3 -> Maximum
  | 5 -> GreaterThan
  | 6 -> LessThan
  | 7 -> Equal
  | _ -> assert false

let string_of_operation = function
  | Sum -> "+"
  | Product -> "*"
  | Minimum -> "min"
  | Maximum -> "max"
  | GreaterThan -> ">"
  | LessThan -> "<"
  | Equal -> "="

let binary_of_hex_map = [
    '0', "0000";
    '1', "0001";
    '2', "0010";
    '3', "0011";
    '4', "0100";
    '5', "0101";
    '6', "0110";
    '7', "0111";
    '8', "1000";
    '9', "1001";
    'A', "1010";
    'B', "1011";
    'C', "1100";
    'D', "1101";
    'E', "1110";
    'F', "1111";
  ] |> Map.of_alist_exn (module Char)

let binary_of_hex s =
  String.to_list s
  |> List.map ~f:(Map.find_exn binary_of_hex_map)
  |> List.reduce_exn ~f:(^)

let int_of_binary s = int_of_string ("0b" ^ s)

let select_from_n s n =
  String.sub s ~pos:n ~len:(String.length s - n)

let rec parse_literal rest_of_string =
  let rec extract_groups s =
    let data = String.sub s ~pos:1 ~len:4 in
    let everything_else = select_from_n s 5 in
    if Char.(=) s.[0] '1' then
      let new_data, after_literal = extract_groups everything_else in
      (data ^ new_data, after_literal)
    else
      (data, everything_else) in
  let binary, after_literal = extract_groups rest_of_string in
  Literal (int_of_binary binary), after_literal

(* amt is either length or count, depending on length type id *)
and traverse_sub_packets sub_packets s current_amt total_amt amt_increment_calc =
  let this_packet, new_s = packet_of_string s in
  let new_amount = current_amt + amt_increment_calc s new_s in
  let new_sub_packets = this_packet :: sub_packets in
  let comparison = compare new_amount total_amt in
  if comparison = -1 then
    traverse_sub_packets new_sub_packets new_s new_amount total_amt amt_increment_calc
  else if comparison = 0 then
    new_sub_packets, new_s
  else
    assert false

and parse_operator rest_of_string type_id =
  let length_type_id = String.get rest_of_string 0 in
  let bits_in_constant =
    match length_type_id with
      | '0' -> 15
      | '1' -> 11
      | _ -> assert false in
  let constant = int_of_binary @@
    String.sub rest_of_string ~pos:1 ~len:bits_in_constant in
  let after_constant =
    select_from_n rest_of_string (1 + bits_in_constant) in
  let amt_increment_calc =
    match length_type_id with
      | '0' -> fun s new_s -> String.length s - String.length new_s
      | '1' -> fun _ _ -> 1
      | _ -> assert false in
  let sub_packets, after_sub_packets =
    traverse_sub_packets [] after_constant 0 constant amt_increment_calc in
  Operator (operation_of_int type_id, sub_packets), after_sub_packets

and packet_of_string s =
  let version = int_of_binary (String.sub s ~pos:0 ~len:3) in
  let type_id = int_of_binary (String.sub s ~pos:3 ~len:3) in
  let rest_of_whole_string = select_from_n s 6 in
  let contents, after_packet =
    match type_id with
      | 4 -> parse_literal rest_of_whole_string
      | _ -> parse_operator rest_of_whole_string type_id in
  {version; contents}, after_packet

let rec eval p =
  let map_eval_and_reduce l ~f =
    List.map l ~f:eval |> List.reduce_exn ~f in
  let compare_sub_packets sub_packets ~cmp =
    (* sub_packets are in reverse order due to :: *)
    match sub_packets with
      | second :: first :: []
        -> if cmp (eval first) (eval second) then 1 else 0
      | _ -> assert false in
  match p.contents with
    | Literal n -> n
    | Operator (op, sub_packets) ->
      match op with
        | Sum         -> map_eval_and_reduce sub_packets ~f:(+)
        | Product     -> map_eval_and_reduce sub_packets ~f:( * )
        | Minimum     -> map_eval_and_reduce sub_packets ~f:(min)
        | Maximum     -> map_eval_and_reduce sub_packets ~f:(max)
        | GreaterThan -> compare_sub_packets sub_packets ~cmp:(>)
        | LessThan    -> compare_sub_packets sub_packets ~cmp:(<)
        | Equal       -> compare_sub_packets sub_packets ~cmp:(=)

let rec print_packet p ~print_versions =
  match p.contents with
    | Literal n -> 
      if print_versions then
        Printf.printf "([%d] %d" p.version n
      else
        Printf.printf "%d" n;
    | Operator (op, sub_packets) ->
      let op_string = string_of_operation op in
      begin
        if print_versions then 
          Printf.printf "([%d] %s" p.version op_string
        else 
          Printf.printf "(%s" op_string;
        List.iter sub_packets ~f:(fun sub_packet ->
          Printf.printf " "; 
          print_packet sub_packet ~print_versions;
        );
      end;
  Printf.printf ")"

let q1 whole_packet =
  let rec sum_of_versions sum {version; contents} =
    match contents with
      | Literal _
        -> sum + version
      | Operator (_, sub_packets) 
        -> sum + version + List.fold sub_packets ~init:0 ~f:sum_of_versions
    in
  sum_of_versions 0 whole_packet

let q2 whole_packet = eval whole_packet

let run filename =
  let hex = List.hd_exn (In_channel.read_lines filename) in
  let binary = binary_of_hex hex in
  let whole_packet, after_packet = packet_of_string binary in
  assert (String.is_empty after_packet || int_of_binary after_packet = 0);
  print_packet whole_packet ~print_versions:false;
  Printf.printf "\n";
  (q1 whole_packet, q2 whole_packet)
