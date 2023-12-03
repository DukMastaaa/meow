#define BLANK
#define OPEN (
#define CLOSE )
#define LITOPEN (
#define LITCLOSE )

#define EVAL0(x) x
#define EVAL1(x) EVAL0(EVAL0(x))
#define EVAL2(x) EVAL1(EVAL1(x))
#define EVAL(x)  EVAL2(EVAL2(x))

#define XEVAL0(...) __VA_ARGS__
#define XEVAL1(...) XEVAL0(XEVAL0(__VA_ARGS__))
#define XEVAL2(...) XEVAL1(XEVAL1(__VA_ARGS__))
#define XEVAL(...)  XEVAL2(XEVAL2(__VA_ARGS__))

#define CAT(x, y) CAT_(x, y)
#define CAT_(x, ...) x##__VA_ARGS__

#define APPLY(F, ...) F(__VA_ARGS__)
#define DEFERNOPAREN(F, x) F BLANK x

// #define CONSUME_GAME(...) CONSUME_GAME_##__VA_ARGS__
// #define CONSUME_GAME_Game
// #define PARSE_GAME_NUMBER_1 (1) WRAP OPEN
// #define PARSE_GAME_NUMBER_2 (2) WRAP OPEN
// #define WRAP(x) meow x beans
// #define SPLIT(...) SWAPCAT(CAT(PARSE_NUMBER_, CONSUME_GAME(__VA_ARGS__)), meow)
// #define MACHINE(...) EVAL0(CAT(PARSE_GAME_NUMBER_, CONSUME_GAME(__VA_ARGS__)) CLOSE)

#define Game LITOPEN
#define COLON LITCLOSE LITOPEN LITOPEN PARSEBODY OPEN
#define PARSEBODY(x) [x]
#define EOL EOL_DUMMY CLOSE LITCLOSE LITCLOSE

// goal: parse "3 blue" into (0,0,3), "4 red" into (4,0,0), "2 green" into (0,2,0)


#define WORDSPLIT(tokens) XEVAL0(CAT(GET_NUMBER_, tokens CLOSE ) ) CLOSE
#define GET_NUMBER_1 1 , GET_COLOUR OPEN
#define GET_NUMBER_2 2 , GET_COLOUR OPEN
#define GET_NUMBER_3 3 , GET_COLOUR OPEN

#define GET_COLOUR(tokens) CAT(GET_COLOUR_, tokens)
#define GET_COLOUR_red red CLOSE
#define GET_COLOUR_green green CLOSE
#define GET_COLOUR_blue blue CLOSE
// GET_COLOUR(blue beans blah blah)

// WORDSPLIT(3 blue 2 red)

// WORDSPLIT(2 red)

#define WORDCOMBO(number, colour)     WORDCOMBO_##colour OPEN number CLOSE    hmm OPEN    WORDCOMBO_ALT BLANK OPEN WORDSPLIT OPEN
#define WORDCOMBO_ALT(number, colour) WORDCOMBO_##colour OPEN number CLOSE    hmm OPEN    WORDCOMBO BLANK OPEN WORDSPLIT OPEN
#define WORDCOMBO_red(number) LITOPEN number , 0 , 0 LITCLOSE
#define WORDCOMBO_green(number) LITOPEN 0 , number , 0 LITCLOSE
#define WORDCOMBO_blue(number) LITOPEN 0 , 0 , number LITCLOSE

// EVAL1(WORDCOMBO(3, blue))
// EVAL1(WORDCOMBO(4, red))
// EVAL1(WORDCOMBO(2, green))

// EVAL0(  WORDCOMBO BLANK OPEN WORDSPLIT(3 blue 2 red)  )
// EVAL0( EVAL0(  WORDCOMBO OPEN WORDSPLIT (3 blue 2 red)  ) )
// EVAL( EVAL0( EVAL0(  WORDCOMBO OPEN WORDSPLIT(3 blue 2 red)  ) ) )

// ( WORDCOMBO_ALT ( WORDSPLIT ( 2 red )
// ( WORDCOMBO_ALT BLANK ( WORDSPLIT ( 2 red )
//  ( ( WORDCOMBO_ALT BLANK ( WORDSPLIT ( 2 red ) )

EVAL0 (OPEN DEFERNOPAREN(WORDCOMBO, OPEN WORDSPLIT (2 red) ))

// ( WORDCOMBO_ALT ( 2 , red ) )


// #define INPUT Game 1 COLON 3 blue COMMA 4 red SEMICOLON 1 red COMMA 2 green COMMA 6 blue SEMICOLON 2 green EOL
// EVAL0(INPUT)

