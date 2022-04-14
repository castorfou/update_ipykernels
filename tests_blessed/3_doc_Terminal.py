import blessed

term = blessed.Terminal()
print(term.height,term.width)


print(term.green_reverse('hello'))

print(term.number_of_colors)

print(f"{term.green}Yellow is brown, {term.bright_yellow}"
          f"Bright yellow is actually yellow!{term.normal}")

print(term.blink("Insert System disk into drive A:"))

print(term.underline_bold_green_on_yellow('They live! In sewers!'))

print(term.home + term.on_black + term.clear)
# print(term.home)

print(f"blessed {term.link('https://blessed.readthedocs.org', 'documentation')}")


# C'est le full screen

# with term.fullscreen(), term.cbreak():
#     print(term.move_y(term.height // 2) +
#           term.center('press any key').rstrip())
#     term.inkey()


if term.does_styling:
    with term.location(x=0, y=term.height - 1):
        print('Progress: [=======>   ]')
print(term.bold("60%"))