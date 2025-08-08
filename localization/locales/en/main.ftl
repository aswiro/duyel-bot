admin-welcome-message =
    👋 Welcome to the admin panel, {$user_name}!

    You have extended rights to manage the bot and groups.

advertiser-not-found = Advertiser not found

advertiser-menu =
    👋 Welcome, {$company_name}!

    💰 Balance: ${$balance}

    Select an action:

no-campaigns = You don't have any campaigns yet.

my-campaigns-header = 📋 My Campaigns:

campaign-info =
    📊 Campaign: {$name}
    💰 Budget: ${$budget}
    📈 Status: {$status}
    📅 Created: {$created_at}

campaign-not-found = Campaign not found

campaign-details =
    📊 Campaign Details

    📝 Name: {$name}
    💰 Daily Budget: ${$daily_budget}
    💸 Spent: ${$spent_amount}
    📈 Status: {$status}
    📅 Start Date: {$start_date}
    📅 End Date: {$end_date}
    🕒 Created: {$created_at}

create-campaign-enter-name = 📝 Enter campaign name:

campaign-name-too-short = ❌ Campaign name is too short. Minimum 3 characters.

campaign-name-too-long = ❌ Campaign name is too long. Maximum 100 characters.

create-campaign-enter-budget = 💰 Enter daily budget (in USD):

budget-must-be-positive = ❌ Budget must be positive.

budget-too-large = ❌ Budget is too large. Maximum $10,000 per day.

invalid-budget-format = ❌ Invalid budget format. Please enter a number.

create-campaign-enter-start-date = 📅 Choose start date:

create-campaign-enter-end-date = 📅 Choose end date:

start-date-in-past = ❌ Start date cannot be in the past.

invalid-date-format = ❌ Invalid date format. Use DD.MM.YYYY

end-date-before-start = ❌ End date cannot be before start date.

create-campaign-confirmation =
    ✅ Campaign Summary

    📝 Name: {$name}
    💰 Daily Budget: ${$budget}
    📅 Start Date: {$start_date}
    📅 End Date: {$end_date}

    Confirm creation?

campaign-created-success = ✅ Campaign '{$name}' created successfully!

campaign-creation-error = ❌ Error creating campaign. Please try again.

admin-ad-menu = 🔧 Admin Ad Menu

moderation-queue-header = 📋 Creative Moderation Queue

no-creatives-pending = No creatives pending moderation.

moderation-error = Error during creative moderation.

creative-not-found = Creative not found.

creative-details-header = 📝 Creative Details

creative-type = Type: {$type}

creative-campaign = Campaign: {$campaign}

creative-advertiser = Advertiser: {$advertiser}

creative-created = Created: {$date}

creative-approved-success = ✅ Creative approved successfully!

select-rejection-reason = Select rejection reason:

reason-inappropriate = Inappropriate content

reason-misleading = Misleading information

reason-quality = Poor quality

reason-policy = Policy violation

creative-rejected-success = ❌ Creative rejected. Reason: {$reason}

enter-custom-reason = Enter rejection reason:

no-campaigns-found = ❌ No campaigns found

all-campaigns-title = 📊 All Ad Campaigns

total-campaigns = Total campaigns: {$count}

page-info = Page {$current} of {$total}

error-occurred = ❌ An error occurred

advertiser_not_found = ❌ Advertiser not found

advertiser_details =
    📊 Advertiser: {$name}

    💰 Balance: {$balance}₽
    📈 Total campaigns: {$total_campaigns}
    🟢 Active campaigns: {$active_campaigns}
    💸 Total spent: {$total_spent}₽
    📅 Registration date: {$created_at}

no-advertisers-found = No advertisers found

advertisers-management-title = 🏢 Advertiser Management

total-advertisers = Total advertisers: {$count}

advertisers-page-info = Page {$current} of {$total}

captcha-settings-menu = Captcha Settings

setting-updated = Settings updated!

select-captcha-type = Select captcha type

select-captcha-size = Select captcha size

select-captcha-difficulty = Select captcha difficulty

select-captcha-chars-mode = Character Mode

enter-new-value = Enter new value

invalid-numeric-value = ❌ Invalid value. Please enter a valid number.

error-generating-captcha = ❌ Error getting groups list.

captcha-preview-caption = Captcha preview

select_group = 📋 Select a group to configure filters:

no-filters-found = ❌ No filters found for this group.

unknown-group = Unknown group

filters-for-group = 🔧 Filters for group: {$group_name}

filter-updated-success = ✅ Filter successfully updated for group: {$group_name}

filter-max-message-length = Max message length

filter-bonus-per-user = Bonus per user

filter-bonus-checkpoint = Bonus checkpoint

enter-value = Enter new value for filter {$filter_name}. Current value: {$current_value}

invalid-message-length-range = ❌ Invalid value! Message length must be between 10 and 4000 characters.

invalid-bonus-per-user-range = ❌ Invalid value! Bonus per user must be between 1 and 100 units.

invalid-bonus-checkpoint-range = ❌ Invalid value! Bonus checkpoint must be between 100 and 10000 units.

invalid-number-format = ❌ Invalid group format. Please send a valid group link or username.

filter-update-error = ❌ Error updating filter. Please try again.

error-getting-groups = ❌ Error getting groups list.

groups-list-empty = 📭 Groups list is empty.

all-groups-header = 📋 All groups:

add-group-instructions =
    Please send me the group link or username (e.g., @groupname or
    https://t.me/groupname)

invalid-group-format = ❌ Invalid group format. Please send a valid group link or username.

balance = Balance
enter-stake = Enter stake
insufficient-balance-for-create = Insufficient balance to create a game.
getting-group-info = 🔍 Getting group information...

getting-admins-list = 👥 Getting administrators list...

saving-to-database = 💾 Saving to database...

no-username = No username

group-added-success = ✅ Group successfully added to monitoring!

error-chat-not-found = ❌ Chat not found. Please check the link or username.

error-bot-not-member =
    ❌ Bot is not a member of this group. Please add the bot to the group
    first.

error-insufficient-rights = ❌ Bot has insufficient rights in this group.

error-adding-group = ❌ Error adding group. Please try again later.

error-removing-group = ❌ Error removing group.

choose-language = 🌐 Choose your language:

welcome-message =
    👋 Welcome, {$user_name}!

    I'm a bot for monitoring Telegram groups. Choose an action from the menu
    below:

language-changed = ✅ Language changed successfully!

my-campaigns = 📋 My Campaigns

create-campaign = ➕ Create Campaign

my-balance = 💰 My Balance

ad-analytics = 📊 Analytics

edit_advertiser_balance = 💰 Edit Balance

view_advertiser_campaigns = 📈 Advertiser Campaigns

block_advertiser = 🚫 Block

back_to_advertisers = ⬅️ Back to Advertisers

back-to-ad-menu = ⬅️ Back to Ad Menu

campaign-analytics = 📊 Campaign Analytics

show-more-campaigns = 📄 Show More

activate-campaign = ▶️ Activate

pause-campaign = ⏸️ Pause

register-advertiser = 🚀 Become an Advertiser

register-advertiser-enter-name = Enter your company name:

already-advertiser = You are already registered as an advertiser!

invalid-company-name = Company name must be between 2 and 100 characters

advertiser-registered-success = 🎉 Congratulations! You have successfully registered as an advertiser for '{$company_name}'

advertiser-registration-error = ❌ Error during registration. Please try again later.

resume-campaign = ▶️ Resume

edit-campaign = ✏️ Edit

campaign-creatives = 🎨 Creatives

back-to-campaigns = 🔙 Back to Campaigns

cancel = ❌ Cancel

start-now = 🚀 Start Now

one-week = 📅 One Week

one-month = 📅 One Month

confirm-create = ✅ Confirm

view-campaign = 👁️ View Campaign

moderate-ads = 🔍 Moderate Ads

all-campaigns = 📋 All Campaigns

advertiser-management = 👥 Advertiser Management

ad-analytics-admin = 📊 Ad Analytics (Admin)

no-pending-creatives = No pending creatives

show-more-creatives = Show more creatives

refresh-queue = Refresh queue

back-to-admin-menu = 🔙 Back to admin menu

approve-creative = Approve

reject-creative = Reject

back-to-moderation = Back to moderation

inappropriate-content = Inappropriate content

misleading-info = Misleading information

poor-quality = Poor quality

policy-violation = Policy violation

custom-reason = Custom reason

back-to-creative = Back to creative

back-to-menu = ⬅️ Back to Menu

change-language = 🌐 Change Language

ad-menu = Ad Settings

add-group = ➕ Add Group

groups-menu = 👥 Groups Menu

filters-menu = 🔧 Filters Menu

captcha-type = Captcha type

captcha-size = Captcha size

captcha-difficulty = Captcha difficulty

easy = Easy

light = Light

medium = Medium

hard = Hard

expert = Expert

nightmare = Nightmare

captcha-chars-mode = Character Mode

nums = Numbers

hex = Hex

ascii = ASCII

captcha-multicolor = Multicolor

captcha-margin = Margin

captcha-multiplication = Multiplication

captcha-timeout = Timeout

captcha-max-attempts = Max attempts

captcha-auto-kick = Auto-kick

preview-captcha = Preview captcha

back-to-filters = ⬅️ Back to groups

captcha-type-standard = Standard

captcha-type-math = Math

back = Back

filter-hashtag = Hashtags

filter-url = URL links

filter-email = Email addresses

filter-ads = Advertisements

filter-phone-number = Phone numbers

filter-forbidden-words = Forbidden words

filter-track-members = Track members

filter-captcha = Captcha

captcha-settings = Captcha settings

filter-bonuses-enabled = Bonus system

back-to-groups = ⬅️ Back to groups

support = 💬 Support

support-title = 💬 Support

contact-admin = 📞 Contact Administrator

faq = ❓ Frequently Asked Questions

contact-admin-message = 📞 To contact the administrator, write to @admin

faq-message = ❓ Frequently Asked Questions:
1. How to get started?
2. How to create a campaign?
3. How to top up balance?

games-menu = 🎮 Games Menu

games-welcome = 👋 Welcome, {$user_name}!
    💰 Your balance: {$balance} USD.

games-list = 📋 Games List

my-games-welcome = 👋 Your games, {$user_name}!
    💰 Your balance: {$balance} USD.

my-games-list = 📋 Available games

my-games = 🎯 My Games

no-pending-games = 🚫 No available games

create-game = ➕ Create Game

join-game = 🎮 Join Game

game-history = 📊 Game History

back-to-menu = ⬅️ Back to Menu

# Game Creation
select-game-type = 🎮 Select game type:

game-type-dice = Dice
game-type-darts = Darts
game-type-basketball = Basketball
game-type-football = Football
game-type-slot = Slot
game-type-bowling = Bowling

balance = Balance
current-stake = Current stake
enter-stake = Enter stake amount
stake-description = Use +/- buttons or enter amount from $1 to $10,000
select-rolls = Select number of rolls
rolls-description = Choose 3 or 5 rolls for the game
confirm-game-creation = Confirm game creation
game-details = Game details
stake = Stake
rolls = Rolls
confirm = Confirm
cancel = Cancel
stake-must-be-positive = Stake must be positive
stake-must-be-at-least-5 = Stake must be at least $5
stake-too-large = Stake cannot exceed $10,000

invalid-stake-format = Invalid stake format
insufficient-balance = Insufficient balance
insufficient-balance-for-stake = Insufficient balance for this stake
game-created-success = ✅ Game created successfully!
    {$game_emoji} Type: {$game_type},
    💵 Stake: ${$stake},
    🎲 Rolls: {$rolls}
    💰 Your new balance is {$balance} USD.
game-creation-error = Error creating game

next = ➡️ Next
back = ⬅️ Back

game-deleted-success = {$game_emoji} Game #{$game_id} - {$stake} USD has been deleted.
        Your new balance is {$balance} USD.
game-deleted-error = Error deleting game

max-games-reached = ⛔️ You have reached the maximum number of games (5)
❎ For create new game, you must delete one of your existing games.

balance = 💰 Balance
