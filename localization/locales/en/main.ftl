# --- Common ---
back-to-menu = ⬅️ Back to Menu
balance = 💰 Balance: ${$balance}
change-language = 🌐 Change Language
language-changed = ✅ Language changed successfully!
choose-language = 🌐 Choose your language:
support = 💬 Support
support-title = 💬 Support
contact-admin = 📞 Contact Administrator
faq = ❓ FAQ
contact-admin-message = 📞 To contact the administrator, write to @admin
faq-message = ❓ FAQ:
1. How to get started?
2. How to create a campaign?
3. How to top up balance?

# --- Main Menu ---
main-menu-welcome = 👋 Welcome, {$user_name}!
games-menu = 🎮 Games Menu

# --- Games Menu ---
games-welcome = Hello, { $user_name }! Your balance: ${ $balance }
games-list = 📜 List of available games
no-pending-games = 😔 No available games to join.
my-games = 🕹️ My Games
create-game = ✨ Create Game
game-history = 📊 Game History
game-not-available-error = ⚠️ This game is no longer available.
cannot-join-own-game-error = 🚫 You cannot join your own game.
insufficient-balance-for-join = 😔 Insufficient funds to join this game.

# --- Game Creation ---
enter-stake = 💰 Enter stake amount (from 5 to 10000):
invalid-stake-format = ⚠️ Invalid stake format. Please enter a number.
stake-must-be-positive = 🚫 Stake must be positive.
stake-must-be-at-least-5 = 💰 Minimum stake is 5.
stake-too-large = 💰 Maximum stake is 10000.
insufficient-balance-for-stake = 😔 Insufficient funds for this stake.
insufficient-balance-for-create = 😔 Insufficient funds to create a game.
max-games-reached = 🚫 You have reached the active games limit (5).
game-created-success = ✅ Game created successfully!
    .type = { $game_emoji } Type: { $game_type }
    .stake = 💵 Stake: { $stake }
    .rolls = 🎲 Rolls: { $rolls }
game-creation-error = ❌ Error creating game.

# --- My Games ---
my-games-title = 🎯 My Games
no-active-games = 😔 You have no active games.
game-info = 💎 #{$game_id} | {$game_emoji} | Stake: ${$stake} | Status: {$status}
cancel-game = ❌ Cancel Game
confirm-cancel = ❓ Are you sure you want to cancel game #{$game_id}?
game-cancelled = ✅ Game #{$game_id} has been cancelled.
cancel-error = ❌ Failed to cancel the game.

# --- Game Room ---
game-header = { $game_emoji } Game #{ $game_id }
game-bank = 🏦 Bank: ${$bank}
player-info = { $player } | Score: { $score } | Rolls: { $rolls }
turn-of-player = 👉 It's { $player }'s turn
roll-dice-button = 🎲 Roll Dice
game-over = 🏁 Game Over!
winner-is = 🏆 The winner is { $winner }!
your-prize = 💰 Your prize: ${ $prize }
no-winner = 🤝 It's a draw!
waiting-for-opponent = ⏳ Waiting for opponent...
game-start-notification = 🚀 Game #{ $game_id } has started!
roll-notification = { $player } rolled the dice and got { $roll_value }.
your-turn-notification = 👉 It's your turn in game #{ $game_id }!
not-your-turn = 🚫 It's not your turn.
