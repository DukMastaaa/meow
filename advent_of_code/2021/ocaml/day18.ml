open Core

(* Code adapted from zipper tutorial in http://learnyouahaskell.com/zippers *)
module Tree = struct
  type t =
    | Leaf of int
    | Internal of {left: t; right: t}
  
  type crumb =
    | LeftCrumb of t
    | RightCrumb of t
  
  type zipper = t * crumb list

  type direction =
    | Left
    | Right

  let crumb_to_direction = function
    | LeftCrumb _ -> Left
    | RightCrumb _ -> Right

  let opposite_direction = function
    | Left -> Right
    | Right -> Left

  let at_root = function
    | (Internal _, []) -> true
    | _ -> false

  let go_in_direction dir = function
    | (Leaf _, _) -> None
    | (Internal {left; right}, crumbs) ->
      match dir with
        | Left -> Some (left, LeftCrumb right :: crumbs)
        | Right -> Some (right, RightCrumb left :: crumbs)

  let go_up (tree, crumbs) = match crumbs with
    | LeftCrumb right :: more -> Some (Internal {left=tree; right}, more)
    | RightCrumb left :: more -> Some (Internal {left; right=tree}, more)
    | [] -> None

  let rec top_most = function
    | (_, []) as z -> z
    | z -> top_most (Option.value_exn (go_up z))

  let left_most_pair_at_depth threshold (tree, crumbs) =
    (* root node has 0 depth *)
    let rec helper current_depth threshold (tree, crumbs) = 
      match tree with
        | Internal {left=Leaf _; right=Leaf _} ->
          if current_depth >= threshold then Some (tree, crumbs) else None
        | Internal _ ->
          let branch dir =
            let open Option in 
            go_in_direction dir (tree, crumbs) >>= helper (current_depth + 1) threshold in
          Option.first_some (branch Left) (branch Right)
        | Leaf _ -> None in
    helper 0 threshold (tree, crumbs)
  
  let rec left_most_leaf_pred f (tree, crumbs) = match tree with
    | Leaf n -> if f n then Some (tree, crumbs) else None
    | Internal _ ->
      let branch dir =
        let open Option in
        go_in_direction dir (tree, crumbs) >>= left_most_leaf_pred f in
      Option.first_some (branch Left) (branch Right)
  
  let attach new_tree (_, crumbs) = (new_tree, crumbs)
  
  let transform_furthermost_leaf f dir (tree, crumbs) =
    let rec helper f dir tree = match tree with
    | Leaf n -> Leaf (f n)
    | Internal {left; right} ->
      match dir with
        | Left  -> Internal {left=helper f dir left; right}
        | Right -> Internal {left; right=helper f dir right} in
    helper f dir tree, crumbs
  
  let explode (tree, crumbs) = 
    (*  here, we have two things to replace:
          1. the closest leaf at the same level or below the pair
          2. the closest leaf at the same level or above the pair
        the one below can be done easily with attach_to_furthermost_leaf,
        keeping the focus in the same position.
        we'll need to zip back up to access the other pair.
    *)

    (* this preserves focus *)
    let replace_leaf_below_pair pair_dir n_left n_right parent_of_pair =
      let increment = if Caml.(=) pair_dir Left then n_right else n_left in 
      let open Option in
      parent_of_pair 
      |>  go_in_direction (opposite_direction pair_dir)
      >>| transform_furthermost_leaf ((+) increment) pair_dir 
      >>= go_up in

    (* this does NOT preserve focus *)
    let rec replace_leaf_above_pair pair_dir n_left n_right (tree, crumbs) =
      let increment = if Caml.(=) pair_dir Left then n_left else n_right in
      if at_root (tree, crumbs) then None else
      let current_dir = crumb_to_direction (List.hd_exn crumbs) in
      if Caml.(=) current_dir pair_dir
        then match go_up (tree, crumbs) with
          | Some z -> replace_leaf_above_pair pair_dir n_left n_right z
          | None -> None
      else
        let open Option in
        go_up (tree, crumbs)
        >>= go_in_direction pair_dir
        >>| transform_furthermost_leaf ((+) increment) (opposite_direction pair_dir) in

    match tree with
      | Internal {left=Leaf n_left; right=Leaf n_right} ->
        let zeroed_tree, zeroed_crumbs = attach (Leaf 0) (tree, crumbs) in
        (* exn justified since no explosions near root *)
        let parent_of_pair = Option.value_exn (go_up (zeroed_tree, zeroed_crumbs)) in
        let pair_dir = crumb_to_direction (List.hd_exn zeroed_crumbs) in
        let step_1 = replace_leaf_below_pair pair_dir n_left n_right parent_of_pair in
        let step_2 = replace_leaf_above_pair pair_dir n_left n_right (Option.value_exn step_1) in
        Option.first_some step_2 step_1

    (* | Leaf _ -> Option.value_exn (go_up (tree, crumbs)) |> explode *)
    | _ -> None

  let split (tree, crumbs) = match tree with
    | Leaf n ->
      let left = Leaf (Utils.floor_divide n 2) in
      let right = Leaf (Utils.ceil_divide n 2) in
      Internal {left; right}, crumbs
    | _ -> assert false  (* you can only split a leaf *)
  
  let add (tree1, _) (tree2, _) = Internal {left=tree1; right=tree2}, []
  
  let rec magnitude = function
    | Leaf n -> n
    | Internal {left; right} -> 3 * magnitude left + 2 * magnitude right
  
  let rec simplify z =
    let z = top_most z in
    match left_most_pair_at_depth 4 z with
      | Some new_z -> Option.value_exn (explode new_z) |> simplify
      | None ->
        match left_most_leaf_pred ((<=) 10) z with
          | Some new_z -> split new_z |> simplify
          | None -> z
  
  let parse s =
    let placeholder = Leaf 0 in
    let empty_internal = Internal {left=placeholder; right=placeholder} in
    
    let extract_int offset s =
      let extract_helper accum offset s = 
        if Char.is_digit s.[offset] then accum ^ (Char.to_string s.[offset]), offset + 1
        else accum, offset in
      let number_string, new_offset = extract_helper "" offset s in
      int_of_string number_string, new_offset in
    
    (* i really don't want to add Empty to t... *)
    (* maybe this is a bit unsafe, but its fineee *)
    let rec parse_helper z offset s =
      if offset >= String.length s then z
      else
        let open Option in
        let new_z, new_offset = match s.[offset] with
          | '[' -> 
            z |> attach empty_internal |> go_in_direction Left |> value_exn, offset + 1
          | ',' ->
            z |> go_up >>= go_in_direction Right |> value_exn, offset + 1
          | ']' ->
            z |> go_up |> value_exn, offset + 1
          | '0' .. '9' ->
            let number, off = extract_int offset s in
            z |> attach (Leaf number), off
          | ' ' -> z, offset
          | _ -> assert false in
        parse_helper new_z new_offset s in

    let initial_z = (empty_internal, [])
      |> go_in_direction Left
      |> Option.value_exn in

    parse_helper initial_z 1 s
  
  let rec print_tree = function
    | Leaf n -> Printf.printf "%d" n;
    | Internal {left; right} ->
      Printf.printf "[";
      print_tree left;
      Printf.printf ",";
      print_tree right;
      Printf.printf "]";
end;;

let q1 zippers =
  Array.reduce_exn ~f:(fun z1 z2 -> Tree.add z1 z2 |> Tree.simplify) zippers
  |> fst
  |> Tree.magnitude

let q2_brute_force zippers =
  let indices = List.range 0 (Array.length zippers) in
  let unique_pairs = List.cartesian_product indices indices
    |> List.filter ~f:(fun (x, y) -> x <> y) in
  List.map unique_pairs ~f:(fun (x, y) ->
    Tree.add zippers.(x) zippers.(y)
    |> Tree.simplify
    |> fst
    |> Tree.magnitude
  )
  |> List.max_elt ~compare
  |> Option.value_exn

let parse_data input = Array.of_list input |> Array.map ~f:Tree.parse

let run filename =
  let zippers = parse_data (In_channel.read_lines filename) in
  q1 zippers, q2_brute_force zippers
