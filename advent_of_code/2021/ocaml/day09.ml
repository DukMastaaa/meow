open Core;;

type position = int * int

let at_array2 data (row, col) = data.(row).(col)

let neighbours (row, col) = [(row-1, col); (row+1, col); (row, col-1); (row, col+1)]

let pos_is_valid (row, col) side_length =
  0 <= row && row < side_length && 0 <= col && col < side_length

let all_valid_positions side_length =
  List.init (side_length * side_length) ~f:(fun n -> (n / side_length, n mod side_length))

let positions_not_nine data side_length =
  List.filter (all_valid_positions side_length)
    ~f:(fun pos -> at_array2 data pos <> 9)


let get_low_points data pos_not_nine =
  List.filter pos_not_nine
    ~f:(fun pos -> 
      let valid_neighbours = List.filter (neighbours pos) ~f:pos_is_valid in
      List.reduce (neighbours pos)
    )

let q1 data low_points = 0

let q2 data low_points pos_not_nine = 0

let parse_data input =
  List.to_array @@ List.map 
    ~f:(fun n -> String.strip n |> String.to_array |> Array.map ~f:int_of_char)
    input 

let run filename =
  let data = parse_data (In_channel.read_lines filename) in
  let side_length = Array.length data in
  let pos_not_nine = positions_not_nine data side_length in
  let low_points = get_low_points data pos_not_nine in
  (q1 data low_points, q2 data low_points pos_not_nine)
  (* (int_of_string filename, 0) *)
