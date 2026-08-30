# Changelog

## [1.0.0] - Initial Release

### Added
- Core Hangman game logic (word masking, guess tracking, win/loss detection)
- Console UI with ASCII-art hangman drawing
- Single-player mode with a computer-selected word
- Multiplayer mode: one player sets a custom word/phrase, others take turns
  guessing, with a per-turn player indicator
- Input validation (single-letter guesses, repeated-guess detection, custom
  word/phrase validation)
- Replay prompt at the end of each round
- JUnit 5 test suite for the core game logic
