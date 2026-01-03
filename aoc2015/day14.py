from attrs import define


TEST_INPUT = '''Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
'''


@define
class Reindeer:
    name: str
    speed: int
    fly_time: int
    rest_time: int

    def get_distance_travelled_after(self, travel_time):
        full_cycle_time = self.fly_time + self.rest_time
        full_cycle_distance = self.speed * self.fly_time
        num_full_cycles = travel_time // full_cycle_time
        return num_full_cycles * full_cycle_distance + self.speed * min(self.fly_time, travel_time % full_cycle_time)


def parse_line(the_line):
    name, _, tail = the_line.partition(' can fly ')
    speed, _, tail = tail.partition(' km/s for ')
    fly_time, _, tail = tail.partition(' seconds, but then must rest for ')
    rest_time, _, tail = tail.partition(' seconds.')
    assert(tail == '')
    return Reindeer(name, int(speed), int(fly_time), int(rest_time))


def get_farthest_travelled_at(travel_time, reindeers):
    return max((r.get_distance_travelled_after(travel_time) for r in reindeers))


def get_best_scoring_pt2(reindeers, travel_time):
    scores = {r.name: 0 for r in reindeers}
    for t in range(1, travel_time + 1):
        leading_reindeers = None
        leading_dist = -1
        for r in reindeers:
            r_dist = r.get_distance_travelled_after(t)
            if r_dist > leading_dist:
                leading_dist = r_dist
                leading_reindeers = []
            if r_dist == leading_dist:
                leading_reindeers.append(r)
        for r in leading_reindeers:
            scores[r.name] += 1
    return scores


def main():
    test_input = TEST_INPUT
    with open('input/day14.txt') as f:
        test_input = f.read()
    reindeers = [parse_line(line) for line in test_input.splitlines()]
    print(get_farthest_travelled_at(1000, reindeers))
    print(get_farthest_travelled_at(2503, reindeers))
    # part 2
    print(get_best_scoring_pt2(reindeers, 1000))
    print(get_best_scoring_pt2(reindeers, 2503))


if __name__ == '__main__':
    main()
