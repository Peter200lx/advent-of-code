DATA = """491 players; last marble is worth 71058 points"""
EXAMPLE_DATA = """10 players; last marble is worth 1618 points"""  # high score is 8317


class Marble:
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

    def add_marble(self, new_value):
        if not new_value % 23:
            away_marble = self
            for _ in range(7):
                away_marble = away_marble.prev
            away_marble.next.prev = away_marble.prev
            away_marble.prev.next = away_marble.next
            return away_marble.next, new_value + away_marble.value
        else:
            new_marble = Marble(new_value)
            one_away, two_away = self.next, self.next.next
            new_marble.next = two_away
            new_marble.prev = one_away
            one_away.next = new_marble
            two_away.prev = new_marble
            return new_marble, 0


def winning_score(num_players, last_marble):
    latest_marble = Marble(0)
    players = [0] * num_players
    for next_marble in range(1, last_marble):
        latest_marble, score = latest_marble.add_marble(next_marble)
        players[next_marble % num_players] += score
    return max(players)


if __name__ == "__main__":
    print(winning_score(491, 71058))
    print(winning_score(491, 71058 * 100))
