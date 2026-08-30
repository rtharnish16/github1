# Design Notes

## Game flow

1. `Main` asks how many players and which game mode to use.
2. **Mode 1 (custom word):** Player 1 enters a word or phrase (letters and
   spaces only); it's hidden from the display but every other player takes
   turns guessing letters.
3. **Mode 2 (computer word):** `WordBank` picks a random word from a small
   built-in list.
4. `Main.playGame` drives the guess loop: it asks `ConsoleUI` for a letter,
   passes it to `Game.guessLetter`, and repeats until `Game.isGameOver()`.
   In multiplayer, the turn number cycles through "Player 1", "Player 2", ...
5. `ConsoleUI.displayResult` shows the outcome; `Main.askPlayAgain` offers
   another round.

## Main classes

| Class | Responsibility |
|---|---|
| `Game` | Word masking, guess validation state, win/loss rules. No console I/O — fully unit-testable. |
| `ConsoleUI` | All `System.out`/`Scanner` interaction: prompts, the ASCII hangman drawing, formatting guessed letters. |
| `WordBank` | The built-in word list for computer-selected games. |
| `Main` | Orchestrates a full session: player/mode setup, the game loop, replay. |

## How words are selected

- If a human sets the word (mode 1), it's validated to contain only letters
  and spaces, then stored upper-cased. Spaces are preserved (not hidden)
  in the display word so a multi-word phrase still reads naturally.
- If the computer picks (mode 2), `WordBank.selectRandomWord()` returns one
  entry from a fixed `String[]` using `java.util.Random`.

## Key design decisions

- **Logic and I/O are separate classes.** `Game` has no `Scanner` or
  `System.out` calls, which is what makes `GameTest` possible without
  simulating keyboard input.
- **Guess handling is case-insensitive and de-duplicated.** A repeat guess
  (in either case) doesn't count against the player twice.
- **Multiplayer turn order is explicit.** The original version described a
  multiplayer mode but didn't show whose turn it was; this version
  prints "Player N's turn" before each prompt so the feature is fully
  functional, not just an input count.
