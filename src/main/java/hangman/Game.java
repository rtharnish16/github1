package hangman;

import java.util.ArrayList;
import java.util.List;

/**
 * Core Hangman game logic: tracks the hidden word, the letters guessed so
 * far, and how many incorrect guesses remain. Deliberately has no console
 * I/O in it, so it can be unit tested without simulating user input.
 */
public class Game {

    private static final int MAX_INCORRECT_GUESSES = 6;

    private final String hiddenWord;
    private String displayWord;
    private final List<Character> guessedLetters;
    private int incorrectGuesses;

    /**
     * @param word the word or phrase to guess. Spaces stay visible in the
     *             display word (only letters are hidden), so multi-word
     *             phrases read naturally while still guessing.
     */
    public Game(String word) {
        this.hiddenWord = word.toUpperCase();
        this.guessedLetters = new ArrayList<>();
        this.incorrectGuesses = 0;

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < hiddenWord.length(); i++) {
            char c = hiddenWord.charAt(i);
            sb.append(c == ' ' ? ' ' : '_');
        }
        this.displayWord = sb.toString();
    }

    /**
     * Registers a guessed letter, updating the display word on a hit.
     *
     * @return true if the letter appears in the hidden word, false if it's
     *         a repeat guess or an incorrect guess.
     */
    public boolean guessLetter(char guess) {
        char upperGuess = Character.toUpperCase(guess);

        if (guessedLetters.contains(upperGuess)) {
            return false;
        }
        guessedLetters.add(upperGuess);

        boolean found = false;
        StringBuilder newDisplay = new StringBuilder(displayWord);
        for (int i = 0; i < hiddenWord.length(); i++) {
            if (hiddenWord.charAt(i) == upperGuess) {
                newDisplay.setCharAt(i, upperGuess);
                found = true;
            }
        }
        displayWord = newDisplay.toString();

        if (!found) {
            incorrectGuesses++;
        }
        return found;
    }

    public String getDisplayWord() {
        return displayWord;
    }

    public String getHiddenWord() {
        return hiddenWord;
    }

    public List<Character> getGuessedLetters() {
        return guessedLetters;
    }

    public int getIncorrectGuesses() {
        return incorrectGuesses;
    }

    public int getMaxIncorrectGuesses() {
        return MAX_INCORRECT_GUESSES;
    }

    public boolean isGameOver() {
        return isWon() || isLost();
    }

    public boolean isWon() {
        return displayWord.indexOf('_') == -1;
    }

    public boolean isLost() {
        return incorrectGuesses >= MAX_INCORRECT_GUESSES;
    }
}
