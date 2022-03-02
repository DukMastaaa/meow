open Core

type packet = 
  { version  : int;
    contents : packet_contents;
  }
and packet_contents =
  | Sum of packet list
  | Product of packet list
  | Minimum of packet list
  | Literal of int
  | Maximum of packet list
  | GreaterThan of packet * packet
  | LessThan of packet * packet
  | Equal of packet * packet

let string_of_contents_type = function
  | Sum _ -> "+"
  | Product _ -> "*"
  | Minimum _ -> "min"
  | Maximum _ -> "max"
  | Literal _ -> ""
  | GreaterThan _ -> ">"
  | LessThan _ -> "<"
  | Equal _ -> "="

let list_from_contents = function
  | Literal _ -> []
  | Sum ps | Product ps | Minimum ps | Maximum ps -> ps
  | GreaterThan (fst, snd) | LessThan (fst, snd) | Equal (fst, snd) -> [fst; snd]

let rec parse_literal rest_of_string =
  let rec extract_groups s =
    let data = String.sub s ~pos:1 ~len:4 in
    let everything_else = Utils.select_str_from_n s 5 in
    if Char.(=) s.[0] '1' then
      let new_data, after_literal = extract_groups everything_else in
      (data ^ new_data, after_literal)
    else
      (data, everything_else) in
  let binary, after_literal = extract_groups rest_of_string in
  Literal (Utils.int_of_binary binary), after_literal

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

and packet_contents_from_list type_id sub_packets =
  match type_id with
  | 0 -> Sum sub_packets
  | 1 -> Product sub_packets
  | 2 -> Minimum sub_packets
  | 3 -> Maximum sub_packets
  | _ ->
    assert (List.length sub_packets = 2);
    (* sub_packets are in reverse order due to :: *)
    let fst = List.nth_exn sub_packets 1 in
    let snd = List.hd_exn sub_packets in
    match type_id with
      | 5 -> GreaterThan (fst, snd)
      | 6 -> LessThan (fst, snd)
      | 7 -> Equal (fst, snd)
      | _ -> assert false

and parse_operator rest_of_string type_id =
  let length_type_id = String.get rest_of_string 0 in
  let bits_in_constant =
    match length_type_id with
      | '0' -> 15
      | '1' -> 11
      | _ -> assert false in
  let constant = Utils.int_of_binary @@
    String.sub rest_of_string ~pos:1 ~len:bits_in_constant in
  let after_constant =
    Utils.select_str_from_n rest_of_string (1 + bits_in_constant) in
  let amt_increment_calc =
    match length_type_id with
      | '0' -> fun s new_s -> String.length s - String.length new_s
      | '1' -> fun _ _ -> 1
      | _ -> assert false in
  let sub_packets, after_sub_packets =
    traverse_sub_packets [] after_constant 0 constant amt_increment_calc in
  packet_contents_from_list type_id sub_packets, after_sub_packets

and packet_of_string s =
  let version = Utils.int_of_binary (String.sub s ~pos:0 ~len:3) in
  let type_id = Utils.int_of_binary (String.sub s ~pos:3 ~len:3) in
  let rest_of_whole_string = Utils.select_str_from_n s 6 in
  let contents, after_packet =
    match type_id with
      | 4 -> parse_literal rest_of_whole_string
      | _ -> parse_operator rest_of_whole_string type_id in
  {version; contents}, after_packet

let rec eval p =
  let eval_and_reduce l ~f =
    List.map l ~f:eval |> List.reduce_exn ~f in
  let compare (first, second) ~cmp =
    if cmp (eval first) (eval second) then 1 else 0 in
  match p.contents with
    | Literal n -> n
    | Sum ps -> eval_and_reduce ps ~f:(+)
    | Product ps -> eval_and_reduce ps ~f:( * )
    | Minimum ps -> eval_and_reduce ps ~f:(min)
    | Maximum ps -> eval_and_reduce ps ~f:(max)
    | GreaterThan (first, second) -> compare (first, second) ~cmp:(>)
    | LessThan (first, second) -> compare (first, second) ~cmp:(<)
    | Equal (first, second) -> compare (first, second) ~cmp:(=)

let rec print_packet {version; contents} ~print_versions =
  let packet_is_literal, literal_n = match contents with
    | Literal n -> (true, n)
    | _ -> (false, 0) in
  if not packet_is_literal || print_versions
    then Printf.printf "(";
  if print_versions
    then Printf.printf "[%d] " version;
  Printf.printf "%s" (string_of_contents_type contents);
  (* Literal _ gives [] *)
  List.iter (list_from_contents contents) ~f:(fun sub_packet ->
    Printf.printf " "; 
    print_packet sub_packet ~print_versions;
  );
  if packet_is_literal then
    Printf.printf "%d" literal_n
  else Printf.printf ")"

let q1 whole_packet =
  let rec sum_of_versions running_total {version; contents} =
    let sub_packet_total = List.fold (list_from_contents contents) ~init:0 ~f:sum_of_versions in
    running_total + version + sub_packet_total in
  sum_of_versions 0 whole_packet

let q2 whole_packet = eval whole_packet

let run filename =
  let hex = List.hd_exn (In_channel.read_lines filename) in
  let binary = Utils.binary_of_hex hex in
  let whole_packet, after_packet = packet_of_string binary in
  assert (String.is_empty after_packet || Utils.int_of_binary after_packet = 0);
  print_packet whole_packet ~print_versions:false;
  Printf.printf "\n";
  (q1 whole_packet, q2 whole_packet)
