def pick(items, rng, exclude=()):
  """Return a random item not in exclude; raise ValueError if none left."""
  candidates = [item for item in items if item not in exclude]
  if not candidates:
    raise ValueError("no items left to pick from")
  return rng.choice(candidates)


def draw(names, questions, rng, used_names=(), used_questions=()):
  """Return (name, question), skipping anything in used_names / used_questions."""
  return (pick(names, rng, used_names), pick(questions, rng, used_questions))


def rand_draw(rng, n_list, q_list):
  return draw(n_list, q_list, rng)


def pick_excluding(rng, items, exclude):
  """Pick a random item not in exclude; auto-reset (ignore exclude) once every item has been used."""
  if not items:
    return None
  try:
    return pick(items, rng, exclude)
  except ValueError:
    return pick(items, rng)


def rand_draw_no_repeat(rng, n_list, q_list, used_names, used_questions):
  chosen_name = pick_excluding(rng, n_list, used_names)
  chosen_question = pick_excluding(rng, q_list, used_questions)

  return (chosen_name, chosen_question)
