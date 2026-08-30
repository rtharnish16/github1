package hangman;

import java.util.List;
import java.util.Scanner;

/**
 * All console input/output for the game lives here, kept separate from
 * {@link Game} so the game rules can be unit tested without a keyboard.
 */
public class ConsoleUI {

    private final Scanner scanner = new Scanner(System.in);

    public void displayWelcome() {
        System.out.println("===== Welcome to Hangman game! =====");
        System.out.println();
    }

    public void displayGameState(Game game) {
        System.out.println("------------------------------------");
        drawHangman(game.getIncorrectGuesses());
        System.out.println("Word: " + game.getDisplayWord());
        System.out.println("Incorrect Guesses: " + game.getIncorrectGuesses()
                + "/" + game.getMaxIncorrectGuesses());
        System.out.println("Used Letters: " + formatGuessedLetters(game.getGuessedLetters()));
    }

    /**
     * Prompts for a single letter, re-prompting on empty, multi-character,
     * or non-alphabetic input. {@code turnLabel} (e.g. "Player 2") is
     * printed before the prompt in multiplayer games; pass an empty string
     * for single-player.
     */
    public char getGuessFromUser(String turnLabel) {
        while (true) {
            System.out.println("------------------------------------");
            if (!turnLabel.isEmpty()) {
                System.out.println(turnLabel + "'s turn.");
            }
            System.out.print("Guess a letter: ");
            String input = scanner.nextLine().trim();

            if (input.isEmpty()) {
                System.out.println("Error: Please enter a letter.");
                continue;
            }
            if (input.length() != 1) {
                System.out.println("Error: Please enter only one letter.");
                continue;
            }
            char guess = input.charAt(0);
            if (!Character.isLetter(guess)) {
                System.out.println("Error: Please enter a valid alphabetic character.");
                continue;
            }
            return guess;
        }
    }

    public void displayResult(Game game) {
        System.out.println("===== Game Over! =====");
        if (game.isWon()) {
            System.out.println("Congratulations, you have WON!");
        } else {
            System.out.println("Sorry, you LOST! The word was: " + game.getHiddenWord());
            drawHangman(game.getIncorrectGuesses());
        }
    }

    public Scanner getScanner() {
        return scanner;
    }

    private String formatGuessedLetters(List<Character> letters) {
        if (letters.isEmpty()) {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < letters.size(); i++) {
            sb.append(letters.get(i));
            if (i < letters.size() - 1) {
                sb.append(", ");
            }
        }
        return sb.toString();
    }

    private void drawHangman(int stage) {
        System.out.println("+---+");
        System.out.println("|   |");
        System.out.println(stage >= 1 ? "|   O" : "|   ");

        if (stage >= 4) {
            System.out.println("|  /|\\");
        } else if (stage >= 3) {
            System.out.println("|  /|");
        } else if (stage >= 2) {
            System.out.println("|  |");
        } else {
            System.out.println("|  ");
        }

        if (stage >= 6) {
            System.out.println("|  / \\");
        } else if (stage >= 5) {
            System.out.println("| /");
        } else {
            System.out.println("| ");
        }

        System.out.println("|");
        System.out.println("=======");
    }
}
