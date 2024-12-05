from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Card types
card_sequence = ["challenge", "risk", "event"]

@app.route('/')
def setup():
    """Team setup page for registering all teams."""
    if 'teams' not in session:
        session['teams'] = []  # Initialize an empty list for teams
    return render_template('setup.html', teams=session['teams'])

@app.route('/start_game', methods=['POST'])
def start_game():
    """Start the game after all teams are registered."""
    team_name = request.form['team_name']

    # Ensure the team name is not empty
    if team_name.strip():
        # Add the team to the session
        session['teams'].append({"name": team_name.strip(), "points": 1000, "history": [], "drawn_cards": []})

    # After registering the teams, show the setup page again to add more teams if needed
    return redirect(url_for('setup'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    """Main game page where teams play their turn."""
    if 'teams' not in session:
        return redirect(url_for('setup'))  # Redirect if no teams are registered
    
    teams = session['teams']
    current_team_index = session['current_team_index']
    current_team = teams[current_team_index]

    # Handle team selection
    if request.method == 'POST' and 'teamSelect' in request.form:
        selected_team_index = int(request.form['teamSelect'])
        session['current_team_index'] = selected_team_index
        return redirect(url_for('game'))  # Refresh the page with the new team selected

    return render_template(
        'game.html',
        teams=teams,
        current_team=current_team,
        current_team_index=current_team_index
    )

@app.route('/draw_card', methods=['POST'])
def draw_card():
    """Draw a card for the current team and update their score."""
    if 'teams' not in session:
        return redirect(url_for('setup'))  # Redirect if no teams are registered

    teams = session['teams']
    current_team_index = session['current_team_index']
    current_team = teams[current_team_index]

    card_type = request.form['cardType']
    if card_type not in current_team['drawn_cards']:
        result = draw_card_for_team(card_type, current_team)
        current_team['history'].append(result)
        current_team['drawn_cards'].append(card_type)
        session['teams'] = teams  # Save the updated teams
    return redirect(url_for('game'))

def draw_card_for_team(card_type, current_team):
    """Process the card drawing and update the team score."""
    if card_type == "challenge":
        card = "Product Development" if random.random() > 0.5 else "Market Expansion"
        cost = 200 if card == "Product Development" else 300
        current_team["points"] -= cost
        return {"card": card, "pointsChange": -cost}
    elif card_type == "risk":
        card = "Social Media Blitz" if random.random() > 0.5 else "Influencer Marketing"
        cost = 200 if card == "Social Media Blitz" else 300
        current_team["points"] -= cost
        return {"card": card, "pointsChange": -cost}
    elif card_type == "event":
        outcome = "Economic Boom" if random.random() > 0.5 else "Market Crash"
        change = random.randint(60, 80) if outcome == "Economic Boom" else -random.randint(20, 40)
        current_team["points"] += change
        return {"card": outcome, "pointsChange": change}

@app.route('/final_score')
def final_score():
    """Show the final scorecard with all teams' scores."""
    teams = session['teams']
    return render_template('final_score.html', teams=teams)

if __name__ == '__main__':
    app.run(debug=True)
