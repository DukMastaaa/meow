#define BLANK
#define OPEN (
#define CLOSE )
#define LITOPEN (
#define LITCLOSE )
#define LITCOMMA ,

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
#define DEFERAPPLY(F, ...) F BLANK (__VA_ARGS__)
#define DEFERNOPAREN(F, x) F BLANK x

// #define CONSUME_GAME(...) CONSUME_GAME_##__VA_ARGS__
// #define CONSUME_GAME_Game
// #define PARSE_GAME_NUMBER_1 (1) WRAP OPEN
// #define PARSE_GAME_NUMBER_2 (2) WRAP OPEN
// #define WRAP(x) meow x beans
// #define SPLIT(...) SWAPCAT(CAT(PARSE_NUMBER_, CONSUME_GAME(__VA_ARGS__)), meow)
// #define MACHINE(...) EVAL0(CAT(PARSE_GAME_NUMBER_, CONSUME_GAME(__VA_ARGS__)) CLOSE)

#define Game LITOPEN
#define COLON LITCOMMA LITOPEN FOO OPEN
#define EOL CLOSE LITCLOSE LITCLOSE
#define COMMA CLOSE FOO OPEN
#define SEMICOLON CLOSE LITCLOSE LITOPEN FOO OPEN



// #define GET_COLOUR(tokens) CAT(GET_COLOUR_, tokens)
// #define GET_COLOUR_red red CLOSE
// #define GET_COLOUR_green green CLOSE
// #define GET_COLOUR_blue blue CLOSE
// GET_COLOUR(blue beans blah blah)



// goal: parse "3 blue" into (0,0,3), "4 red" into (4,0,0), "2 green" into (0,2,0)


// #define WORDSPLIT(tokens) EVAL0(CAT(COMMA_AFTER_NUMBER_, tokens))
#define WORDSPLIT(tokens) CAT(COMMA_AFTER_NUMBER_, tokens)
#define COMMA_AFTER_NUMBER_0 0 LITCOMMA
#define COMMA_AFTER_NUMBER_1 1 LITCOMMA
#define COMMA_AFTER_NUMBER_2 2 LITCOMMA
#define COMMA_AFTER_NUMBER_3 3 LITCOMMA
#define COMMA_AFTER_NUMBER_4 4 LITCOMMA
#define COMMA_AFTER_NUMBER_5 5 LITCOMMA
#define COMMA_AFTER_NUMBER_6 6 LITCOMMA
#define COMMA_AFTER_NUMBER_7 7 LITCOMMA
#define COMMA_AFTER_NUMBER_8 8 LITCOMMA
#define COMMA_AFTER_NUMBER_9 9 LITCOMMA

// WORDSPLIT(2 red)

#define WORDCOMBO(number, colour) WORDCOMBO_##colour OPEN number CLOSE
#define WORDCOMBO_red(number) LITOPEN number LITCOMMA 0 LITCOMMA 0 LITCLOSE
#define WORDCOMBO_green(number) LITOPEN 0 LITCOMMA number LITCOMMA 0 LITCLOSE
#define WORDCOMBO_blue(number) LITOPEN 0 LITCOMMA 0 LITCOMMA number LITCLOSE

// EVAL0(WORDCOMBO(3, blue))

// EVAL1(WORDCOMBO(3, blue))
// EVAL1(WORDCOMBO(4, red))
// EVAL1(WORDCOMBO(2, green))

#define FOO(tokens) APPLY(WORDCOMBO, WORDSPLIT(tokens))

// FOO(3 blue)



#define INPUT Game 1 COLON 3 blue COMMA 4 red SEMICOLON 1 red COMMA 2 green COMMA 6 blue SEMICOLON 2 green EOL
// #define INPUT Game 1 COLON 3 blue EOL
INPUT
EVAL0(INPUT)
EVAL0(EVAL0(INPUT))
// EVAL0(EVAL0(EVAL0(INPUT)))
// EVAL0(EVAL0(EVAL0(EVAL0(INPUT))))




// #define TEST(n, ...) n before TEST2(__VA_ARGS__) after
// #define TEST2(x) meow x beans
// TEST (3,((0,0,1)(0,1,0))((1,0,0)))
