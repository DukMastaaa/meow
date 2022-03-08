open Core

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

let select_str_from_n s n =
    String.sub s ~pos:n ~len:(String.length s - n)

let floor_divide x y = x / y

let ceil_divide x y =
  Float.iround_up_exn (float_of_int x /. float_of_int y)
  