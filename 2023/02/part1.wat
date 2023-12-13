(module
  (import "js" "mem" (memory 1))

  (global $line_index (mut i32) (i32.const 0))

  (func $atoi (result i32)
    (local $s i32)
    (local $res i32)

    (local.set $s (global.get $line_index))
    (local.set $res (i32.const 0))

    (block $break
      (loop $loop
        ;; if (!isdigit(str[s])) break;
        (br_if $break
          (i32.or
            (i32.lt_u (i32.load8_u (local.get $s)) (i32.const 48))
            (i32.gt_u (i32.load8_u (local.get $s)) (i32.const 57))
          )
        ) 
        ;; res = res * 10 + str[s] - '0';
        (local.set $res
          (i32.add
            (i32.mul (local.get $res) (i32.const 10))
            (i32.sub (i32.load8_u (local.get $s)) (i32.const 48))
          )
        )
        ;; s++;
        (local.set $s (i32.add (local.get $s) (i32.const 1)))

        (br $loop)
      )
    )

    (global.set $line_index (local.get $s))

    (local.get $res)
  )

  (func $readColor (param $s i32) (result i32)
    (local $col i32)
    (local $ch i32)
    
    (local.set $ch (i32.load8_u (local.get $s)))

    (i32.eq (local.get $ch) (i32.const 0x72))
    if
      i32.const 0
      return
    end

    (i32.eq (local.get $ch) (i32.const 0x67))
    if
      i32.const 1
      return
    end

    (i32.eq (local.get $ch) (i32.const 0x62))
    if
      i32.const 2
      return
    end

    i32.const 3
  )

  (func $isDigit (param $ch i32) (result i32)
    (i32.and
      (i32.le_u (local.get $ch) (i32.const 0x39))
      (i32.ge_u (local.get $ch) (i32.const 0x30))
    )
  )

  (func $isLineValid (result i32)
    (local $max_red i32)
    (local $max_green i32)
    (local $max_blue i32)
    (local $ch i32)
    (local $curr_number i32)
    (local $curr_color i32)

    (local.set $max_red (i32.const 0))
    (local.set $max_green (i32.const 0))
    (local.set $max_blue (i32.const 0))

    (block $line_break
      (loop $line_loop
        (local.tee $ch (i32.load8_u (global.get $line_index)))

        (i32.eq (local.get $ch) (i32.const 0x0a))
        if
          (global.set $line_index (i32.add (global.get $line_index) (i32.const 1)))
          br $line_break
        end

        (i32.eqz (call $isDigit))
        if
          (global.set $line_index (i32.add (global.get $line_index) (i32.const 1)))
          br $line_loop
        end

        (local.set $curr_number (call $atoi))
        (global.set $line_index (i32.add (global.get $line_index) (i32.const 1)))

        (local.set $curr_color (call $readColor (global.get $line_index)))
        
        (i32.and
          (i32.eq (local.get $curr_color) (i32.const 0))
          (i32.ge_u (local.get $curr_number) (local.get $max_red))
        )
        if
          (local.set $max_red (local.get $curr_number))
        end

        (i32.and
          (i32.eq (local.get $curr_color) (i32.const 1))
          (i32.ge_u (local.get $curr_number) (local.get $max_green))
        )
        if
          (local.set $max_green (local.get $curr_number))
        end

        (i32.and
          (i32.eq (local.get $curr_color) (i32.const 2))
          (i32.ge_u (local.get $curr_number) (local.get $max_blue))
        )
        if
          (local.set $max_blue (local.get $curr_number))
        end

        (br $line_loop)
      )
    )

    (i32.and 
      (i32.and
        (i32.le_u (local.get $max_red) (i32.const 12))
        (i32.le_u (local.get $max_green) (i32.const 13))
      )
      (i32.le_u (local.get $max_blue) (i32.const 14))
    )
    if
      i32.const 1
      return
    end    

    i32.const 0
  )

  (func $main (param $len i32) (result i32)
    (local $game_i i32)
    (local $sum_valid i32)
    (global.set $line_index (i32.const 0))

    (block $outer_break
      (loop $outer_loop
        (br_if $outer_break (i32.eq (global.get $line_index) (local.get $len)))

        (global.set $line_index (i32.add (global.get $line_index) (i32.const 5)))

        call $atoi
        local.set $game_i

        call $isLineValid
        if
          (local.set $sum_valid (i32.add (local.get $sum_valid) (local.get $game_i)))
        end

        br $outer_loop
      )
    )

    (local.get $sum_valid)
  )


  (export "main" (func $main))
)
