#define BLANK
#define BLANK_FN()
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
#define DEFERAPPLY1(F, ...) F BLANK (__VA_ARGS__)
#define DOUBLEDEFERAPPLY(F, ...) DEFERAPPLY1(DEFERAPPLY, F, __VA_ARGS__)
#define DEFERNOPAREN(F, x) F BLANK x

// For x == (y), returns y.
#define UNWRAP(...) UNWRAP_HELPER(__VA_ARGS__)
#define UNWRAP_HELPER(x) XEVAL0 x
// Tests:
// UNWRAP((x, y))



/////// Boolean functions

#define TRUE 1
#define FALSE 0

// Returns onTrue if cond is 1 else onFalse.
#define IF(cond, onTrue, onFalse) CAT(IF_COND_, cond)(onTrue, onFalse)
#define IF_COND_1(onTrue, onFalse) onTrue
#define IF_COND_0(onTrue, onFalse) onFalse
// Tests:
// IF(1, (1,2,3), (4,5,6))     // (1,2,3)

#define IF_TRUE(cond, ...) CAT(IF_TRUE_COND_, cond)(__VA_ARGS__)
#define IF_TRUE_COND_1(...) __VA_ARGS__
#define IF_TRUE_COND_0(...)

#define IF_FALSE(cond, ...) CAT(IF_FALSE_COND_, cond)(__VA_ARGS__)
#define IF_FALSE_COND_1(...)
#define IF_FALSE_COND_0(...) __VA_ARGS__
// Tests:
// IF_FALSE(0, beans)
// IF_FALSE(1, beans)




/////// Functions to check emptiness of argument

// Returns whether the given argument is empty.
// If the argument is a function-like macro, it must expect
// either 0, 1 or a variable number of arguments.
// Copied from https://gustedt.wordpress.com/2010/06/08/detect-empty-macro-arguments/
#define ISEMPTY(...)                                                                            \
    ISEMPTY_HELPER(                                                                             \
        ISEMPTY_DETAIL_HAS_COMMA(__VA_ARGS__),                                                  \
        ISEMPTY_DETAIL_HAS_COMMA(ISEMPTY_DETAIL_TRIGGER_PARENTHESIS_ __VA_ARGS__),              \
        ISEMPTY_DETAIL_HAS_COMMA(__VA_ARGS__ (/*empty*/)),                                      \
        ISEMPTY_DETAIL_HAS_COMMA(ISEMPTY_DETAIL_TRIGGER_PARENTHESIS_ __VA_ARGS__ (/*empty*/))   \
    )
#define ISEMPTY_HELPER(_0, _1, _2, _3)                                  \
    ISEMPTY_DETAIL_HAS_COMMA(                                           \
        ISEMPTY_DETAIL_PASTE5(ISEMPTY_DETAIL_CASE_, _0, _1, _2, _3)     \
    )
#define ISEMPTY_DETAIL_ARG16(_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, ...) _15
#define ISEMPTY_DETAIL_HAS_COMMA(...) ISEMPTY_DETAIL_ARG16(__VA_ARGS__, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0)
#define ISEMPTY_DETAIL_TRIGGER_PARENTHESIS_(...) ,
#define ISEMPTY_DETAIL_PASTE5(_0, _1, _2, _3, _4) _0 ## _1 ## _2 ## _3 ## _4
#define ISEMPTY_DETAIL_CASE_0001 ,
// Tests: see blog post this was copied from.
// ISEMPTY()        // 1
// ISEMPTY(BLANK)   // 1
// ISEMPTY(())      // 0
// ISEMPTY(12 34)   // 0
// ISEMPTY(ISEMPTY_DETAIL_ARG16)  // error, see requirements on function-like macros





/////// Functions on pairs (x, y)

// Returns the first and second element.
#define FIRST_PAIR(...) FIRST_ARG __VA_ARGS__
#define FIRST_ARG(x, y) x
#define SECOND_PAIR(...) SECOND_ARG __VA_ARGS__
#define SECOND_ARG(x, y) y
// Tests:
// FIRST_PAIR((x, y))
// SECOND_PAIR((x, y))

// For ... = (x, y), returns (f(x), g(y)).
#define MAP_PAIR(f, g, ...) EVAL0(MAP_PAIR_HELPER(f, g, APPLY(UNWRAP, __VA_ARGS__)))
#define MAP_PAIR_HELPER(f, g, ...) MAP_PAIR_HELPER2(f, g, __VA_ARGS__)
#define MAP_PAIR_HELPER2(f, g, x, y) (f(x), g(y))
// Tests:
// #define DOUBLE(x) 2*x
// #define NEGATE(x) -x
// MAP_PAIR(f, g, (x, y))
// MAP_PAIR(DOUBLE, NEGATE, (x, y))



/////// Functions on sequences (a)(b)(c)

// For seq = (a)(b)(c), returns (f(a))(f(b))(f(c)).


// let's start with
// (a)(b)(c) --> f(a) f(b) f(c)

// #define MAP_SEQ(f, seq) XEVAL(MAP_SEQ_PREFIX1(f) seq LITOPEN LITCLOSE)
// // do i need va args here?
// #define MAP_SEQ_EAT(...) __VA_ARGS__ CLOSE

// // single deferral isn't enough delay to wait for the IF

// #define MAP_SEQ_PREFIX1(f) MAP_SEQ_ONCE1 BLANK OPEN f , MAP_SEQ_EAT
// #define MAP_SEQ_ONCE1(f, ...) IF_FALSE (ISEMPTY(__VA_ARGS__),        \
//     LITOPEN f OPEN __VA_ARGS__ CLOSE LITCLOSE DOUBLEDEFERAPPLY(MAP_SEQ_PREFIX2, f))

// #define MAP_SEQ_PREFIX2(f) MAP_SEQ_ONCE2 BLANK OPEN f , MAP_SEQ_EAT
// #define MAP_SEQ_ONCE2(f, ...) IF_FALSE (ISEMPTY(__VA_ARGS__),        \
//     LITOPEN f OPEN __VA_ARGS__ CLOSE LITCLOSE DOUBLEDEFERAPPLY(MAP_SEQ_PREFIX1, f))


#define MAP_SEQ(f, seq) XEVAL(MAP_SEQ_PREFIX1(f) seq ( ) )
// do i need va args here?
#define MAP_SEQ_EAT(...) __VA_ARGS__ )

// single deferral isn't enough delay to wait for the IF

#define MAP_SEQ_PREFIX1(f) MAP_SEQ_ONCE1 BLANK ( f , MAP_SEQ_EAT
#define MAP_SEQ_ONCE1(f, ...) IF_FALSE (ISEMPTY(__VA_ARGS__),        \
    ( f ( __VA_ARGS__ ) ) DOUBLEDEFERAPPLY(MAP_SEQ_PREFIX2, f))

#define MAP_SEQ_PREFIX2(f) MAP_SEQ_ONCE1 BLANK ( f , MAP_SEQ_EAT
#define MAP_SEQ_ONCE2(f, ...) IF_FALSE (ISEMPTY(__VA_ARGS__),        \
    ( f ( __VA_ARGS__ ) ) DOUBLEDEFERAPPLY(MAP_SEQ_PREFIX1, f))

#define DOUBLE(x) 2*x
MAP_SEQ(f, (a)(b)(c))
MAP_SEQ(DOUBLE, (a)(b)(c))



// MAP_SEQ(f, (a))
// XEVAL0(MAP_SEQ(f, (a)))
// XEVAL0(XEVAL0(MAP_SEQ(f, (a))))

// MAP_SEQ_ONCE1 ( f , ) ( )

// LITOPEN f OPEN a CLOSE LITCLOSE DOUBLEDEFERAPPLY(MAP_SEQ_PREFIX2, f) ( )
// IF_FALSE (ISEMPTY(a), LITOPEN f OPEN a CLOSE LITCLOSE DOUBLEDEFERAPPLY(MAP_SEQ_PREFIX2, f)) ( )
// XEVAL0(IF_FALSE (ISEMPTY(a), LITOPEN f OPEN a CLOSE LITCLOSE DOUBLEDEFERAPPLY(MAP_SEQ_PREFIX2, f)) ( ))

// LITOPEN f OPEN BLANK CLOSE LITCLOSE MAP_SEQ_PREFIX2 BLANK (f)

// IF_FALSE (ISEMPTY(BLANK), LITOPEN f OPEN BLANK CLOSE LITCLOSE APPLY(MAP_SEQ_PREFIX2, f)   MAP_SEQ_PREFIX2 BLANK (f))
// IF_FALSE (ISEMPTY(BLANK), LITOPEN f OPEN BLANK CLOSE LITCLOSE DEFERAPPLY(MAP_SEQ_PREFIX2, f))



// MAP_SEQ_ONCE BLANK OPEN f , MAP_SEQ_EAT (a)(b)(c) LITOPEN LITCLOSE
// MAP_SEQ_PREFIX(f) (a)(b)(c) LITOPEN LITCLOSE





/////// Parsing

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




/////// Main

#define INPUT Game 1 COLON 3 blue COMMA 4 red SEMICOLON 1 red COMMA 2 green COMMA 6 blue SEMICOLON 2 green EOL
// INPUT
// EVAL0(INPUT)
// EVAL0(EVAL0(INPUT))

#define PARSED_INPUT EVAL1(INPUT)
// PARSED_INPUT

// MAP_PAIR(EVAL0, SUM_TUPLES, PARSED_INPUT)

// SECOND_PAIR(PARSED_INPUT)





