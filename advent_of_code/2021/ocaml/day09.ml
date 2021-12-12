open Core;;

type position = int * int

let idx_to_pos _ width index = (index / width, index mod width)

let pos_to_idx _ width (row, col) = row * width + col

let idx_is_valid height width idx = 0 <= idx && idx < height * width

let pos_is_valid height width (row, col) =
  0 <= row && row < height && 0 <= col && width < col

let valid_neighbours height width idx =
  let row, col = idx_to_pos height width idx in
  let neighbours = ref [] in
  if row >= 1          then neighbours := (idx - width) :: !neighbours;
  if col >= 1          then neighbours := (idx - 1)     :: !neighbours;
  if row <= height - 2 then neighbours := (idx + width) :: !neighbours;
  if col <= width - 2  then neighbours := (idx + 1)     :: !neighbours;
  !neighbours

let all_valid_indices height width  =
  List.init (height * width) ~f:Fun.id

let indices_not_nine data height width =
  List.filter (all_valid_indices height width)
    ~f:(fun idx -> data.(idx) <> 9)

let get_low_points data idxs_not_nine height width =
  List.filter idxs_not_nine
    ~f:(fun idx -> 
      List.for_all (valid_neighbours height width idx)
        ~f:(fun neighbour -> data.(idx) < data.(neighbour))
    )

(** recursively traverses the basin to find all points it contains *)
let rec traverse_basin idx data height width basin_points =
  if data.(idx) = 9 || Set.mem basin_points idx then basin_points else
  let valid = List.filter (valid_neighbours height width idx) 
    ~f:(fun n -> data.(n) <> 9 && not(Set.mem basin_points n)) in
  List.fold valid  (* :pog: *)
    ~init:(Set.add basin_points idx)
    ~f:(fun new_basin_pts neighbour ->
        traverse_basin neighbour data height width new_basin_pts
    )

let q1 data low_points =
  List.map low_points ~f:(fun idx -> data.(idx) + 1)
  |> List.fold ~init:0 ~f:(+)

let q2 data low_points height width =
  let basin_sizes = List.map low_points 
    ~f:(fun idx ->
      traverse_basin idx data height width (Set.empty (module Int))
      |> Set.length
    ) in
  let sorted_basin_sizes = List.sort basin_sizes
    ~compare:(fun first second -> Int.compare second first) in
  match sorted_basin_sizes with
  | first :: second :: third :: _ -> first * second * third
  | _ -> 0

let parse_data input =
  let list_of_arrays = List.map 
    ~f:(fun n -> String.strip n |> String.to_array |> Array.map ~f:(fun n -> int_of_char n - 48))
    input in
  let height = List.length list_of_arrays in
  let width = Array.length (List.hd_exn list_of_arrays) in
  Array.concat list_of_arrays, height, width

let run filename =
  let data, height, width = parse_data (In_channel.read_lines filename) in
  let pos_not_nine = indices_not_nine data height width in
  let low_points = get_low_points data pos_not_nine height width in
  (q1 data low_points, q2 data low_points height width)
