# Discord Bots

A collection of Discord bots for various purposes.

## Bots Overview

- **deploymentFlip.py**: Manages clan deployments for ev.io
- **discordBot.py**: Basic bot that tracks SOL price
- **ERPriceBot.py**: Tracks ER token price using Birdeye API
- **JupPriceApi.py**: Tracks Jupiter token prices
- **lenderFlip.py**: Manages NFT lending for ev.io
- **LLTotalLoans.py**: Tracks total active loans on Lender Labs
- **LLTVL.py**: Tracks Total Value Locked on Lender Labs
- **SFBHolderPayout.py**: Calculates and displays SFB holder payouts
- **sportsFlip.py**: Tracks live sports scores and game information

## Requirements

- Python 3.9+
- Discord.py
- Required environment variables (see Configuration section)

## Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/Discord-Bots.git
cd Discord-Bots
```

2. Create a virtual environment (recommended):
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory with the following variables:
```
DISCORD-TOKEN=your_discord_bot_token
BIRDEYE-TOKEN=your_birdeye_api_token
SPORT-TOKEN=your_sports_api_token
api-token=your_ev_io_api_token
TOKEN=your_additional_discord_token
FLIP-LENDER-KEY=your_flip_lender_key
RAF-LENDER-KEY=your_raf_lender_key
LENDER-FLIP-LENDER-KEY=your_lender_flip_key
```

## Running the Bots

To run any of the bots:
```sh
python3 <bot_filename>.py
```

Example:
```sh
python3 ERPriceBot.py
```

## Bot Permissions

Make sure your Discord bot has the following permissions:
- Read Messages/View Channels
- Send Messages
- Manage Messages
- Change Nickname
- Manage Nicknames
- Read Message History

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License - feel free to use and modify the code as needed.
