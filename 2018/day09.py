
DATA = """491 players; last marble is worth 71058 points"""
EXAMPLE_DATA = """10 players; last marble is worth 1618 points"""  # high score is 8317


class Marble:
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

    def add_marble(self, new_marble):
        if not new_marble.value % 23:
            away_marble = self
            for _ in range(7):
                away_marble = away_marble.prev
            away_marble.next.prev = away_marble.prev
            away_marble.prev.next = away_marble.next
            return away_marble.next, new_marble.value + away_marble.value
        else:
            one_away = self.next
            two_away = self.next.next
            new_marble.next = two_away
            new_marble.prev = one_away
            one_away.next = new_marble
            two_away.prev = new_marble
            return new_marble, 0


def winning_score(num_players, last_marble):
    next_marble = 0
    latest_marble = Marble(next_marble)
    next_marble += 1
    players = [0] * num_players
    player = 0
    while latest_marble.value != last_marble:
        latest_marble, score = latest_marble.add_marble(Marble(next_marble))
        next_marble += 1
        players[player] += score
        player += 1
        player %= num_players
    return max(players)


if __name__ == '__main__':
    print(winning_score(491, 71058))
    print(winning_score(491, 71058 * 100))
