def start_spin():
    strength = random.uniform(0.8, 1.0) # Increase the minimum strength to make it faster

    distance = strength * num_leds * 2 * math.pi

    circumference = num_leds * 2 * math.pi
    rotations = int(distance / circumference)

    rotations += random.randint(0, 2)

    total_steps = rotations * num_leds

    friction = 0.9
    speed = 1.9 * strength # Increase the speed to make it faster

    starting_position = random.randint(0, num_leds - 1)

    # Disable the button before starting the spin
    GPIO.remove_event_detect(button_pin)

    i = starting_position
    for i in range(starting_position, starting_position - total_steps, -1):
        remaining_steps = total_steps - (starting_position - i)
        current_speed = speed * remaining_steps / total_steps * friction

        for j in range(5):
            prev_index = (i + 5 - j) % num_leds
            pixels[prev_index] = (0, 0, 0, 0)

        for j in range(5):
            index = (i - j) % num_leds
            pixels[index] = (0, 0, 255, 0)

        pixels.show()

        delay_time = 0.001 / current_speed
        time.sleep(delay_time)

    first_led_index = i % num_leds
    spin_action(first_led_index) # call spin_action with the first_led_index as argument

    # Enable the button again after the spin is finished
    GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)
