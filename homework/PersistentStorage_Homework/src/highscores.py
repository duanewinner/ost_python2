#!/usr/local/bin/python3

import shelve

fn = "my_shelf"

def record(player, score):

    shelf = shelve.open(fn)

    if player not in shelf or score > shelf[player]:
        shelf[player] = score
    else:
        score = shelf[player]
     
    shelf.close()
    return score

