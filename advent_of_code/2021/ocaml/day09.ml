open Core;;

type position = int * int

(* let print_position (row, col) =
  Printf.printf "(%d, %d)\n" row col

let print_pos_list l =
  List.iter l ~f:print_position

let print_array2 arr =
  Array.iter arr
    ~f:(fun row ->
      Array.iter row
        ~f:(fun num ->
          Printf.printf "%d " num
        );
      Printf.printf "\n"
    );
  Printf.printf "\n" *)

let at_array2 data (row, col) = data.(row).(col)

let pos_is_valid height width (row, col) =
  0 <= row && row < height && 0 <= col && col < width

let neighbours (row, col) = [(row-1, col); (row+1, col); (row, col-1); (row, col+1)]

let valid_neighbours pos height width =
  List.filter (neighbours pos) ~f:(pos_is_valid height width) 

let all_valid_positions height width  =
  List.init (height * width) ~f:(fun n -> (n / width, n mod width))

let positions_not_nine data height width =
  List.filter (all_valid_positions height width)
    ~f:(fun pos -> at_array2 data pos <> 9)

let get_low_points data pos_not_nine height width =
  List.filter pos_not_nine
    ~f:(fun pos -> 
      List.for_all (valid_neighbours pos height width)
        ~f:(fun neighbour -> (at_array2 data pos) < (at_array2 data neighbour))
    )

let rec check_pos pos data height width basin_points =
  if at_array2 data pos = 9 || Set.Poly.mem basin_points pos
    then basin_points
  else 
  List.map (valid_neighbours pos height width)
    ~f:(fun neighbour ->
      check_pos neighbour data height width (Set.Poly.add basin_points pos)
  )
  |> List.fold ~init:Set.Poly.empty ~f:Set.Poly.union

let q1 data low_points =
  List.map low_points ~f:(fun pos -> at_array2 data pos + 1)
  |> List.fold ~init:0 ~f:(+)

let q2 data low_points height width =
  let sorted_basin_sizes = List.map low_points 
      ~f:(fun pos ->
        let basin_points = check_pos pos data height width (Set.Poly.empty) in
        Set.length basin_points
      )
    |> List.sort ~compare:(fun first second -> Int.compare second first) in
  match sorted_basin_sizes with
  | first :: second :: third :: _ -> first * second * third
  | _ -> 0

let parse_data input =
  List.to_array @@ List.map 
    ~f:(fun n -> String.strip n |> String.to_array |> Array.map ~f:(fun n -> int_of_char n - 48))
    input

let run filename =
  let data = parse_data (In_channel.read_lines filename) in
  let height = Array.length data in
  let width = Array.length data.(0) in
  let pos_not_nine = positions_not_nine data height width in
  let low_points = get_low_points data pos_not_nine height width in
  (* print_array2 data;
  Printf.printf "low_points\n";
  print_pos_list low_points;
  Printf.printf "pos_not_nine\n";
  print_pos_list pos_not_nine;
  Printf.printf "all_valid_positions\n";
  print_pos_list (all_valid_positions height width); *)
  (q1 data low_points, q2 data low_points height width)
