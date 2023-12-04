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

// For x == (y), returns y.
#define UNWRAP(...) UNWRAP_HELPER(__VA_ARGS__)
#define UNWRAP_HELPER(x) XEVAL0 x
// Tests:
// UNWRAP((x, y))



#define Game LITOPEN
#define COLON LITCOMMA LITOPEN PARSE OPEN
#define EOL CLOSE LITCLOSE LITCLOSE
#define COMMA CLOSE PARSE OPEN
#define SEMICOLON CLOSE LITCLOSE LITOPEN PARSE OPEN

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

#define WORDCOMBO(number, colour) WORDCOMBO_##colour OPEN number CLOSE
#define WORDCOMBO_red(number) LITOPEN number LITCOMMA 0 LITCOMMA 0 LITCLOSE
#define WORDCOMBO_green(number) LITOPEN 0 LITCOMMA number LITCOMMA 0 LITCLOSE
#define WORDCOMBO_blue(number) LITOPEN 0 LITCOMMA 0 LITCOMMA number LITCLOSE

#define PARSE(tokens) APPLY(WORDCOMBO, WORDSPLIT(tokens))


#define INPUT Game 1 COLON 3 blue COMMA 4 red SEMICOLON 1 red COMMA 2 green COMMA 6 blue SEMICOLON 2 green EOL
// INPUT
// EVAL0(INPUT)
// EVAL0(EVAL0(INPUT))

#define PARSED_INPUT EVAL1(INPUT)

// PARSED_INPUT


// For ... = (x, y), returns (first(x), second(y)).
#define MAP_PAIR(first, second, ...) MAP_PAIR_HELPER(first, second, __VA_ARGS__)
#define MAP_PAIR_HELPER(first, second, tuple) 



// #define TEST(n, ...) n before TEST2(__VA_ARGS__) after
// #define TEST2(x) meow x beans
// TEST (3,((0,0,1)(0,1,0))((1,0,0)))
