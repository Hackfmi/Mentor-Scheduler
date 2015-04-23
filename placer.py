from tabulate import tabulate


def lowest_intersection(s1, s2):
    s1 = sorted(s1)
    s2 = sorted(s2)

    largest = s1
    smallest = s2


    if len(s2) > len(s1):
        largest = s2
        smallest = s1

    start = 0
    end = len(largest)

    while start < end:
        if largest[start] in smallest:
            return largest[start]
        start += 1
    return None


TEAMS = ["T{}".format(i) for i in range(1, 5)]
MENTORS = ["M{}".format(i) for i in range(1, 6)]
SLOTS = ["S{}".format(i) for i in range(1, 5)]
MAX_PICK = 3

INPUT = [("T1", ["M1", "M2", "M3"]),
         ("T2", ["M1", "M2", "M3"]),
         ("T3", ["M2", "M3", "M4"])]

chosen_mentors = []
teams_with_choice = []
mentors_to_teams = {}

for team, mentors in INPUT:
    if team not in teams_with_choice:
        teams_with_choice.append(team)
    
    for mentor in mentors:
        if mentor not in mentors_to_teams:
            mentors_to_teams[mentor] = [team]
        else:
            mentors_to_teams[mentor].append(team)

        if mentor not in chosen_mentors:
            chosen_mentors.append(mentor)


mentor_slots_table = {mentor: SLOTS[:] for mentor in chosen_mentors}
team_slots_table = {team: SLOTS[:] for team in teams_with_choice}


leftovers = []
result = {}

for mentor in chosen_mentors:
    teams = mentors_to_teams[mentor]
    

    for team in teams:
        mentor_free_slots = mentor_slots_table[mentor]
        team_free_slots = team_slots_table[team]

        first_free_slot = lowest_intersection(mentor_free_slots, team_free_slots)
        if first_free_slot is None:
            leftovers.append((team, mentor))
            continue

        if mentor not in result:
            result[mentor] = {}
        
        result[mentor][first_free_slot] = team

        if len(mentor_free_slots) != 0:
            mentor_free_slots.remove(first_free_slot)
        
        if len(team_free_slots) != 0:
            team_free_slots.remove(first_free_slot)
            


headers = ["Slots"] + chosen_mentors

table = []

for slot in SLOTS:
    teams_for_slot = []

    for mentor in chosen_mentors:
        if slot in result[mentor]:
            teams_for_slot.append(result[mentor][slot])
        else:
            teams_for_slot.append("EMPTY")
    
    table.append([slot] + teams_for_slot)

print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
print("Leftovers: ")
print(leftovers)
