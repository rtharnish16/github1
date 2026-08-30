package hangman;

import java.util.Scanner;

/**
 * Entry point: a console Hangman game supporting either a computer-chosen
 * word (single player) or one player setting a word/phrase for the rest of
 * the group to guess in turns.
 */
public class Main {

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        ConsoleUI ui = new ConsoleUI();
        ui.displayWelcome();

        boolean playAgain = true;
        while (playAgain) {
            int numPlayers = getNumberOfPlayers();
            int gameMode = getGameMode();

            String wordToGuess;
            if (gameMode == 1) {
                wordToGuess = getCustomWordFromPlayer();
            } else {
                WordBank wordBank = new WordBank();
                wordToGuess = wordBank.selectRandomWord();
            }

            playGame(wordToGuess, numPlayers, ui);

            playAgain = askPlayAgain();
        }

        System.out.println("\nThank you for playing Hangman! Goodbye!");
    }

    private static int getNumberOfPlayers() {
        while (true) {
            System.out.print("Enter number of players (1 for single player, 2+ for multiplayer): ");
            try {
                int num = Integer.parseInt(scanner.nextLine().trim());
                if (num < 1) {
                    System.out.println("Error: Please enter at least 1 player.");
                    continue;
                }
                return num;
            } catch (NumberFormatException e) {
                System.out.println("Error: Please enter a valid number.");
            }
        }
    }

    private static int getGameMode() {
        while (true) {
            System.out.println("\nSelect game mode:");
            System.out.println("1. First player enters word/phrase");
            System.out.println("2. Computer selects random word");
            System.out.print("Enter your choice (1 or 2): ");
            try {
                int choice = Integer.parseInt(scanner.nextLine().trim());
                if (choice == 1 || choice == 2) {
                    return choice;
                }
                System.out.println("Error: Please enter 1 or 2.");
            } catch (NumberFormatException e) {
                System.out.println("Error: Please enter a valid number.");
            }
        }
    }

    private static String getCustomWordFromPlayer() {
        System.out.println("\n" + "=".repeat(50));
        System.out.println("Player 1, please enter a word, phrase, or sentence.");
        System.out.println("(Only letters and spaces allowed)");
        System.out.println("=".repeat(50));

        while (true) {
            System.out.print("Enter word/phrase: ");
            String input = scanner.nextLine().trim();

            if (input.isEmpty()) {
                System.out.println("Error: Input cannot be empty.");
                continue;
            }

            boolean valid = true;
            for (char c : input.toCharArray()) {
                if (!Character.isLetter(c) && c != ' ') {
                    valid = false;
                    break;
                }
            }
            if (!valid) {
                System.out.println("Error: Please use only letters and spaces.");
                continue;
            }

            System.out.println("\nWord/phrase has been set! Other players, get ready to guess!\n");
            return input.toUpperCase();
        }
    }

    private static void playGame(String wordToGuess, int numPlayers, ConsoleUI ui) {
        Game game = new Game(wordToGuess);

        if (numPlayers == 1) {
            System.out.println("Starting single player game...\n");
        } else {
            System.out.println("Starting multiplayer game with " + numPlayers + " players...");
            System.out.println("Players take turns guessing!\n");
        }

        int turn = 0;
        while (!game.isGameOver()) {
            ui.displayGameState(game);
            String turnLabel = numPlayers > 1 ? "Player " + (turn % numPlayers + 1) : "";
            char guess = ui.getGuessFromUser(turnLabel);
            game.guessLetter(guess);
            turn++;
        }

        ui.displayResult(game);
    }

    private static boolean askPlayAgain() {
        while (true) {
            System.out.print("\nDo you want to play again? (Y/N): ");
            String input = scanner.nextLine().trim().toUpperCase();

            if (input.equals("Y") || input.equals("YES")) {
                System.out.println("\n" + "=".repeat(50) + "\n");
                return true;
            } else if (input.equals("N") || input.equals("NO")) {
                return false;
            }
            System.out.println("Error: Please enter Y or N.");
        }
    }
}
